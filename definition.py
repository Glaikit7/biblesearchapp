import requests
import json
import PyPDF2
import re
from bs4 import BeautifulSoup

# create an empty dictionary to store the names and meanings
# this one is hitchcocks dictionary
old_dict = {}
# create an empty list of names
rawnames = []
names = []


# CREATE LIST OF BIBLE NAMES
# add all Bible names to list
url = 'https://www.biblegateway.com/resources/all-men-bible/Alphabetical-Order-All-Men'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

    # find all the a tags that match the criteria
name_a = soup.find_all("a", href=lambda x: x and x.startswith("/resources/all-men-bible/"))

    # extract the names from the a tags and clean names
rawnames = [re.sub(r'\d+', '', a.text).strip() for a in name_a]
rawnames = [name.split(', ') for name in rawnames]
for name_group in rawnames:
    for name in name_group:
        names.append(name)


print('looping old_dict')
# ADD DEFINITIONS FROM HITCHCOCKS
# loop through the names in hitchcocks dictionary 
try:    
    for name in names:
        # make a request to the website
        url = f"https://www.biblestudytools.com/dictionaries/hitchcocks-bible-names/{name}.html"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')


        # find the definition in the website, definitions are contained in blockquotes
        blockquote = soup.find('blockquote')
        if blockquote:
            meaning = blockquote.get_text()
            old_dict[name] = meaning
        else:
            print(f'{name} not found')

except requests.exceptions.RequestException as e:
    print(e)
    print(f'{name} not found')


# ADD DEFINITIONS FROM SMITHS
# create smiths dictionary
new_names = {}

print('looping new_names')
# loop through the names in smiths dictionary 
try:    
    for name in names:
        # make a request to the website
        url = f"https://www.biblegateway.com/resources/all-men-bible/{name}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')


        # find the definition in the website, definitions are contained in <i> tags
        div = soup.find('span', class_ = 'small-caps')
        if div:
           meaning = div.get_text()
           new_names[name] = meaning
        else:
            print(f'{name} not found')

except requests.exceptions.RequestException as e:
    print(e)
    print(f'{name} not found')

 #create new dict called names_dict then combine old_dict and new_names
try:
    names_dict = {k: (v + ' ; ' + new_names[k]) if k in new_names else v for k, v in old_dict.items()}
    names_dict.update({k: v for k, v in new_names.items() if k not in names_dict})

except:
   pass


# ADD DEFINITIONS FROM PDF SOURCE
# open the pdf file in binary mode
pdfFileObj = open('Biblical-Names-and-their-Meanings.pdf', 'rb')

# create a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# create an empty dictionary to store the names and meanings
pdf_dict = {}

# loop through all the pages
for page_num in range(len(pdfReader.pages)):
    # get the page object
    page_obj = pdfReader.pages[page_num]
    
    # extract the text from the page
    page_text = page_obj.extract_text()
    
    # extract the names and meanings from the text
    lines = page_text.split("\n")
    for line in lines:
        for name in names:
            if line.startswith(name):
                try:
                    name, meaning = line.split(", ", 1)
                    pdf_dict[name] = meaning
                    break
                except ValueError:
                    pass

# close the pdf file
pdfFileObj.close()


# update names_dict
try:
    names_dict.update({k: (v + ' ; ' + pdf_dict[k]) if k in pdf_dict else v for k, v in names_dict.items()})
    names_dict.update({k: v for k, v in pdf_dict.items() if k not in names_dict})

except:
    pass







# save names_dict to file
with open('biblenames.json', 'w') as outfile:
    json.dump(names_dict, outfile)
