import requests
from datetime import datetime

def download_image(url:str=None, filename:str=None):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(f'output/{filename}', 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image downloaded successfully: {filename}")
    else:
        print(f"Failed to download image: {response.status_code}")

def timestamp_to_date(timestamp:str=None)->list[str,int]:
    date = datetime.fromtimestamp(timestamp / 1000)
    date_string = date.strftime('%Y-%m-%d')
    month = date.strftime('%B')

    return date_string, month

def get_later_month_from_today(month:int=0):
    today = datetime.now()
    if month in [0,1]:
        return today.month
    
    month = today.month - month
    if month > 12:
        month = month - 12
    return month