import os

# Directory containing the XML files
xml_directory = "../../Nature_and_Science_of_Sleep"

# Output file
output_file = "formatting.xhtml"

# Template for the XHTML file
template = """<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Corpus</title>
    <link rel="stylesheet" href="styles.css" />
</head>
<body>
    <div class="container">
        <div id="nav-container">
            <div id="navigation">
                <h2>Tabs</h2>
                <ul>
                    <li><a href="../index.html">Home</a></li>
                    <li><a href="methods.xhtml">Methods</a></li>
                    <li><a href="corpus.xhtml">Corpus</a></li>
                </ul>
            </div>
        </div>
        <div id="content">
            <h1>Corpus Files</h1>
            <ul>
{links}
            </ul>
        </div>
    </div>
</body>
</html>
"""

# Generate list of links
links = []
for filename in sorted(os.listdir(xml_directory)):
    if filename.endswith(".xml"):
        # Adjust file path to contain only one `..`
        relative_path = f"../Nature_and_Science_of_Sleep/{filename}"
        link = f'                <li><a href="{relative_path}">{filename}</a></li>'
        links.append(link)

# Join all links into a single string
links_string = "\n".join(links)

# Create the full XHTML content
xhtml_content = template.format(links=links_string)

# Write to the output file
with open(output_file, "w") as f:
    f.write(xhtml_content)

print(f"Generated {output_file} with {len(links)} XML file links!")
