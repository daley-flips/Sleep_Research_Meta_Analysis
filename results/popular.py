import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
path = '/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/results/citation_analysis.csv'
df = pd.read_csv(path)

# Filter only negatives
negatives_df = df[df['citation_analysis'] == 'negative']

# Count the number of negatives per source
negative_counts = negatives_df['source'].value_counts()

# Get the top 5 most negative papers
top_negatives = negative_counts.nlargest(5)

# Calculate the total negatives for 'Other'
other_negatives = negative_counts.sum() - top_negatives.sum()

# Prepare data for the pie chart
labels = top_negatives.index.tolist() + ['Other']
sizes = top_negatives.tolist() + [other_negatives]
percentages = [(size / sum(sizes)) * 100 for size in sizes]

# Create pie chart
plt.figure(figsize=(10, 7))
plt.pie(
    sizes, 
    labels=[f"{label} ({p:.1f}%)" for label, p in zip(labels, percentages)], 
    autopct='%1.1f%%', 
    startangle=140
)
plt.title('Negative Citation Distribution')
plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

# Save to SVG
output_path = '/Users/daleyfraser/Documents/cs/classes/INFSCI_0013/Sleep_Research_Meta_Analysis/results/negative_pie_chart.svg'
plt.savefig(output_path, format='svg')

print(f"Pie chart saved to {output_path}")
