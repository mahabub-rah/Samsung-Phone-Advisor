import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

df = pd.read_csv("data/data.csv", encoding="utf-8")
all_specs = []

for i, row in df.iterrows():
    specs = {}
    link = row['url']
    name = row['model_name']
    
    try:
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        specs['model_name'] = name
        
        # Find all specification tables
        spec_tables = soup.find_all('table', class_='data-table')
        
        for table in spec_tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    key = cells[0].text.strip().lower()
                    value = cells[1].text.strip()
                    
                    # Battery extraction
                    if 'battery' in key:
                        battery_match = re.search(r'(\d+)\s*mAh', value, re.I)
                        if battery_match:
                            specs['battery'] = f"{battery_match.group(1)}mAh"
                    
                    # Rear Camera extraction
                    elif any(word in key for word in ['rear', 'main', 'primary', 'back camera']):
                        if 'front' not in key and 'selfie' not in key:
                            # Find all MP values
                            mp_matches = re.findall(r'(\d+\s*MP)', value, re.I)
                            if mp_matches:
                                specs['rear_camera'] = ' + '.join(mp_matches)
                    
                    # Front Camera extraction
                    elif any(word in key for word in ['front', 'selfie']):
                        mp_matches = re.findall(r'(\d+\s*MP)', value, re.I)
                        if mp_matches:
                            specs['front_camera'] = ' + '.join(mp_matches)
                    
                    # RAM extraction
                    elif 'ram' in key:
                        ram_match = re.search(r'(\d+\s*GB)', value, re.I)
                        if ram_match:
                            specs['ram'] = ram_match.group(1)
                    
                    # Storage extraction
                    elif 'storage' in key or 'rom' in key:
                        storage_match = re.search(r'(\d+\s*GB)', value, re.I)
                        if storage_match:
                            specs['storage'] = storage_match.group(1)
        
        # If not found in tables, search in the entire page content
        if 'battery' not in specs:
            battery_match = re.search(r'(\d+)\s*mAh', soup.text, re.I)
            if battery_match:
                specs['battery'] = f"{battery_match.group(1)}"
        
        if 'rear_camera' not in specs:
            # Look for camera patterns in the entire page
            camera_sections = re.findall(r'(\d+MP(?:\s*\+\s*\d+MP)*)', soup.text, re.I)
            if camera_sections:
                specs['rear_camera'] = ' + '.join(camera_sections[:1])
        
        # default values if not found
        specs.setdefault('battery', None)
        specs.setdefault('rear_camera', None)
        specs.setdefault('ram', None)
        specs.setdefault('storage', None)
        specs.setdefault('price', 10000)
        

        # Price scrape
        price = soup.find("span", class_="price")
        if price:
            price_text = price.text.strip()
            price_numbers = re.findall(r'[\d,]+', price_text)
            if price_numbers:
                specs['price'] = int(price_numbers[0].replace(',', ''))
    
        all_specs.append(specs)
        time.sleep(1)
 
        
    except Exception as e:
        error_specs = {
            'model_name': name,
            'battery': None,
            'rear_camera': None,
            'ram': None,
            'storage': None,
            'price': None
        }
        all_specs.append(specs)
    
    time.sleep(1)