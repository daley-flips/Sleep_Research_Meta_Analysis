import os
from lxml import etree

def apply_xslt_to_files(xslt_path, input_dir, output_dir):
    #parse the XSLT file
    with open(xslt_path, 'r') as xslt_file:
        xslt_root = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_root)
    

    os.makedirs(output_dir, exist_ok=True)
    
    # iterate through all XML files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):  # Process only XML files
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            # parse the input XML file
            with open(input_path, 'r') as input_file:
                xml_root = etree.parse(input_file)
            
            # Apply the transformation
            transformed_tree = transform(xml_root)
            
            # save the result to the output directory
            with open(output_path, 'wb') as output_file:
                output_file.write(etree.tostring(transformed_tree, pretty_print=True, xml_declaration=True, encoding="UTF-8"))
            
            print(f"Processed: {filename}")


xslt_file = "/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/transformations/citations.xsl"  
input_folder = "/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/Nature_and_Science_of_Sleep"   
output_folder = "/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/transformations/xmls" 


apply_xslt_to_files(xslt_file, input_folder, output_folder)
