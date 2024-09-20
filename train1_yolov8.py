#this code makes the training set for train and val by splitting it into 80% and 20% and making the seperate folders for each train folder and val folder under which u will get images and txt files
#this code ensures the images are not duplicated in the train and val data
import os
import random
import shutil

# Source directories for images and annotations
image_dir = '/home/simrannaik/Organic_OCR/Organic_Yolo-Ocr/Dataset/raw_files/Final_Images'
label_dir = '/home/simrannaik/Organic_OCR/Organic_Yolo-Ocr/Dataset/raw_files/Final_Annotations'

# Destination directories for the split data
train_image_dir = '/home/simrannaik/Organic_OCR/Organic_Yolo-Ocr/Dataset/images/train'
val_image_dir = '/home/simrannaik/Organic_OCR/Organic_Yolo-Ocr/Dataset/images/val'
train_label_dir = '/home/simrannaik/Organic_OCR/Organic_Yolo-Ocr/Dataset/labels/train'
val_label_dir = '/home/simrannaik/Organic_OCR/Organic_Yolo-Ocr/Dataset/labels/val'

# Create the destination directories if they don't exist
os.makedirs(train_image_dir, exist_ok=True)
os.makedirs(val_image_dir, exist_ok=True)
os.makedirs(train_label_dir, exist_ok=True)
os.makedirs(val_label_dir, exist_ok=True)

# Set the split ratio (e.g., 20% of the data for validation)
split_ratio = 0.2

# List all images in the dataset (assuming they are .jpg or .png files)
all_images = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

# Shuffle the list of images
random.shuffle(all_images)

# Calculate the number of validation samples
val_count = int(len(all_images) * split_ratio)

# Split the images into validation and training sets
val_images = set(all_images[:val_count])
train_images = set(all_images[val_count:])

# Check for duplicates
duplicates = val_images.intersection(train_images)
if duplicates:
    raise ValueError(f"Duplicate images found: {duplicates}")

# Function to copy files
def copy_files(file_list, source_dir, target_dir, label_source_dir, label_target_dir):
    for file_name in file_list:
        # Copy the image
        try:
            shutil.copy2(os.path.join(source_dir, file_name), os.path.join(target_dir, file_name))
            print(f"Copied image: {file_name}")
        except FileNotFoundError:
            print(f"Image file {file_name} not found in source directory.")
            continue
        
        # Copy the corresponding label (assume .txt extension)
        label_name = file_name.replace('.png', '.txt').replace('.jpg', '.txt')
        label_path = os.path.join(label_source_dir, label_name)
        
        if os.path.exists(label_path):
            try:
                shutil.copy2(label_path, os.path.join(label_target_dir, label_name))
                print(f"Copied label: {label_name}")
            except FileNotFoundError:
                print(f"Label file {label_name} not found in source directory.")
        else:
            print(f"Label file {label_name} not found for image {file_name}.")

# Copy training files
copy_files(train_images, image_dir, train_image_dir, label_dir, train_label_dir)

# Copy validation files
copy_files(val_images, image_dir, val_image_dir, label_dir, val_label_dir)

# Print the number of files in each directory after the copy
print(f"Training images: {len(os.listdir(train_image_dir))}")
print(f"Validation images: {len(os.listdir(val_image_dir))}")
print(f"Training labels: {len(os.listdir(train_label_dir))}")
print(f"Validation labels: {len(os.listdir(val_label_dir))}")

