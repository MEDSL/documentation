"""
Load and validate datapackage schema.
"""

from pathlib import Path
import yaml

yaml.load(Path('schema/core.yaml').read_text())
