import logging
import os
import pkgutil
import re
import sys
from pathlib import Path

import attr
import jinja2


@attr.s
class Template(object):
    """Jinja-driven template for documentation.

    Args:
        filename (str): Path to Jinja template.

    Attributes:
        filename (str): Path to Jinja template.
        text (str): Text of Jinja template.
    """
    filename = attr.ib()

    def __attrs_post_init__(self):
        template_bytes = pkgutil.get_data('medsldocs', 'templates/{}'.format(self.filename))
        self.text = template_bytes.decode('utf-8')

    def write(self, data, dest='', strict=True):
        """Render a template and write the result to the disk.

        Args:
            data (dict): A mapping of template variables to values.
            dest (str): Destination path (e.g., `./release-notes.md`).
            strict (bool): Whether undefined template variables should result in an error. `True` by default because
                our templates aren't written to handle this gracefully.

        Returns:
            str: The rendered template text.
        """
        template = jinja2.Template(self.text, undefined=jinja2.StrictUndefined if strict else None)
        rendered = template.render(data)
        if dest:
            Path(dest).resolve().write_text(rendered)
        return rendered


@attr.s
class RdTemplate(Template):
    """Jinja-driven template for R documentation.

    Args:
        filename (str): Path to Jinja template.

    Attributes:
        filename (str): Path to Jinja template.
        text (str): Text of Jinja template.
    """

    def __attrs_post_init__(self):
        module_dir = os.path.dirname(sys.modules['medsldocs'].__file__)
        loader = jinja2.FileSystemLoader(searchpath=os.path.join(module_dir, 'templates'))
        self.env = jinja2.Environment(loader=loader, block_start_string='<+', block_end_string='+>',
                                      variable_start_string='<<', variable_end_string='>>', comment_start_string='<#',
                                      comment_end_string='>#')
        self.env.filters['r_alias'] = self._r_alias
        self.env.filters['format_code'] = self._format_code

    def write(self, data, dest='', strict=True):
        """Render a template and write the result to the disk.

        Args:
            data (dict): A mapping of template variables to values.
            dest (str): Destination path (e.g., `./release-notes.md`).
            strict (bool): Whether undefined template variables should result in an error. `True` by default because
                our templates aren't written to handle this gracefully.

        Returns:
            str: The rendered template text.
        """
        if strict:
            self.env.undefined = jinja2.StrictUndefined
        template = self.env.get_template(self.filename)
        rendered = template.render(data)
        if dest:
            Path(dest).resolve().write_text(rendered)
        return rendered

    @staticmethod
    def _r_alias(text: str) -> str:
        """Jinja filter for translating dataset names to valid R object names.

        Example: '2016-precinct-house' -> 'house_precinct_2016'.
        See http://jinja.pocoo.org/docs/2.10/api/#custom-filters.
        """
        if text:
            print(text)
            no_dashes = re.sub('[- ]', '_', text)
            return re.sub(r'([0-9]*)(_*)(.*)', '\g<3>\g<2>\g<1>', no_dashes)
        else:
            return ''

    @staticmethod
    def _format_code(text: str) -> str:
        """Jinja filter for translating Markdown code markup to Latex code markup.

        Example: \`inline snippet\` -> \\code\{inline snippet\}.
        See http://jinja.pocoo.org/docs/2.10/api/#custom-filters.
        """
        if text:
            return re.sub(r'`([^`]+)`', '\code{\g<1>}', text)
        else:
            return ''


@attr.s
class Readme(Template):
    """Jinja-driven template for GitHub repo READMEs.

    Args:
        filename (str): Path to Jinja template.

    Attributes:
        filename (str): Path to Jinja template.
        text (str): Text of Jinja template.
    """
    filename = attr.ib(default='precinct_repo_readme.jinja')

    def __attrs_post_init__(self):
        self.template = self.env.get_template(self.filename)

