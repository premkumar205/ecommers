import os
import pandas as pd
import shutil

DATASET_PATH = 'dataset/product_recommendation_dataset_cleaned.xlsx'
IMAGE_DIR = 'dataset/images/'
BASE_DATASET_DIR = 'dataset/'

def organize():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: {DATASET_PATH} not found.")
        return

    df = pd.read_excel(DATASET_PATH)
    print(f"Loaded {len(df)} products for organization.")

    count = 0
    for _, row in df.iterrows():
        p_id = int(row['Product_ID'])
        category = str(row.get('Category', 'Electronics')).strip()
        # Handle "Home & Kitchen" folder name properly
        cat_folder = os.path.join(BASE_DATASET_DIR, category)
        
        if not os.path.exists(cat_folder):
            os.makedirs(cat_folder, exist_ok=True)
            
        old_path = os.path.join(IMAGE_DIR, f"product_{p_id}.jpg")
        new_path = os.path.join(cat_folder, f"product_{p_id}.jpg")
        
        if os.path.exists(old_path):
            # Move if it doesn't exist in new place or if we want to force refresh
            shutil.move(old_path, new_path)
            count += 1

    print(f"Successfully organized {count} images into categorical folders.")

if __name__ == "__main__":
    organize()
