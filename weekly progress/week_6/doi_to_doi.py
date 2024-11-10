import requests
from lxml import etree
import pandas as pd
import xml.etree.ElementTree as ET
import sys

# Initialize the DataFrame with the required columns
df = pd.DataFrame(columns=["source_title", "referenced_title", "source_doi", "referenced_doi"])

# =============================================================================
# Fetch paper XML from PubMed Central by PMCID
# =============================================================================
def fetch(pmcid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pmc',
        'id': pmcid,
        'retmode': 'xml',
    }
    response = requests.get(url, params=params)
    success = response.status_code == 200
    return response, success

# =============================================================================
# Convert response content to XML
# =============================================================================
def to_xml(response):
    try:
        paper_data = etree.fromstring(response.content)
        reply_exists = paper_data.xpath('//Reply')
        success = not bool(reply_exists)
    except etree.XMLSyntaxError as e:
        print(f"XML parsing failed: {e}")
        return None, False
    return paper_data, success

# =============================================================================
# Get DOI and Title for a paper by PMCID
# =============================================================================
def get_doi_and_title_from_pmcid(pmcid):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pmc',
        'id': pmcid,
        'retmode': 'xml',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        paper_data = etree.fromstring(response.content)
        doi_list = paper_data.xpath('//article-id[@pub-id-type="doi"]/text()')
        title_list = paper_data.xpath('//article-title/text()')
        
        doi = doi_list[0] if doi_list else None
        title = title_list[0] if title_list else "No title available"
        return doi, title
    else:
        print(f"Failed to fetch data for PMCID {pmcid}")
        get_doi_and_title_from_pmcid(pmcid)

# =============================================================================
# Fetch references for a paper by DOI from CrossRef
# =============================================================================
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

# =============================================================================
# Process references and add them to the DataFrame
# =============================================================================
def get_references_from_pmcid(pmcid, df):
    # Get DOI and Title of the source paper
    source_doi, source_title = get_doi_and_title_from_pmcid(pmcid)
    if source_doi:
        print(f"DOI for PMCID {pmcid}: {source_doi}")
        references = fetch_references_from_crossref(source_doi)
        
        if references:
            for ref in references:
                # Get details for the referenced paper
                referenced_title = ref.get('article-title', 'No title available')
                referenced_doi = ref.get('DOI', 'No DOI')
                
                # Add a new row to the DataFrame
                df = pd.concat([df, pd.DataFrame({
                    "source_title": [source_title],
                    "referenced_title": [referenced_title],
                    "source_doi": [source_doi],
                    "referenced_doi": [referenced_doi]
                })], ignore_index=True)
        else:
            print("No references found.")
    else:
        print(f"No DOI found for PMCID {pmcid}")
    return df

# =============================================================================
# Main execution
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
    
    df = get_references_from_pmcid(pmcid, df)

df.to_csv('test.csv', index=False)