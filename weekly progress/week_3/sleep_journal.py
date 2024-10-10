print()
import requests
import xml.etree.ElementTree as ET
from lxml import etree
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
    try:
        # Parse the response content (assumed to be XML)
        paper_data = etree.fromstring(response.content)

        # XPath query to check if 'Reply' is present anywhere in the XML tree
        reply_exists = paper_data.xpath('//Reply')
        
        # If 'Reply' element exists, mark the process as unsuccessful
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
if __name__ == '__main__':
    number_of_papers = 10
    # =============================================================================
    # search endpoint for PMC and parameters
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
    'db': 'pmc',  # Search within PubMed Central
    'term': 'Sleep[Journal]',  # Query term
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
    iteration = 0
    for pmcid in pmc_ids:
        print()
        iteration += 1
        
        # if iteration < 3:
        #     continue
        
        print(f'paper {iteration}/{len(pmc_ids)}')
        print('paper id:', pmcid)
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
        # print(paper_data)
        # =============================================================================    
        #
        #
        #
        # =============================================================================    
        # get keywords from XPath
        # keyword elements are in <kwd>
        # =============================================================================    
        
        kwd_elements = paper_data.xpath('//kwd')

        # Extract the text content of each <kwd> element
        kwd_list = [kwd.text for kwd in kwd_elements]
        
        print(kwd_list)
        
        date_elements = paper_data.xpath('//pub-date[@pub-type="epub"]')
        
        year = paper_data.xpath('//pub-date[@pub-type="epub"]/year/text()')
        month = paper_data.xpath('//pub-date[@pub-type="epub"]/month/text()')
        day = paper_data.xpath('//pub-date[@pub-type="epub"]/day/text()')
        
        print(f"Year: {year}, Month: {month}, Day: {day}")
                
        
            
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
