import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the CSV file
path = '/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/results/citation_analysis.csv'
df = pd.read_csv(path)

# Create adjacency list
adj_list = {}
print('checkpoint 0')
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
    if s not in adj_list:
        adj_list[s] = [(c, a)]
    else:
        adj_list[s].append((c, a))

# Create graph from adjacency list
G = nx.DiGraph()

# Add edges with color based on citation analysis
for source, citations in adj_list.items():
    for cited, analysis in citations:
        color = 'green' if analysis == 1 else ('red' if analysis == -1 else 'gray')
        G.add_edge(source, cited, color=color)

# Draw the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)  # Spring layout for better readability
edges = G.edges()
colors = [G[u][v]['color'] for u, v in edges]
nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', font_color='black')
nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=colors, width=1.5, alpha=0.7)
plt.title("Citation Network Graph", fontsize=16)

# Save the graph as an SVG file
plt.axis('off')
plt.savefig('citation_network_graph.svg', format='svg')
plt.show()
