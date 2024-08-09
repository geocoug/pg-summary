# pg_summary

[![ci/cd](https://github.com/geocoug/pg-summary/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/geocoug/pg-summary/actions/workflows/ci-cd.yaml)
[![Documentation Status](https://readthedocs.org/projects/pg-summary/badge/?version=latest)](https://pg-summary.readthedocs.io/en/latest/?badge=latest)
[![PyPI Latest Release](https://img.shields.io/pypi/v/pg-summary.svg)](https://pypi.org/project/pg-summary/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/pg-summary.svg?label=pypi%20downloads)](https://pypi.org/project/pg-summary/)
[![Python Version Support](https://img.shields.io/pypi/pyversions/pg-summary.svg)](https://pypi.org/project/pg-summary/)

Create a summary of unique values for each column in a Postgres table or view and summarize results in an Excel workbook.

![Output](https://raw.githubusercontent.com/geocoug/pg-summary/main/output.png)

## Installation

You can install **pg_summary** via pip from PyPI:

```bash
pip install pg-summary
```

There is also a Docker image available on the GitHub Container Registry:

```bash
docker pull ghcr.io/geocoug/pg-summary:latest
```

## Usage

The following example demonstrates how to use **pg_summary** to summarize a Postgres table. By default, the output is an Excel file with one sheet. Each column in the sheet will summarize a column in the Postgres table with the unique values, number of unique values, number of null values, data type, and the column name.

Each of the examples below will produce the exact same output.

### Python

```python
from pg_summary import PgSummary

PgSummary(
    host="localhost",
    port=5432,
    database="mydb",
    user="myuser",
    table_or_view="mytable",
    schema="staging",
).summarize()
```

### Command Line

```bash
 pg_summary -v localhost -u myuser -d mydb -t mytable -s staging
```

### Docker

```bash
docker run --rm -v $(pwd):/data ghcr.io/geocoug/pg-summary:latest -v localhost -u myuser -d mydb -t mytable -s staging
```
