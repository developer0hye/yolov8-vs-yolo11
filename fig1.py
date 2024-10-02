import pandas as pd
import matplotlib.pyplot as plt

# List of file paths for YOLOv11 and YOLOv8 results
file_paths_yolo11 = [
    'yolo11l-coco-results.csv',
    'yolo11m-coco-results.csv',
    'yolo11n-coco-results.csv',
    'yolo11s-coco-results.csv',
    'yolo11x-coco-results.csv'
]

file_paths_yolo8 = [
    'yolov8l-coco-results.csv',
    'yolov8m-coco-results.csv',
    'yolov8n-coco-results.csv',
    'yolov8s-coco-results.csv',
    'yolov8x-coco-results.csv'
]

# Load the CSV files into DataFrames
dfs_yolo11 = [pd.read_csv(file) for file in file_paths_yolo11]
dfs_yolo8 = [pd.read_csv(file) for file in file_paths_yolo8]

# List of YOLO model sizes for naming the plots
model_sizes = ['l', 'm', 'n', 's', 'x']

# Loop through each DataFrame for YOLOv11 and YOLOv8 and corresponding size to create separate scatter plots
for i, (size, df_yolo11, df_yolo8) in enumerate(zip(model_sizes, dfs_yolo11, dfs_yolo8)):
    plt.figure(figsize=(20, 6))
    
    # Filter out the "all" class
    df_yolo11_filtered = df_yolo11[df_yolo11['Class'] != 'all']
    df_yolo8_filtered = df_yolo8[df_yolo8['Class'] != 'all']
    
    # Count how many classes YOLOv11 performs better than YOLOv8
    better_classes_count = (df_yolo11_filtered['mAP50-95'] > df_yolo8_filtered['mAP50-95']).sum()
    
    # Plot YOLOv11 results
    plt.scatter(df_yolo11_filtered['Class'], df_yolo11_filtered['mAP50-95'], color='b', label=f'YOLOv11-{size}', marker='o')
    
    # Plot YOLOv8 results
    plt.scatter(df_yolo8_filtered['Class'], df_yolo8_filtered['mAP50-95'], color='r', label=f'YOLOv8-{size}', marker='o')
    
    # Set plot titles and labels, including the count of better performing classes
    plt.title(f'YOLOv11 vs YOLOv8 - {size} Model Comparison\nYOLOv11 performs better in {better_classes_count} out of 80 classes')
    plt.xlabel('Class')
    plt.ylabel('mAP50-95')
    plt.legend()

    # Rotate x-axis labels to vertical
    plt.xticks(rotation=90)
    
    # Display the plot
    plt.tight_layout()
    plt.savefig(f'fig1_{size}.png')