from quality import compute_quality_for_corpus
from simplefilters import  (
    NaiveFilter,
    ParanoidFilter,
    RandomFilter)
import os


# Define paths for training and testing datasets
train_data_path = 'path/1/'
test_data_path = 'path/2/'

# Initialize the chosen filter
filter = RandomFilter()

# Train the filter on the training dataset
filter.train(train_data_path)

# Test the filter on the testing dataset
filter.test(test_data_path)

# Compute quality of predictions
quality = compute_quality_for_corpus(test_data_path)

# Print the quality
print(f"Prediction quality: {quality}")

# Remove the prediction file from the test dataset
prediction_file = os.path.join(test_data_path, '!prediction.txt')
if os.path.exists(prediction_file):
    os.remove(prediction_file)
    print(f"Removed file: {prediction_file}")
else:
    print("Prediction file not found.")
