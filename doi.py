"""
import requests
from bs4 import BeautifulSoup

# Output filename
OUTPUT_FILE = "doi_links.txt"
INPUT_FILE = "input.txt"  # change this


def extract_doi(url):
    #Fetches the PubMed page at `url` and returns the DOI if found.
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Look for meta tag with DOI
    meta = soup.find("meta", attrs={"name": "citation_doi"})
    if meta and meta.get("content"):
        return meta["content"]

    # Fallback: find any doi.org link
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "doi.org" in href:
            return href.split("doi.org/")[-1]

    return None


def main():
    urls = []
    with open(INPUT_FILE, "r") as a:
        for line in a:
            url = line.strip()
            if url:
                urls.append(url)

    # Write results to file
    with open(OUTPUT_FILE, "w") as outfile:
        for url in urls:
            doi = extract_doi(urls)
            if doi:
                link = f"https://doi.org/{doi}"
                outfile.write(f"{link}\n")
            else:
                outfile.write(f"{url} -> DOI not found\n")

    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
"""

#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

INPUT_FILE = "input.txt"
OUTPUT_FILE = "doi_links.txt"


def extract_doi(url: str) -> str | None:
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    meta = soup.find("meta", attrs={"name": "citation_doi"})
    if isinstance(meta, Tag) and meta.get("content"):
        return meta["content"]

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "doi.org/" in href:
            return href.split("doi.org/")[-1]
    return None


def main():
    # 1) Read URLs from the file
    with open(INPUT_FILE, "r") as infile:
        urls = [line.strip() for line in infile if line.strip()]

    # 2) Process each URL one by one
    with open(OUTPUT_FILE, "w") as outfile:
        for url in urls:
            doi = extract_doi(url)
            if doi:
                outfile.write(f"{url} -> https://doi.org/{doi}\n")
            else:
                outfile.write(f"{url} -> DOI not found\n")

    print(f"✅ Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
