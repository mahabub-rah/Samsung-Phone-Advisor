import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
def scrape():

    base_url = "https://www.startech.com.bd/samsung-mobile-phone"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    }

    req = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    
    phones = soup.select("div.p-item-inner h4 a")
    print(phones)
    data = []
    for phone in phones:
        name = phone.text.strip()
        link = phone["href"]
        data.append({"model_name": name, "url": link})

    os.makedirs('data', exist_ok=True)

    df = pd.DataFrame(data)
    df.to_csv("data/data.csv", index=False)
    print("CSV saved successfully!")
    


if __name__ == "__main__":
    scrape()