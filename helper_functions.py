from datetime import datetime, date
import re
import pandas as pd

def save_dict_to_xlsx(data:dict=None, filename:str=None)->None:
    df = pd.DataFrame(data)
    df.to_excel(f'{filename}', index=False)

def count_string_matches(string:str=None, substring:str=None)->int:
    matches = re.findall(re.escape(substring), string)
    return len(matches)

def find_and_count_money_patterns(string_to_search:str='')->int:
  """Finds occurrences of money-related patterns in a string.

  Args:
    text: The string to search.

  Returns:
    A list of tuples, where each tuple contains the matched pattern and its starting index in the string.
  """

  patterns = [
    r"\$\d+\.\d+",  # $11.1
    r"\$\d{1,3}(,\d{3})*\.\d+",  # $111,111.11
    r"\d+ dollars",  # 11 dollars
    r"\d+ USD"  # 11 USD
  ]

  matches = []
  for pattern in patterns:
    for match in re.finditer(pattern, string_to_search):
      matches.append((match.group(), match.start()))

  return len(matches)

def timestamp_to_date(timestamp:str=None)->str:
    date = datetime.fromtimestamp(timestamp / 1000)
    date_string = date.strftime('%Y-%m-%d')
    # month = date.strftime('%B')

    return date_string

def get_first_day_of_earlier_month(months_back:int=0)->str:    
    today = date.today()
    if months_back in [0,1]:
        return date(today.year, today.month, 1).strftime('%Y-%m-%d')    
    
    months_back = months_back - 1

    target_month = today.month - months_back

    if target_month <= 0:
        target_month += 12
        target_year = today.year - 1
    else:
        target_year = today.year
        
    return date(target_year, target_month, 1).strftime('%Y-%m-%d')

def compare_dates(date1:str=None, date2:str=None):
  """Compares two dates and returns True if date1 is earlier than date2."""

  date1 = datetime.strptime(date1, '%Y-%m-%d')
  date2 = datetime.strptime(date2, '%Y-%m-%d')

  return date1 < date2


if __name__ == '__main__':
    month = get_first_day_of_earlier_month(3)
    print(month,type(month))
    actual_date = '2024-09-11'
    print(compare_dates(actual_date, month))
    
    