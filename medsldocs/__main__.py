#!/usr/bin/env python3
# coding: utf-8
"""
Create documentation for MEDSL releases: codebooks, coverage notes, R help, etc.

This general approach is to fill Jinja templates with values from YAML files.
"""
import logging
from pathlib import Path

from medsldocs.metadata import Meta
from medsldocs.templates import Template, RdTemplate


def write_docs(dataset_name, path):
    """Generate dataset documentation: release notes, coverage notes, and codebook.

    Args:
        dataset_name (str): The dataverse of the dataset.
        path (Path): Destination directory for the documentation.

    Returns:
        None

    >>> write_docs('2016-precinct-president.yaml', 'output')
    """
    if isinstance(path, str):
        path = Path(path).resolve()
    meta = Meta(dataset_name)
    Template('codebook.jinja').write(meta.to_dict(), path / 'codebook-{}.md'.format(meta.dataset_name))
    Template('release_notes.jinja').write(meta.to_dict(), path / 'release-notes-{}.md'.format(meta.dataset_name))
    Template('coverage_notes.jinja').write(meta.to_dict(), path / 'coverage-notes-{}.md'.format(meta.dataset_name))
    RdTemplate('r_doc.jinja').write(meta.to_dict(), path / '{}.Rd'.format(meta.dataset_meta['r_alias']))
    logging.info('Wrote docs to {}'.format(path))


def write_precinct_readme():
    meta = Meta('2016-precinct-president.yaml')
    return Template('precinct_repo_readme.jinja').write(meta.to_dict(),
                                                        Path('output') / 'README.md'.format(meta.dataset_name))


if __name__ == '__main__':
    datasets = Path('medsldocs', 'metadata', 'dataset').glob('2016-precinct*')
    for dataset_name in datasets:
        write_docs(dataset_name.name, Path('output'))
        print('Wrote documentation for {}'.format(dataset_name.stem))
    write_precinct_readme()
    print('Wrote precinct-returns repo README.md')
