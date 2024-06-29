# rcv

The [data/raw](data/raw) directory contains actual data retrieved from official
election sources.  The raw data files are processed into a common
format and stored in the [data/processed](data/processed/) directory.

## Development

You will need to be familiar with and have installed:

- [pipenv](https://pipenv.pypa.io/) for dependency management
- [dvc](https://dvc.org/) for storage of large raw data files
- [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) for separately
  version tracking figures for a webserver

Use the following commands to set up your local environment:

```
# Set up a local git repo
$ git clone git@github.com:chrisroat/rcv-analysis
$ cd rcv-analysis
$ pipenv install  # Install dependencies necessary for the analysis.

# Raw data is stored in Google Drive and is tracked with dvc.
$ dvc pull  # This can take some time.  Often you may want to just pull a subset of data.

# Figures are output to the rcv-analysis-figures repo in a submodule.
$ git submodule init
$ git submodule update
```

To ingest the raw data sources and output the processed data sources:

```
python alameda_ingest.py
python scc_ingest.py
python sf_ingest.py
```

In order to regenerate all the figures from processed data:

```
python analysis.py
```


## Data Sources

- Los Altos data was received via open records request with the Santa Clara County Registrar
- 2020 SF General Elections Cast Vote Record from [SF Gov](https://sfelections.sfgov.org/november-3-2020-election-results-detailed-reports)
