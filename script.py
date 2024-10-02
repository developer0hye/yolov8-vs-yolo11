import os
import re
import pandas as pd

# Define model prefixes and model variants
model_prefixes = ['yolov8', 'yolo11']
model_variants = ['n', 's', 'm', 'l', 'x']

# Step 1: Run YOLO validation for different models and store logs
for model_prefix in model_prefixes:
    for variant in model_variants:
        model_name = f'{model_prefix}{variant}'
        log_file = f'{model_name}-coco-results.txt'
        os.system(f'yolo val data=coco.yaml model={model_name}.pt >> {log_file}')

# Collect all log files
log_files = [f'{model_prefix}{variant}-coco-results.txt' for model_prefix in model_prefixes for variant in model_variants]

# Define the regex pattern for extracting data
pattern = r"\s*(\w+[\s\w]*)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"

def process_log_file(log_file_path):
    # Initialize lists to store data
    classes = []
    images = []
    instances = []
    p_scores = []
    r_scores = []
    map50_scores = []
    map5095_scores = []

    # Read the log file and extract relevant data
    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                classes.append(match.group(1).strip())
                images.append(int(match.group(2)))
                instances.append(int(match.group(3)))
                p_scores.append(float(match.group(4)))
                r_scores.append(float(match.group(5)))
                map50_scores.append(float(match.group(6)))
                map5095_scores.append(float(match.group(7)))

    # Create a DataFrame with the extracted data
    df = pd.DataFrame({
        "Class": classes,
        "Images": images,
        "Instances": instances,
        "P": p_scores,
        "R": r_scores,
        "mAP50": map50_scores,
        "mAP50-95": map5095_scores
    })

    # Save the DataFrame as a CSV file
    csv_file_path = log_file_path.replace('.txt', '.csv')
    df.to_csv(csv_file_path, index=False)

    print(f"Results saved to {csv_file_path}")

# Step 2: Extract information from the log files and create CSVs
for log_file_path in log_files:
    process_log_file(log_file_path)
