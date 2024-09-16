import re
from datetime import datetime, date

from RPA.Excel.Files import Files

def save_dict_to_xlsx(data:dict=None, filename:str=None)->None:
  """Saves a dictionary to an Excel file.

  Args:
    data: A dictionary containing the data to be saved.
    filename: The name of the Excel file to save the data to.
  """
  lib = Files()
  lib.create_workbook(path=filename, fmt="xlsx")
  lib.create_worksheet(name="news data",content=data,header=True)
  lib.save_workbook()

def count_string_matches(string:str=None, substring:str=None)->int:
  """Counts the number of occurrences of a substring in a string.

  Args:
    string: The string to search.
    substring: The substring to search for.

  Returns:
    The number of occurrences of the substring in the string.
  """
  matches = re.findall(re.escape(substring), string)
  return len(matches)

def find_and_count_money_patterns(string_to_search:str='')->int:
  """Finds occurrences of money-related patterns in a string.

  Args:
    text: The string to search.

  Returns:
    The number of times money is mentioned in the string.
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
  """Converts a timestamp to a date string.

  Args:
    timestamp: The timestamp to convert.

  Returns:
    The date string in the format 'YYYY-MM-DD'.
  """
  date = datetime.fromtimestamp(timestamp / 1000)
  date_string = date.strftime('%Y-%m-%d')

  return date_string

def get_first_day_of_earlier_month(months_back:int=0)->str:
  """Returns the first day of the month that is months_back months before the current month.

  Args:
    months_back: The number of months to go back.

  Returns:
    The first day of the month that is months_back months before the current month.
  """    
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