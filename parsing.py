import pandas as pd
from bs4 import BeautifulSoup

def fix_price(word):
    tmp = ""

    last_valid = 0
    for char in word:
        if char.isdigit():
            tmp += char
            last_valid = 0
        else:
            last_valid += 1
        
        #if we have gone through 2 characters without a digit, it is not valid
        if last_valid >= 2:
            break
    return int(tmp)

#Helper to remove newlines for the bed bath list
def remove_list_newlines(inc_list):
    out = []
    for elem in inc_list:
        if elem != '\n':
            out.append(elem)
    return out

#Helper to remove the li tag for the bed bath list
def remove_li_tag(inc_list):
    out = []
    for val in inc_list:
        #need to cast the val to a str because it is a beautiful soup object
        tmp0 = str(val)
        tmp = tmp0.replace("<li>","")
        final = tmp.replace("</li>","")
        out.append(final)
    return out

#Main function to fix the bed bath list
def fix_bed_bath_list(inc_list):
    out = remove_list_newlines(inc_list)
    out = remove_li_tag(out)
    return out

#load file
GLOBAL_PAGE_VAL = 3
with open(f"scraped/urbanaP{GLOBAL_PAGE_VAL}.html") as page:
    soup = BeautifulSoup(page,features="html.parser")

#extract prices
prices_raw = soup.find_all(class_="price-content")
other_info = soup.find_all(class_="detailed-info-container")

if len(prices_raw) != len(other_info):
    raise RuntimeError

#these are currently indexing an element but that will need to be done per element in later list and fixed each time.
valid_price = fix_price(prices_raw[0].text.strip()[1:])
valid_other_info = fix_bed_bath_list(other_info[0].contents)

db = []
for i in range(len(prices_raw)):
    #need to dynamically determine column names based on content list
    curr_price = fix_price(prices_raw[i].text.strip()[1:])
    curr_other_info = fix_bed_bath_list(other_info[i].contents)

    #choosing to omit land for sale as we only want housing data
    if curr_other_info[0] == 'Land':
        continue

    row = {}
    row["Price"] = curr_price
    for item in curr_other_info:
        #splits the beds/baths/sqft and value
        vals = item.split(" ",1)

        #hard cases
        if vals[1] == 'Bed':
            vals[1] = "Beds"

        if vals[1] == 'Bath':
            vals[1] = 'Baths'
        
        if vals[1] == 'Sq Ft':
            vals[1] = 'SqFt'
        
        row[vals[1]] = float(vals[0].replace(",",""))
    
    db.append(row)


df = pd.DataFrame(db)
df.to_csv(f"page{GLOBAL_PAGE_VAL}.csv",index=False)
