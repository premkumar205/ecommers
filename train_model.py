import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords if not present
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    if pd.isna(text):
        return ""
    # Lowercase
    text = str(text).lower()
    # Remove special characters
    text = re.sub(r'[^a-z0-9\s]', '', text)
    # Remove stopwords
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

def main():
    print("Loading dataset...")
    df = pd.read_excel('dataset/product_recommendation_dataset_cleaned.xlsx')
    
    # Print columns for debugging
    print("Columns in dataset:", df.columns.tolist())
    
    # Fill missing values
    df.fillna('', inplace=True)
    
    # Safely get columns
    def get_col(col_name):
        if col_name in df.columns:
            return df[col_name].astype(str)
        return pd.Series([""] * len(df))
    
    # Combine text fields safely
    print("Processing text...")
    df['combined_text'] = get_col('Product_Name') + " " + \
                          get_col('Category') + " " + \
                          get_col('Brand') + " " + \
                          get_col('Tags') + " " + \
                          get_col('Description')
                          
    df['combined_text'] = df['combined_text'].apply(clean_text)
    
    print("Generating TF-IDF vectors...")
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_text'])
    
    print("Computing Cosine Similarity...")
    similarity = cosine_similarity(tfidf_matrix)
    
    print("Exporting artifacts...")
    os.makedirs('model', exist_ok=True)
    joblib.dump(tfidf, 'model/tfidf.pkl')
    joblib.dump(similarity, 'model/similarity.pkl')
    # Records are already prepared with image_path from the cleaned dataset
    joblib.dump(df.to_dict('records'), 'model/products.pkl')
    
    # Create an index mapping for quick lookup by Product_ID safely
    if 'Product_ID' in df.columns:
        indices = pd.Series(df.index, index=df['Product_ID']).to_dict()
    else:
        # Fallback to index if Product_ID doesn't exist
        indices = pd.Series(df.index, index=df.index).to_dict()
        
    joblib.dump(indices, 'model/indices.pkl')
    
    print("Training complete! Artifacts saved in model/")

if __name__ == "__main__":
    main()
