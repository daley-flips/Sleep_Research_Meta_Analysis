print()
import requests
import xml.etree.ElementTree as ET
import xmltodict
import time
import sys
# =============================================================================
#
#
#
# =============================================================================
# functions to repeat (fetching and xml'ing can fail)
# =============================================================================
def fetch(pmcid):
    # fetch url
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    # data we wanna get
    params = {
        'db': 'pmc',  # scrape pmc
        'id': pmcid,  # find id
        'retmode': 'xml',  # return in xml
    }
    
    response = requests.get(url, params=params)
    
    success = True
    if response.status_code != 200: 
        # print('fetch failed')
        success = False
        # time.sleep(1)  # optionally wait before fetching again
        
    return response, success
# =============================================================================
def to_xml(response):
    
    paper_data = xmltodict.parse(response.content)
    
    success = True
    if 'Reply' in paper_data['pmc-articleset']:
        # print('xml failed')
        success = False
        # time.sleep(1)  # optionally wait before fetching again
        
    return paper_data, success
# =============================================================================
#
#
#
# =============================================================================
number_of_papers = 1
# =============================================================================
# search endpoint for PMC and parameters
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
'db': 'pmc',  # Search within PubMed Central
'term': 'sleep[Title]',  # Query term
'retmax': number_of_papers,  # Maximum number of results to fetch
'retmode': 'xml',  # Return data in XML format
}
# Send request to NCBI E-utilities
response = requests.get(base_url, params=params)

if response.status_code != 200: 
    print('search failed')  # if this fails, just run again
    sys.exit()
# =============================================================================
#
#
#
# =============================================================================
# Parse the XML response to get PMCID list
root = ET.fromstring(response.content)
# The function extracts all <Id> tags from the XML response, 
# which correspond to PMCIDs. It uses a list comprehension to collect these IDs:
pmc_ids = [id_tag.text for id_tag in root.findall(".//Id")]
print(f'found {len(pmc_ids)} papers\n')
# =============================================================================
#
#
#
# =============================================================================
# start iterating through the ids for more info
# =============================================================================

# pmc_ids = [pmc_ids[-10000]]

iteration = 0
for pmcid in pmc_ids:
    iteration += 1
    print(f'paper {iteration}/{len(pmc_ids)}')
    # print('paper id:', pmcid)
# =============================================================================
    response = None
    paper_data = None
# =============================================================================
    # fetch can fail, so we continually call it 
# =============================================================================
    success = False
    while not success:
        response, success = fetch(pmcid)
        
        # only to try convert to xml if the fetch works
        if success:
            # getting xml can also fail, so do the same thing
            paper_data, success = to_xml(response)
        print(paper_data)
# =============================================================================    
#
#
#
# =============================================================================    
# trying (hard) to get the dates    
    # Extracting the publication date from the parsed XML
    pub_dates = paper_data['pmc-articleset']['article']['front']['article-meta']['pub-date']
    
    # Initialize variables for storing publication date
    pub_year = None
    pub_month = None
    pub_day = None
    
    # Check if pub_dates is a dictionary or a list
    if isinstance(pub_dates, dict):
        # Handle if pub_dates is a dictionary
        pub_year = pub_dates.get('year', 'Unknown Year')
        pub_month = pub_dates.get('month', 'Unknown Month')
        pub_day = pub_dates.get('day', 'Unknown Day')
        
    elif isinstance(pub_dates, list):
        # Loop through the list of publication dates
        for date in pub_dates:
            # Print each date element for debugging purposes
            print(f"Date Element: {date} (type: {type(date)})")
            
            try:
                # Check if the date is a dictionary before accessing `.get()`
                if isinstance(date, dict):
                    if date.get('@pub-type') in ['epub', 'ppub', 'pmc-release', 'collection'] or date.get('@date-type') == 'pub':
                        pub_year = date.get('year', 'Unknown Year')
                        pub_month = date.get('month', 'Unknown Month')  # Some dates might not have months
                        pub_day = date.get('day', 'Unknown Day')  # Some dates might not have days
                        # Break once a valid date is found
                        break
                else:
                    print(f"Skipping non-dictionary date element: {date}")
            except Exception as e:
                print(f"Error processing publication date: {e}")
    
    # Print the extracted publication date
    print(f"Publication Date: {pub_year}-{pub_month}-{pub_day}\n")
    
        

    print(pub_year, '\n')
# =============================================================================    























