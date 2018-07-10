# coding: utf-8
"""
Read YAML-formatted metadata files from ./metadata.
"""

import datetime
import logging
import os
import pkgutil
from pathlib import Path

import attr
import yaml


@attr.s
class Meta(object):
    """Metadata for election returns.

    Args:
        dataset_fname (str): Filename of the dataset YAML in directory `medsldocs/metadata/dataset`,
            e.g. `2016-precinct-president.yaml`.

    """
    dataset_fname = attr.ib(default='2016-precinct-president.yaml')

    def __attrs_post_init__(self):
        self.dataset_meta = self._read_dataset_yaml(self.dataset_fname)
        self.dataset_meta['version'] = str(datetime.datetime.today().date())
        self.variable_meta = self._read_variable_yaml()
        self.dataset_name = Path(self.dataset_fname).stem

    def __iter__(self):
        for k, v in self.dataset_meta.items():
            yield k, v

    def _read_dataset_yaml(self, dataset_fname):
        """Read metadata for a dataset.

        Args:
            dataset_fname (str): Filename of the dataset YAML in directory `medsldocs/metadata/dataset`.
        """
        meta_bytes = pkgutil.get_data('medsldocs', os.path.join('metadata', 'dataset', dataset_fname))
        meta = yaml.load(meta_bytes.decode('utf-8'))
        if 'inherits' in meta:
            # The dataset inherits metadata from another file; read each of these
            for inherited_path in meta['inherits']:
                path = os.path.join('metadata', 'dataset', 'common', inherited_path)
                inherited_meta_bytes = pkgutil.get_data('medsldocs', path)
                inherited = yaml.load(inherited_meta_bytes.decode('utf-8'))
                for k, v in inherited.items():
                    # Dataset metadata takes precedence; ignore existing keys
                    if k not in meta:
                        meta[k] = v
        return meta

    def _read_variable_yaml(self):
        """Read metadata for all the variables in a dataset.
        """
        # Variable definitions are common to all election-return datasets.
        meta_bytes = pkgutil.get_data('medsldocs', os.path.join('metadata', 'variables.yaml'))
        meta = yaml.load(meta_bytes.decode('utf-8'))
        # The 'variables' key of the dataset metadata is a list of the variables that appear in the dataset.
        # Filter definitions to those actually in the dataset.
        meta = [var for var in meta if var['name'] in self.dataset_meta['variables']]
        if 'variable_notes' in self.dataset_meta:
            logging.debug('Updating variable notes from dataset metadata:')
            for var in meta:
                for note in self.dataset_meta['variable_notes']:
                    if var['name'] == note['name']:
                        var['note'] = note['note']
                        logging.debug('  {}'.format(var['name']))
        return meta

    def to_dict(self):
        return dict(dataset=self.dataset_meta, variables=self.variable_meta)


def update_congress():
    """Update ``members-of-congress.yaml`` with the latest data from the congress-legislators repo.
    """
    legislators = yaml.load(Path('congress-legislators', 'legislators-current.yaml').read_text())
    legislators.append(yaml.load(Path('congress-legislators', 'legislators-historical.yaml').read_text()))
    # Shape into a dictionary with bioguide as top-level key
    data = {l['id']['bioguide']: l for l in legislators}
    # Looks like this:
    # data['B000944']['id']
    # data['B000944']['name']
    # data['B000944']['bio']
    # data['B000944']['terms']
    Path('medsl', 'metadata', 'candidates', 'members-of-congress.yaml').write_text(yaml.dump(data))
