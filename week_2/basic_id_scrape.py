import requests
import xml.etree.ElementTree as ET
import sys


# fetch endpoint for PMC
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# needed to search
params = {
'db': 'pmc',           # Search within PubMed Central
'term': 'sleep[Title]',          # Query term
'retmax': 50000,      # Maximum number of results to fetch
'retmode': 'xml',      # Return data in XML format
}

# Send request to NCBI E-utilities
response = requests.get(base_url, params=params)


# Parse the XML response to get PMCID list
root = ET.fromstring(response.content)

# The function extracts all <Id> tags from the XML response, 
# which correspond to PMCIDs. It uses a list comprehension to collect these IDs:
pmc_ids = [id_tag.text for id_tag in root.findall(".//Id")]

pmc_ids.sort()
print(pmc_ids)
print(len(pmc_ids))



print('\nquestions\n')

print('\nwhat exactly is my corpus?')
print('ALL papers? or just PMC papers? or just ones in this API')
print('i need to understand this corpus a bit first')
   

check_id = '9541096'  # random paper i found online

for ID in pmc_ids:
    if ID == check_id:
        print('**found**')
        sys.exit()