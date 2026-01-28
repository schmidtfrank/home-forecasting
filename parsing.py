import pandas as pd
from bs4 import BeautifulSoup

def remove_commas(word):
    return int(word.replace(",", ""))

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
with open("scraped/urbanaP1.html") as page:
    soup = BeautifulSoup(page,features="html.parser")

#extract prices
prices_raw = soup.find_all(class_="price-content")
other_info = soup.find_all(class_="detailed-info-container")

if len(prices_raw) != len(other_info):
    raise RuntimeError

#these are currently indexing an element but that will need to be done per element in later list and fixed each time.
valid_price = remove_commas(prices_raw[0].text.strip()[1:])
valid_other_info = fix_bed_bath_list(other_info[0].contents)

db = []
for i in range(len(valid_price)):
    #need to dynamically determine column names based on content list
    pass