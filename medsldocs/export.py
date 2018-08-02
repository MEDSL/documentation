"""
Export metadata to disk.
"""
import pandas as pd
from medsldocs.metadata import Meta

def to_csv():
    pass

def main():
    meta = Meta('2016-precinct-house.yaml')
    pd.DataFrame(meta.variable_meta)
