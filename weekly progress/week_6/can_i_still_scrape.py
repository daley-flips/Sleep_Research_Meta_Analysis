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


def get_doi_from_pmcid(pmcid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pmc',  # Access PubMed Central
        'id': pmcid,  # Use PMCID for retrieval
        'retmode': 'xml',  # Get XML response
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        paper_data = etree.fromstring(response.content)
        doi_list = paper_data.xpath('//article-id[@pub-id-type="doi"]/text()')
        if doi_list:
            return doi_list[0]
        else:
            print("DOI not found in the response.")
            return None
    else:
        print(f"Failed to fetch data for PMCID {pmcid}")
        return None

# Step 2: Fetch references from CrossRef using DOI
def fetch_references_from_crossref(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        references = data.get('message', {}).get('reference', [])
        return references
    else:
        print("CrossRef API request failed.")
        return None
    
    
def get_pmcid_from_doi(doi):
    """Convert DOI to PMCID using PubMed Central API."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pmc',
        'term': doi,
        'retmode': 'xml',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        tree = etree.fromstring(response.content)
        pmcid_list = tree.xpath('//IdList/Id')
        return pmcid_list[0].text if pmcid_list else None
    return None


# Step 3: Combine both steps to fetch references by PMCID
def get_references_from_pmcid(pmcid):
    doi = get_doi_from_pmcid(pmcid)
    if doi:
        print(f"DOI for PMCID {pmcid}: {doi}")
        references = fetch_references_from_crossref(doi)
        
        if references:
            print("References:")
            for i, ref in enumerate(references, 1):
                title = ref.get('article-title', 'No title available')
                author = ref.get('author', 'No author')
                journal = ref.get('journal-title', 'No journal title')
                volume = ref.get('volume', 'No volume')
                year = ref.get('year', 'No year')
                doi = ref.get('DOI', 'No DOI')
                
                ref_pmcid = get_pmcid_from_doi(doi)

                # Print each reference in a structured format
                print(f"{i}. {title}")
                print(f"   Author: {author}")
                print(f"   Journal: {journal}, Volume: {volume}, Year: {year}")
                print(f"   DOI: {doi}\n")
                print(f"   PMCID: {ref_pmcid}\n")
        else:
            print("No references found.")
    else:
        print(f"No DOI found for PMCID {pmcid}")


# =============================================================================
#
#
#
# =============================================================================
pmcid = 11494376
print('paper id:', pmcid)
# =============================================================================
response = None
paper_data = None
success = False
while not success:
    response, success = fetch(pmcid)
    if success:
        paper_data, success = to_xml(response)

print(paper_data)

get_references_from_pmcid(pmcid)



    
    
    
    
    
    
    
    
    
    
 