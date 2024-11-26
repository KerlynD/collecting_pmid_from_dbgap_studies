"""
Mission: Create a script to automatically collect all links to .xml files
"""
import requests
from bs4 import BeautifulSoup

#Read file path to GapExchange XML file
file_input = "Studies_Table_Of_Contents - Copy.xml"

#Open the file
with open(file_input, "r") as file:
    file_lines = file.readlines()

#Process of retrieving links
with open("link_to_all_xml_files.txt", "w") as output_file:
    for line in file_lines:
        if "GapExchange" in line:
            output_file.write(line)