from bs4 import BeautifulSoup
import urllib
import requests
import os



def page_exists(url):
    req = requests.get(url, allow_redirects=False)
    if req.status_code == 200:
        return True
    return False

letters = 'abcdefghijklmnopqrstuvwxyz'
ingredients_list = []
output = open("/home/umberto/Desktop/AI/Ingredients_list.txt", "w")


for letter in letters:
    print("Current letter: ", letter)
    for i in range(1,10):
        url = "https://www.bbc.com/food/ingredients/a-z/" + letter + "/" + str(i) + "#featured-content"
        if page_exists(url):
            local_filename, headers = urllib.request.urlretrieve(url)
            html = open(local_filename)
            soup = BeautifulSoup(html, "html.parser")
            ingrs = soup.find_all("h3", class_="promo__title gel-pica")
            for i in ingrs:
                output.write(str(i).split(">")[1].split("<")[0] + "\n")
            html.close()
            os.remove(local_filename)

output.close()



