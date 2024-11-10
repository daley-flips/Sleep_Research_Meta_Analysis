"""
/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/xml_papers/
"""
import requests
import xml.etree.ElementTree as ET
from lxml import etree
import sys
# =============================================================================
#
#
#
# =============================================================================
# functions to repeat (fetching and xml'ing can fail)
# =============================================================================
def fetch(pmcid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pmc',  # scrape pmc
        'id': pmcid,  # find id
        'retmode': 'xml',  # return in xml
    }
    response = requests.get(url, params=params)
    success = True
    if response.status_code != 200: 
        success = False
    return response, success


def to_xml(response):
    try:
        paper_data = etree.fromstring(response.content)
        reply_exists = paper_data.xpath('//Reply')
        success = False if reply_exists else True
    except etree.XMLSyntaxError as e:
        print(f"XML parsing failed: {e}")
        return None, False  # Return failure if parsing fails
    return paper_data, success
# =============================================================================
#
#
#
# =============================================================================
# scrape the papers
# =============================================================================
number_of_papers = 1
# search endpoint for PMC and parameters
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
'db': 'pmc',  # Search within PubMed Central
'term': 'Sleep[Journal]',  # Query term
'retmax': number_of_papers,  # Maximum number of results to fetch
'retmode': 'xml',  # Return data in XML format
}
response = requests.get(base_url, params=params)
if response.status_code != 200: 
    print('search failed')  # if this fails, just run again
    sys.exit()
root = ET.fromstring(response.content)
pmc_ids = [id_tag.text for id_tag in root.findall(".//Id")]
print(f'found {len(pmc_ids)} papers\n')
# =============================================================================
# start iterating through the ids for more info
# =============================================================================
iteration = 0
for pmcid in pmc_ids:
    
    iteration += 1
    print(f'paper {iteration}/{len(pmc_ids)}')
    print('paper id:', pmcid)
    # =============================================================================
    response = None
    paper_data = None
    success = False
    while not success:
        response, success = fetch(pmcid)
        if success:
            paper_data, success = to_xml(response)
    
    # Define folder path and ensure the filename is unique for each paper
    folder = '/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/xml_papers/'
    file_path = f"{folder}{pmcid}.xml"  # Use pmcid as the filename
    
    # Write XML content to the specified file
    with open(file_path, 'wb') as file:
        file.write(etree.tostring(paper_data, pretty_print=True, encoding="UTF-8"))
    print(f"Saved XML for paper ID {pmcid} to {file_path}")

        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 