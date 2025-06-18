This script extracts DOIs (Digital Object Identifiers) from a list of PubMed article URLs and writes them to an output file.

## Features

- Accepts a list of URLs from `input.txt`
- Extracts DOI from:
  - `<meta name="citation_doi" content="...">` tag, if present
  - Any `<a>` tag containing a `doi.org/` link
- Outputs clickable DOI links in `https://doi.org/...` format
- Logs unfound DOIs clearly

## Requirements

- Python 3.10+
- `requests` and `beautifulsoup4` libraries

Install dependencies (if needed):
```bash
pip install requests beautifulsoup4
