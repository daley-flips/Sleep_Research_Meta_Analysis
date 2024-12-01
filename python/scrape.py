import requests
import xml.etree.ElementTree as ET
import xmltodict
import sys
import time
# =============================================================================
#
#
#
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
#
#
#
# =============================================================================
# Function to fetch full paper details from PubMed Central using PMCID
# =============================================================================
def fetch_paper_details(pmcid, fetch_attempts):
# =============================================================================
# same as before
# =============================================================================
    # fetch endpoint
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pmc',  # scrape pmc
        'id': pmcid,  # find id
        'retmode': 'xml',  # return in xml
    }
# =============================================================================
# fetches may fail, so do it while loop
# =============================================================================
    fetches = 0
    success = False
    delay = 1
    while fetches < fetch_attempts and not success:
        fetches += 1
# =============================================================================
        response = requests.get(url, params=params)
# =============================================================================
        if response.status_code == 200:  # 200 is success code
            
            success = True
        
            # Parse the XML response for paper details
            paper_data = xmltodict.parse(response.content)
            
            # print(paper_data)
            
            if 'Reply' in paper_data['pmc-articleset']:
                # If there is an error in the reply, retry
                # error_message = paper_data['pmc-articleset']['Reply'].get('@error', 'Unknown error')
                # print(f"Error fetching paper {pmcid}: {error_message}")
                
                # print('**AAAAAAAAAA**')
                time.sleep(delay)  # delay before retrying
                success = False
                print(fetches)
                
                # sys.exit()
                continue
            else:
                success = True
                
            
            
            
            
            
            
            
            # article = paper_data['pmc-articleset'].get('article')
    
            # title = article['front']['article-meta']['title-group']['article-title']
            
            
            # # Handle cases where abstract might not be available
            # abstract = article['front']['article-meta'].get('abstract', {}).get('p', 'No abstract available.')
            
            # # Fetch other metadata such as authors
            # authors = article['front']['article-meta'].get('contrib-group', {}).get('contrib', [])
            # if isinstance(authors, dict):
            #     authors = [authors]  # Ensure authors is a list
            # author_list = []
            # for author in authors:
            #     if 'name' in author:
            #         surname = author['name'].get('surname', '')
            #         given_names = author['name'].get('given-names', '')
            #         name = f"{surname} {given_names}"
            #         author_list.append(name.strip())
            
            # return {
            #     'PMCID': pmcid,
            #     'Title': title,
            #     'Abstract': abstract,
            #     'Authors': author_list
            # }
        else:
            # print(f"Error fetching details for PMCID: {pmcid}")
            # print('**EEEEEEE**')
            # sys.exit()
            success = False
            time.sleep(delay)  # delay before retrying
            print(fetches)
            
            # sys.exit()
            continue
# =============================================================================
#
#
#
# =============================================================================
# Main function to scrape sleep research papers
# =============================================================================
def scrape_sleep_papers():
    pmc_ids = get_sleep_research_papers(retmax=10)
    # pmc_ids = get_sleep_research_papers()  # defualt param will search for 1mil papers 
    # but caps out around 40k
    
    # print(pmc_ids)
    # print(len(pmc_ids))
    
    # sys.exit()
    
    fetch_attempts = 20
    
    for pmcid in pmc_ids:
        paper_details = fetch_paper_details(pmcid, fetch_attempts)
        if paper_details:
            print("\n----- Paper Details -----")
            print(f"PMCID: {paper_details['PMCID']}")
            print(f"Title: {paper_details['Title']}")
            print(f"Abstract: {paper_details['Abstract']}")
            print(f"Authors: {', '.join(paper_details['Authors'])}")
# =============================================================================
#
#
#
# =============================================================================
# Call main function
scrape_sleep_papers()
