
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Path to the CSV file containing PMIDs
csv_file_path = r"C:\Users\kad2240\Documents\pmid.csv"

# Read PMIDs from the CSV file using pandas and store them in a set for quick lookup
pmid_df = pd.read_csv(csv_file_path)
pmid_set = set(pmid_df['PMID'].astype(str).str.strip())  # Adjust the column name as necessary
print(pmid_set)


# Read all lines from the text file containing XML links
with open("link_to_all_xml_files.txt", "r") as file:
  xml_links = [line.strip() for line in file]

for link in xml_links:
    try:
        # Download the XML content
        response = requests.get(link)
        response.raise_for_status()  # Raise exception for unsuccessful request

        # Parse the XML content using lxml
        parse = BeautifulSoup(response.content, 'lxml-xml')

        # Find all <Publication> tags containing PMID attributes
        publications = parse.find_all("Publication")
        for pub in publications:
            pmid_tag = pub.find("Pubmed", attrs={"pmid": True})
            if pmid_tag is not None and pmid_tag["pmid"] in pmid_set:
                print(f"PMID {pmid_tag['pmid']} found in both XML and CSV")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {link}: {e}")