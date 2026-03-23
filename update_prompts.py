import pandas as pd
import random
import os
import json

# Paths
DATASET_PATH = 'dataset/product_recommendation_dataset.xlsx'
CLEANED_DATASET_PATH = 'dataset/product_recommendation_dataset_cleaned.xlsx'
CACHE_PATH = 'dataset/image_cache.json'

# Prompt Components
lighting_styles = [
    "soft studio lighting with gentle shadows", 
    "dramatic cinematic lighting with high contrast", 
    "natural golden hour sunlight streaming from a side window", 
    "bright and airy mediterranean morning light", 
    "cool minimalist gallery lighting",
    "warm cozy candlelight ambience",
    "professional product photography strobes"
]

contexts = [
    "resting on a polished white marble surface", 
    "displayed in a modern minimalist industrial loft", 
    "placed on a dark rustic reclaimed oak table", 
    "set against a lush blurred garden background", 
    "arranged on a sleek matte black glass desk", 
    "in a high-end luxury boutique showroom",
    "on a clean concrete floor with architectural shadows",
    "positioned on a designer velvet pedestal"
]

camera_angles = [
    "macro 85mm lens close-up focusing on texture", 
    "wide angle 35mm lifestyle photography shot", 
    "eye-level sharp focus commercial photography", 
    "dramatic low-angle hero shot", 
    "perfect top-down flat-lay composition"
]

materials_map = {
    "Electronics": ["brushed aluminum", "matte polycarbonate", "tempered glass", "anodized metal"],
    "Clothing": ["organic cotton", "breathable mesh", "premium denim", "soft wool blend"],
    "Footwear": ["genuine leather", "flexible rubber", "durable canvas", "suede finish"],
    "Home": ["ceramic", "stainless steel", "natural wood", "tempered glass"],
    "Sports": ["high-grip synthetic", "carbon fiber", "lightweight alloy", "reinforced nylon"]
}

def generate_enhanced_prompt(row):
    product_id = str(row.get('Product_ID', ''))
    product_name = str(row.get('Product_Name', 'Product'))
    brand = str(row.get('Brand', 'Premium'))
    category = str(row.get('Category', 'General'))
    description = str(row.get('Description', ''))
    
    # Extract material based on category or random
    category_key = "Home" # Default
    for key in materials_map.keys():
        if key.lower() in category.lower():
            category_key = key
            break
    
    material = random.choice(materials_map.get(category_key, ["high-quality material"]))
    lighting = random.choice(lighting_styles)
    context = random.choice(contexts)
    angle = random.choice(camera_angles)
    
    # Construct highly descriptive prompt
    # Including ID and full name for maximum specificity
    prompt = f"A high-end professional catalog photo of a {brand} {product_name} (ID: {product_id}) made of {material}. The item is {context}. Featuring {lighting}, {angle}. Real photography with sharp focus and authentic textures."
    
    return prompt

def main():
    if not os.path.exists(DATASET_PATH):
        print(f"Error: {DATASET_PATH} not found.")
        return

    print(f"Loading dataset from {DATASET_PATH}...")
    df = pd.read_excel(DATASET_PATH)
    
    print("Generating unique prompts...")
    df['AI_Image_Prompt'] = df.apply(generate_enhanced_prompt, axis=1)
    
    print(f"Saving updated dataset to {CLEANED_DATASET_PATH}...")
    df.to_excel(CLEANED_DATASET_PATH, index=False)
    
    # Also update image_cache.json for legacy support if needed
    # but the user specifically asked for it. 
    # We will populate it with the first 50 common names for quick reference
    cache_data = {}
    for name in df['Product_Name'].unique()[:100]:
        sample_prompt = df[df['Product_Name'] == name]['AI_Image_Prompt'].iloc[0]
        cache_data[name] = f"https://image.pollinations.ai/prompt/{random.randint(1,100000)}%20{sample_prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true"
    
    with open(CACHE_PATH, 'w') as f:
        json.dump(cache_data, f, indent=4)
        
    print("Prompts updated successfully!")
    print("\nSample Prompts:")
    for i in range(5):
        print(f"- {df.iloc[i]['Product_Name']}: {df.iloc[i]['AI_Image_Prompt']}")

if __name__ == "__main__":
    main()
