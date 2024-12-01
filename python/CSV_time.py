"""
DF:
    source | cited | citation_analysis
    
    ^those are pmids

per xml file in /Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/transformations/xmls
the pmid is the name of the xml --> pmid_for_that_paper.xml

for that paper immediately grab all citations for it. so the df will grow about 50 rows at the start

source | (pmid_cited,1) | nan
source | (pmid_cited,2) | nan
.
.
.
citations are found here:
    <title>References</title>
          <ref id="b1-nss-2-213">
            <label>1</label>                                                   # <-- WE WANT THIS   
            <element-citation publication-type="journal">
              <person-group person-group-type="author">
                <name>
                  <surname>Horne</surname>
                  <given-names>J</given-names>
                </name>
              </person-group>
              <article-title>Is there a sleep debt?</article-title>
              <source>Sleep</source>
              <year>2004</year>
              <volume>27</volume>
              <fpage>1047</fpage>
              <lpage>1049</lpage>
              <pub-id pub-id-type="pmid">15532195</pub-id>                     # <-- WE WANT THIS
            </element-citation>
          </ref>
          <ref id="b2-nss-2-213">
            <label>2</label>


we need the for the information, and the number for the regex matching
regex match:
    <citation_analysis attribute="positive"> .* </citation_analysis>

    inside the .* if there is a <xref ref-type="bibr" rid="b3-nss-2-213">3</xref>
    the content inside the <xref> elements is the citation number (which we stored earlier)
    
now we can look for that number in the df and put "positive" in the citation_analysis column
"""
# =============================================================================
import pandas as pd
import os
import xml.etree.ElementTree as ET

# Columns for the DataFrame
columns = ['source', 'cited', 'citation_analysis']
data = []  # Use a list to collect rows efficiently

# Directory containing XML files
xml_dir = '/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/transformations/xmls'

index = 1

# Iterate over all XML files in the directory
for file in os.listdir(xml_dir):
    if file.endswith('.xml'):
        print(f"\nProcessing file {index}: {file}")
        index += 1
        file_path = os.path.join(xml_dir, file)
        source_pmid = os.path.basename(file).replace('.xml', '')

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Map of rid to PMIDs
        ref_id_to_pmid = {}

        # Extract <ref> elements and map rid to pmid
        for ref in root.findall(".//ref"):
            pub_id_elem = ref.find(".//pub-id[@pub-id-type='pmid']")
            if pub_id_elem is not None:
                cited_pmid = pub_id_elem.text.strip()
                rid = ref.get("id").strip().lower() if ref.get("id") else None
                if rid:
                    ref_id_to_pmid[rid] = cited_pmid

        # Flatten the XML tree to a list of elements in order
        elements_in_order = list(root.iter())

        # Initialize variables
        current_attribute = 'neither'
        unattached_attribute = None

        # Iterate over elements in order
        for elem in elements_in_order:
            if elem.tag == 'citation_analysis':
                attribute = elem.get('attribute')
                current_attribute = attribute if attribute else 'neither'

                xrefs = elem.findall(".//xref[@ref-type='bibr']")
                if xrefs:
                    for xref in xrefs:
                        rid = xref.get('rid').strip().lower() if xref.get('rid') else None
                        if rid and rid in ref_id_to_pmid:
                            cited_pmid = ref_id_to_pmid[rid]
                            data.append({
                                'source': source_pmid,
                                'cited': cited_pmid,
                                'citation_analysis': current_attribute
                            })
                            print(f"Added {current_attribute} for PMID {cited_pmid} (from citation_analysis with xref).")
                        else:
                            print(f"RID {rid} not found in references.")
                else:
                    # No xref in this citation_analysis, set unattached_attribute
                    unattached_attribute = current_attribute
                    print(f"Unattached attribute '{current_attribute}' detected.")

            elif elem.tag == 'xref' and elem.get('ref-type') == 'bibr':
                rid = elem.get('rid').strip().lower() if elem.get('rid') else None
                if rid and rid in ref_id_to_pmid:
                    cited_pmid = ref_id_to_pmid[rid]
                    if unattached_attribute:
                        attribute_to_use = unattached_attribute
                        unattached_attribute = None
                    else:
                        attribute_to_use = current_attribute
                    data.append({
                        'source': source_pmid,
                        'cited': cited_pmid,
                        'citation_analysis': attribute_to_use
                    })
                    print(f"Added {attribute_to_use} for PMID {cited_pmid} (from xref).")
                else:
                    print(f"RID {rid} not found in references.")

# Create DataFrame from collected data
df = pd.DataFrame(data, columns=columns)

# Ensure 'citation_analysis' only contains 'positive', 'negative', or 'neither'
df['citation_analysis'] = df['citation_analysis'].fillna('neither')

# Debug: Final check of global DataFrame
print(f"\nFinal DataFrame with {len(df)} rows:\n{df}")
















