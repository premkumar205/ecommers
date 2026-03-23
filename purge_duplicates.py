import os

dataset_path = r"c:\Users\yadav\Downloads\pjt\dataset"
images_path = os.path.join(dataset_path, "images")
placeholders_path = os.path.join(dataset_path, "placeholders")

# Get sizes of all placeholders
placeholder_sizes = set()
if os.path.exists(placeholders_path):
    for f in os.listdir(placeholders_path):
        if f.endswith(".jpg"):
            size = os.path.getsize(os.path.join(placeholders_path, f))
            placeholder_sizes.add(size)
            print(f"Placeholder {f} size: {size}")

# Common duplicate size found earlier
placeholder_sizes.add(100526)
placeholder_sizes.add(110386)
placeholder_sizes.add(185506)
placeholder_sizes.add(105060)
placeholder_sizes.add(469412) # Smartwatch duplicate for smartphones
placeholder_sizes.add(449022) # Another common duplicate

count = 0
deleted = 0

for root, dirs, files in os.walk(dataset_path):
    # Skip placeholders directory itself to avoid deleting them!
    if "placeholders" in root:
        continue
        
    for f in files:
        if f.startswith("product_") and f.endswith(".jpg"):
            count += 1
            full_path = os.path.join(root, f)
            size = os.path.getsize(full_path)
            # Delete placeholders and SVG-content "JPGs"
            is_svg = False
            if size < 30000: # SVG placeholders are usually small
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        header = f.read(100)
                        if '<svg' in header:
                            is_svg = True
                except:
                    pass
                
            if size in placeholder_sizes or is_svg:
                os.remove(full_path)
                deleted += 1

print(f"Total product images checked: {count}")
print(f"Deleted {deleted} duplicate/generic images.")
