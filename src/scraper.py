import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone, timedelta

DATA_DIR = 'data'
CSV_DIR = 'exchange_rate.csv'
UTILS_DIR = 'utils'
TXT_DIR = 'metadata.txt'
headers = ['TIMESTAMP', 'RATE (EGP)']

tz = timezone(timedelta(hours=2))

url = "https://wise.com/us/currency-converter/usd-to-egp-rate"

def save_to_csv(data : dict):
    os.makedirs(DATA_DIR , exist_ok = True)
    data_path = os.path.join(DATA_DIR , CSV_DIR)
    file_exists_flag = os.path.exists(data_path)
    with open(file = data_path , mode = 'a') as f:
        if not file_exists_flag:
            f.write(','.join(headers))
            f.write('\n')

        f.write(str(data['timestamp']))
        f.write(',')
        f.write(data['rate'])
        f.write('\n')

def save_metadata(metadata : dict):
    os.makedirs(UTILS_DIR , exist_ok = True)
    metadata_path = os.path.join(UTILS_DIR , TXT_DIR)
    with open(file = metadata_path , mode = 'w') as f:
        f.write(f"Latest Price: {metadata['rate']}")

def main():
    try:
        response = requests.get(url , timeout = 10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        for tag in soup.find_all('span', dir="ltr"):
            exchange_price = tag.text.split('=')

            if len(exchange_price) < 2:   
                continue

            if 'EGP' in exchange_price[0]:
                rate = exchange_price[0].split(' ')[0]
            else:
                rate = exchange_price[1].split(' ')[1]

            try:                          
                float(rate)
            except ValueError:
                continue

            data_frame = {
                'timestamp' : datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z') ,
                'rate' : rate
                }
            save_to_csv(data_frame)
            save_metadata(data_frame)
            break

    except requests.RequestException as error:
        print(f'Error: {error}')

if __name__ == '__main__':
    main()