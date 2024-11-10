import requests
import xml.etree.ElementTree as ET
from lxml import etree
import pandas as pd
import sys
# =============================================================================
#
#
#
# =============================================================================
# functions to repeat (fetching and xml'ing can fail)
# =============================================================================
#
#
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
#
#
def to_xml(response):
    try:
        paper_data = etree.fromstring(response.content)
        reply_exists = paper_data.xpath('//Reply')
        success = False if reply_exists else True
    except etree.XMLSyntaxError as e:
        print(f"XML parsing failed: {e}")
        return None, False  # Return failure if parsing fails
    return paper_data, success
#
#
# =============================================================================
#
#
#
# =============================================================================
# doi functions
# =============================================================================
#
#
def get_doi_and_title_from_pmcid(pmcid, paper_data):
    doi_list = paper_data.xpath('//article-id[@pub-id-type="doi"]/text()')
    title_list = paper_data.xpath('//article-title/text()')
    
    doi = doi_list[0] if doi_list else None
    title = title_list[0] if title_list else "No title available"
    return doi, title
#
#
def fetch_references_from_crossref(doi, response):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        references = data.get('message', {}).get('reference', [])
        return references
    else:
        print(f"CrossRef API request failed. {pmcid}")
        return None
#
#
def get_references_from_pmcid(pmcid, df, response, paper_data):
    # Get DOI and Title of the source paper
    source_doi, source_title = get_doi_and_title_from_pmcid(pmcid, paper_data)
    if source_doi:
        # print(f"DOI for PMCID {pmcid}: {source_doi}")
        references = fetch_references_from_crossref(source_doi, response)
        
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
            print(f"No references found. {pmcid}")
    else:
        print(f"No DOI found for PMCID {pmcid}")
    return df
#
#
# =============================================================================
#
#
#
# =============================================================================
# scrape the papers
# =============================================================================
number_of_papers = 5000
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
df = pd.DataFrame(columns=["source_title", "referenced_title", "source_doi", "referenced_doi"])

iteration = 0
for pmcid in pmc_ids:
    
    iteration += 1
    if iteration % 50 == 0:
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
    
    df = get_references_from_pmcid(pmcid, df, response, paper_data)
    

df.to_csv('massive.csv', index=False)
    
    
    
    
    
    
    
    
    
    
 