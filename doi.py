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
    with open(INPUT_FILE, "r") as infile:
        urls = [line.strip() for line in infile if line.strip()]

    with open(OUTPUT_FILE, "w") as outfile:
        for url in urls:
            doi = extract_doi(url)
            if doi:
                outfile.write(f"{url} -> https://doi.org/{doi}\n")
            else:
                outfile.write(f"{url} -> DOI not found\n")

    print(f"Results written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
