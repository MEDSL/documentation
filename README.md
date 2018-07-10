# documentation

This repo holds a Python module for generating MEDSL dataset documentation.
Specifically, four files for each dataset:

* Release notes
* Coverage notes
* Codebook
* R documentation

The module also generates the `README.md` for the
[precinct-returns](https://github.com/MEDSL/precinct-returns) repo.

The approach is to fill [Jinja2](http://jinja.pocoo.org/docs) templates with
metadata defined in YAML.

Organization:

```
├── medsldocs           # The module (Python)
│   ├── metadata        # Data about data (YAML)
│   │   ├── candidates  # ... candidates
│   │   ├── dataset     # ... datasets
│   │   │   └── common  # 
│   │   └── elections   # ... offices and districts
│   ├── templates       # Templates (Jinja2)
│   └── test            # Test suite (Python)
└── output              # Generated documentation (Markdown, Rd)
```

Run:

```{bash}
python -m medsldocs
```

