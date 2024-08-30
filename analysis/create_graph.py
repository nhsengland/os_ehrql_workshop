import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
# Make sure to use the compressed file - this is the one that'll update each time you generate the dataset
input_file = 'output/dataset.csv.gz'
df = pd.read_csv(input_file)

# Extract the relevant columns
age = df['age']
num_medications = df['num_asthma_inhaler_medications']

# Create the histogram
plt.figure(figsize=(10, 6))
plt.hist(age, bins=30, weights=num_medications, edgecolor='k')
plt.xlabel('Age')
plt.ylabel('Number of Asthma Inhaler Medications')
plt.title('Histogram of Asthma Inhaler Medications by Age')

# Save the histogram as a PNG file - and make sure to close it
output_file = 'output/age_num_inhalers_meds_histogram.png'
plt.savefig(output_file)
plt.close()
