"""
Mission: Read the file with all links into a list. Make requests to the links in that list and search for
PMIDs which will be added into a final list or .txt file
"""
import requests
from bs4 import BeautifulSoup

#Initialize a set for seen PMIDs
seen_pmids = []

# Read all lines from the text file containing XML links
with open("test_link_to_xml.txt", "r") as file:
  xml_links = [line.strip() for line in file]

# Write to a new output file
with open("PMID_output.txt", "w") as output:
    for link in xml_links:
        try:
            # Download the XML content
            response = requests.get(link)
            response.raise_for_status() # Raise exception for unsuccessful request

            # Parse the XML content
            parse = BeautifulSoup(response.content, features="xml")

            # Find all <Publication> tags containing PMID attributes
            publications = parse.find_all("Publication")
            for pub in publications:
                pmid_tag = pub.find("Pubmed", attrs={"pmid" : True})
                if pmid_tag and pmid_tag["pmid"] not in seen_pmids:
                    # Extract the PMID value and add to seen PMID list
                    seen_pmids.append(pmid_tag["pmid"])
                    output.write(f"{pmid_tag['pmid']}\n") # Write to output file
                    print(f"PMID extracted from {link}: {pmid_tag['pmid']}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {link}: {e}") 
