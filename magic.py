import requests
from bs4 import BeautifulSoup
import csv
import re

r = requests.get('https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&Locality=Bopal&cityName=Mumbai')
soup = BeautifulSoup(r.text, 'html.parser')

category = []
size = []
price = []
floor = [] 
image = []
    
for item in soup.findAll('div', {'class': 'm-photo__fig'}):
    print("=====================",item)
    images = item.select_one('.m-photo__img')
    image.append(images['src'])
for item in soup.findAll('span', {'class': 'm-srp-card__title__bhk'}):
    category.append(item.get_text(strip=True))
for item in soup.findAll(text=re.compile('area$')):
    size.append(item.find_next('div').text)
for item in soup.findAll('span', {'class': 'm-srp-card__price'}):
    price.append(item.text)
for item in soup.findAll(text='floor'):
    floor.append(item.find_next('div').text)
data = []
for items in zip(category, size, price, floor):
    data.append(items)

print("category",category)
print("size",size)
print("price",price)
print("floor",floor)
print("image",image)
