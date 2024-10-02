import requests
import xml.etree.ElementTree as ET
import xmltodict
import sys
import time

# =============================================================================
# get PMCIDs
# params
# term means papers with sleep in the title
# retmax is the max IDs it will return
# =============================================================================
def get_sleep_research_papers(term="sleep[Title]", retmax=50000):
    # fetch endpoint for PMC
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # needed to search
    params = {
        'db': 'pmc',           # Search within PubMed Central
        'term': term,          # Query term
        'retmax': retmax,      # Maximum number of results to fetch
        'retmode': 'xml',      # Return data in XML format
    }
    # Send request to NCBI E-utilities
    response = requests.get(base_url, params=params)
    if response.status_code == 200:  # code 200 means success
        # Parse the XML response to get PMCID list
        root = ET.fromstring(response.content)

        # The function extracts all <Id> tags from the XML response, 
        # which correspond to PMCIDs. It uses a list comprehension to collect these IDs:
        pmc_ids = [id_tag.text for id_tag in root.findall(".//Id")]
        print(f"Found {len(pmc_ids)} articles for '{term}'.")
        return pmc_ids
    else:
        print("Error fetching data from PubMed Central.")
        sys.exit()

# =============================================================================
# Function to fetch full paper details from PubMed Central using PMCID
# =============================================================================
def fetch_paper_details(pmcid):
    # fetch endpoint
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pmc',  # scrape pmc
        'id': pmcid,  # find id
        'retmode': 'xml',  # return in xml
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:  # 200 is success code
        # Parse the XML response for paper details
        paper_data = xmltodict.parse(response.content)
        print(paper_data)
        
        # Extract the year of the paper
        try:
            # Check where the publication date is located in the XML structure
            pub_dates = paper_data['pmc-articleset']['article']['front']['article-meta']['pub-date']
            # Find the year of publication
            if isinstance(pub_dates, list):  # sometimes there are multiple publication dates
                for pub_date in pub_dates:
                    if pub_date.get('@pub-type') in ['epub', 'ppub']:  # electronic or print publication
                        year = pub_date.get('year', 'Unknown')
                        return year
            else:
                year = pub_dates.get('year', 'Unknown')
                return year
        except KeyError:
            print(f"Error fetching the year for PMCID: {pmcid}")
            return None
    else:
        print(f"Error fetching details for PMCID: {pmcid}")
        return None

# =============================================================================
# Main function to scrape sleep research papers and fetch publication years
# =============================================================================
def scrape_sleep_papers():
    pmc_ids = get_sleep_research_papers(retmax=10)
    
    for pmcid in pmc_ids:
        year = fetch_paper_details(pmcid)
        if year:
            print(f"PMCID: {pmcid}, Year: {year}")

# =============================================================================
# Call main function
scrape_sleep_papers()
