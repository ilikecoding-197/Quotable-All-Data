"""
update.py - update quotes, authors, and tags.
"""

# Imports
from requests import get
from pprint import pprint
import json
from os.path import abspath, dirname
from os import chdir

# Go to the directory containing this file.
chdir(dirname(abspath(__file__)))

quotes_url = "https://api.quotable.io/quotes?limit=999" # URL for getting all quotes
authors_url = "https://api.quotable.io/authors?limit=999" # URL for getting all authors
tags_url = "https://api.quotable.io/tags" # URL for getting all tags

def get_quotes():
    """
    Get a list of all quotes from the quotable database.
    """

    # Get the quotes
    pages = 1 # Start with 1 pages, whoich will allow us to get the number of pages.
    page = 1 # Current page.
    meta = {} # Metadata for the quotes.
    quotes = {"quotes": []} # Quotes.

    while page <= pages:
        # Get data from the quotable API.
        data = get(quotes_url + f"&page={page}").json()
        if page == 1: # First page
            # Get the number of pages and update the pages variable.
            pages = data["totalPages"]

            # Get metadata.
            meta["totalQuotes"] = data["totalCount"]
        
        # Convert the quotes data returned from the quotable API to a list formatted for our purposes.
        for quote in data["results"]:
            quotes["quotes"].append({
                "id": quote["_id"],
                "quote": quote["content"],
                "author": quote["author"],
                "authorSlug": quote["authorSlug"],
                "length": quote["length"],
                "tags": quote["tags"]
            })
        

        page += 1 # Increment the page number.

    # Add the metadata to the quotes.
    quotes["meta"] = meta

    # Return the quotes.
    return quotes

def get_authors():
    """
    Get a list of all authors from the quotable database.
    """

    pages = 1 # Start with 1 pages, whoich will allow us to get the number of pages.
    page = 1 # Current page.
    meta = {} # Metadata for the authors.
    authors = {"authors": []} # Authors.

    while page <= pages:
        # Get data from the quotable API.
        data = get(authors_url + f"&page={page}").json()
        if page == 1: # First page
            # Get the number of pages and update the pages variable.
            pages = data["totalPages"]

            # Get metadata.
            meta["totalAuthors"] = data["totalCount"]
        
        # Convert the authors data returned from the quotable API to a list formatted for our purposes.
        for author in data["results"]:
            authors["authors"].append({
                "id": author["_id"],
                "bio": author["bio"],
                "desc": author["description"],
                "link": author["link"],
                "name": author["name"],
                "slug": author["slug"],
                "quoteCount": author["quoteCount"],
            })
        

        page += 1 # Increment the page number.

    # Add the metadata to the authors.
    authors["meta"] = meta

    # Return the quotes.
    return authors

def get_tags():
    """
    Get all tags from the quotable database.
    """

    # Get data from the quotable API.
    data = get(tags_url).json()

    # Return the tags.
    return {
        "count": len(data),
        "tags": data
    }

def main():
    """
    Main function.
    """

    print("Updating data...")

    # Get quotes.
    print("Getting quotes...")
    quotes = get_quotes() # Get quotes.

    # Get the extra quotes.
    with open("../extra/extra_quotes.json", mode="r") as f:
        extra_quotes = json.load(f)
    
    # Get authors
    print("Getting authors...")
    authors = get_authors() # Get authors.

    # Get the extra authors.
    with open("../extra/extra_authors.json", mode="r") as f:
        extra_authors = json.load(f)

    # Get tags
    print("Getting tags...")
    tags = get_tags() # Get tags.

    # Get the extra tags.
    with open("../extra/extra_tags.json", mode="r") as f:
        extra_tags = json.load(f)

    
    # Get the old quote data.
    with open("../data/quotes.json", mode="r") as f:
        old_quotes = json.load(f)

    # Get the old author data.
    with open("../data/authors.json", mode="r") as f:
        old_authors = json.load(f)

    # Get the old tag data.
    with open("../data/tags.json", mode="r") as f:
        old_tags = json.load(f)


    # Check if we have any differences.
    if any([
        old_quotes != {"quotes": quotes, "meta": quotes["meta"]},
        old_authors != {"authors": authors, "meta": authors["meta"]},
        old_tags != {"tags": tags, "count": tags["count"]}
    ]):
        print("New data!")
        # Write the new data.
        with open("../data/quotes.json", mode="w") as f:
            json.dump(quotes, f, indent=4)

        with open("../data/authors.json", mode="w") as f:
            json.dump(authors, f, indent=4)

        with open("../data/tags.json", mode="w") as f:
            json.dump(tags, f, indent=4)

        # Get the old version.
        with open("../data/version.txt", "r") as f:
            old_verson = int(f.read())
        
        # Update the version.
        with open("../data/version.txt", "w") as f:
            f.write(str(old_verson + 1))

        print("Updated!") # Please, I pray, work.

if __name__ == "__main__":
    main()
