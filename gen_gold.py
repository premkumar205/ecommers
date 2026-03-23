import os, requests, urllib.parse, time

def gen():
    prompts = {
        'gold_electronics.jpg': 'New modern high-tech electronic gadget product shot, studio lighting, white background, professional e-commerce photography',
        'gold_fashion.jpg': 'New mens denim jacket product shot, rugged style, studio lighting, white background, professional e-commerce photography',
        'gold_beauty.jpg': 'New luxury perfume bottle product shot, high-end branding, studio lighting, white background, professional e-commerce photography',
        'gold_home.jpg': 'New modern stainless steel toaster appliance product shot, studio lighting, white background, professional e-commerce photography',
        'gold_sports.jpg': 'New professional running shoe product shot, sports gear, studio lighting, white background, professional e-commerce photography'
    }
    placeholder_dir = r"c:\Users\yadav\Downloads\pjt\dataset\placeholders"
    os.makedirs(placeholder_dir, exist_ok=True)
    
    for filename, p in prompts.items():
        url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(p)}?width=1024&height=1024&nologo=true&seed=99"
        max_retries = 3
        for i in range(max_retries):
            try:
                resp = requests.get(url, timeout=30)
                if resp.status_code == 200 and len(resp.content) > 15000:
                    save_path = os.path.join(placeholder_dir, filename)
                    with open(save_path, 'wb') as f:
                        f.write(resp.content)
                    print(f"Generated {filename}")
                    break
                elif resp.status_code == 429:
                    print(f"Rate limited on {filename}, waiting 10s... (Try {i+1}/{max_retries})")
                    time.sleep(10)
                else:
                    print(f"Failed {filename}: {resp.status_code}")
                    break
            except Exception as e:
                print(f"Error {filename}: {e}")
                break
        time.sleep(5) # Base delay

if __name__ == "__main__":
    gen()
