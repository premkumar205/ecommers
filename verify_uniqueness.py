import pandas as pd
df = pd.read_excel('dataset/product_recommendation_dataset_cleaned.xlsx')
print('Checking 5 samples for uniqueness:\n')
for i in range(5):
    row = df.iloc[i]
    print(f"Product: {row.get('Product_Name')}")
    print(f"Prompt: {row.get('AI_Image_Prompt')}")
    print("---")
