import asyncio
import os.path
from time import sleep
import json
import pandas as pd
import random
from datetime import date, timedelta
import csv

def save_update_txtFile(file_name,data):
    check_file = os.path.exists(file_name)
    if check_file == True:
        file = open(file_name,"a")
        file.write(data)
    else:
        file = open(file_name,"w+")
        file.write(data)

async def get_value_atrribute(page,selector, attribute):
    final_output = []
    elm_handle = await page.query_selector_all(selector)
    elm_count = len(elm_handle)
    for i in range(elm_count):
        elm_value = await elm_handle[i].get_attribute(attribute)
        final_output.append(elm_value)
    
    sleep(.2)
    return final_output

async def get_inner_text(page,selector):
    try:
        elm_handle = await page.query_selector(selector)
        elm_value = await elm_handle.inner_html()
        return elm_value.strip()
    except:
        return None

async def get_inner_text_all(page,selector):
    final_output = []
    try:
        elements = await page.query_selector_all(f'{selector}')
        for element in elements:
            inner_text = await element.inner_text()
            final_output.append(inner_text)
        
        sleep(.2)
        return final_output
    except:
        return final_output

async def remove_duplicate(string):
    str_list = string.split(', ')
    unique = list(set(str_list))
    return ', '.join(unique)

async def save_session(context, session_file):
    cookies = await context.cookies()
    with open(session_file, 'w') as f:
        f.write(json.dumps(cookies))

async def load_session(context, session_file):
    check_file = os.path.exists(session_file)
    if check_file:
        with open(session_file, "r") as f:
            cookies = json.loads(f.read())
            await context.add_cookies(cookies)
    else:
        print(f'{session_file} is Not Exist.')

async def save_csv(arr,filename = "my_file"):
    with open(f'{filename}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write each row of the array as a separate line in the CSV file
        for row in arr:
            writer.writerow(row)

def read_xlsx(filePath):
    final_output = []
   # Load the CSV file into a dataframe
    df = pd.read_excel(filePath)

    # Loop through each column in the dataframe
    for index,row in df.iterrows():
        row_value = []
        for value in row:
            row_value.append(value)
        final_output.append(row_value)
    
    return final_output

async def add_check_price(price_in):
    price = price_in.replace(' ', '').replace(',', '')
    if '$' in price:
        if len(price) == 3 or len(price) >= 6:
            return True
        else:
            return False
    else:
        if len(price) == 2 or len(price) >= 5:
            return True
        else:
            return False

async def get_attribute_value(page,selector,attribute_name):
    try:
        element_list = await page.query_selector_all(selector)
        attribute_value = [ await element.get_attribute(attribute_name) for element in element_list]
        sleep(.4)
        return attribute_value
    except Exception as e:
        return None

async def read_dir(path):
    loop = asyncio.get_running_loop()
    file_name_arr = []

    files = await loop.run_in_executor(None, os.listdir, path)
    for file in files:
        file_path = os.path.join(path, file)
        file_name_arr.append(file_path)

    return file_name_arr

async def is_empty_dir(dirname):
    loop = asyncio.get_running_loop()
    files = await loop.run_in_executor(None, os.listdir, dirname)
    return len(files) == 0

async def get_previous_date(num_day):
    today = date.today()
    two_days_ago = today - timedelta(days=num_day)
    formatted_date = two_days_ago.strftime('%d-%m-%Y')
    return formatted_date

def get_description_parse_value(description):
    description = description.lower()
    parsed_value = {
        "fenced_yard": 'Yes' if 'fenced yard' in description else '',
        "garage": 'Yes' if 'garage' in description else '',
        "ac": 'Yes' if 'a/c' in description or ' ac,' in description else '',
        "fireplace": 'Yes' if 'fireplace' in description else '',
        "pool": 'Yes' if 'pool' in description else '',
        "hot_tub": 'Yes' if 'hot tub' in description else '',
        "sauna": 'Yes' if 'sauna' in description else '',
        "gym": 'Yes' if 'gym' in description else '',
        "laundry_in_suite": 'Yes' if 'laundry-in suite' in description or 'in-suite laundry' in description or ('laundry' in description and 'no laundry' not in description) else '',
        "laundry_on_site": 'Yes' if 'laundry-on site' in description or 'on-site laundry' in description else '',
        "dishwasher": 'Yes' if 'dishwasher' in description or 'diswasher' in description else '',
        "utilities_included": 'Yes' if 'utilities included' in description or 'including utilities' in description or 'rent covers utilities' in description else '',
        "view": 'Yes' if 'view' in description else '',
        "water_access": 'Yes' if 'water access' in description else ''
    }
    return parsed_value

def read_csv_file(file_path):
    objects = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            objects.append(row)
    
    return objects

def array_to_csv(array_of_objects, file_name):
    if len(array_of_objects) > 0:
        fieldnames = array_of_objects[0].keys()
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for obj in array_of_objects:
                writer.writerow(obj)
        print(f"Data successfully written to {file_name}")
    else:
        print("The input array is empty, no CSV generated.")