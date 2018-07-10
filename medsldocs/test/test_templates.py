from medsldocs.metadata import Meta
from medsldocs.templates import Template

meta = Meta('2016-precinct-president.yaml')


def test_read_template():
    """Template finds .jinja files in templates directory"""
    template = Template('codebook.jinja')
    assert template.text
    template = Template('coverage_notes.jinja')
    assert template.text
    template = Template('r_doc.jinja')
    assert template.text
    template = Template('precinct_repo_readme.jinja')
    assert template.text


def test_render_codebook():
    """Codebook template renders without error"""
    template = Template('codebook.jinja')
    assert template.write(meta.to_dict())


def test_render_coverage():
    """Coverage template renders without error"""
    template = Template('coverage_notes.jinja')
    assert template.write(meta.to_dict())


def test_render_r_doc():
    """Rd template renders without error"""
    template = Template('r_doc.jinja')
    assert template.write(meta.to_dict())


def test_render_readme():
    """README template renders without error"""
    template = Template('precinct_repo_readme.jinja')
    assert template.write(meta.to_dict())
