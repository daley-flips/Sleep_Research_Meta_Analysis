import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
path = '/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/results/citation_analysis.csv'  # Adjust the path if needed
df = pd.read_csv(path)

# Create adjacency list and graph
adj_list = {}
G = nx.DiGraph()

# Create the adjacency list and populate the graph
for idx, row in df.iterrows():
    s = row['source']
    c = row['cited']
    a = row['citation_analysis']
    if a == 'positive':
        a = 1
    elif a == 'negative':
        a = -1
    else:
        a = 0
    G.add_edge(s, c, weight=a)

# Identify node degree centrality
degree_centrality = nx.degree_centrality(G)

# Sort nodes by degree centrality and select the top N (e.g., top 1% of nodes)
N = int(0.01 * len(degree_centrality))  # Top 1% of nodes by degree centrality
top_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:N]

# Filter edges: only include edges where both source and target nodes are in the top nodes
edges_to_show = [(u, v) for u, v in G.edges() if u in top_nodes and v in top_nodes]

# Create a subgraph with only the filtered edges and top nodes
H = G.edge_subgraph(edges_to_show).copy()

# Debugging output: Check if we have any nodes and edges in the filtered graph
print(f"Number of nodes in filtered graph: {len(H.nodes())}")
print(f"Number of edges in filtered graph: {len(H.edges())}")

if len(H.nodes()) == 0 or len(H.edges()) == 0:
    print("No nodes or edges to display. Try adjusting the filtering criteria.")

# Color positive edges green, negative edges red
edge_colors = []
for u, v, data in H.edges(data=True):
    if data['weight'] == 1:
        edge_colors.append('green')  # Positive citation
    elif data['weight'] == -1:
        edge_colors.append('red')    # Negative citation
    else:
        edge_colors.append('gray')   # Neutral citation

# Layout for visualization (using a force-directed layout with adjusted k)
pos = nx.spring_layout(H, k=0.3, iterations=100)  # Adjust 'k' for better spacing between nodes

# Plot the graph
plt.figure(figsize=(12, 12))

# Draw nodes with important nodes in larger size and different color
node_sizes = [500 * degree_centrality[node] for node in H.nodes()]  # Reduce node size based on degree centrality
nx.draw_networkx_nodes(H, pos, node_size=node_sizes, node_color=['orange' if node in top_nodes else 'lightblue' for node in H.nodes()])

# Draw edges with color-coding based on the type of citation (positive/negative)
nx.draw_networkx_edges(H, pos, edge_color=edge_colors, alpha=0.7, width=2)

# Draw labels for nodes
nx.draw_networkx_labels(H, pos, font_size=8, font_color="black")

# Remove axis for better presentation
plt.axis('off')

# Save to SVG
plt.savefig("/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/results/filtered_graph_output.svg", format="SVG")
plt.show()
