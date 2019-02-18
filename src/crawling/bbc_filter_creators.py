from bs4 import BeautifulSoup
import urllib
import os

def page_exists(url):
    local_filename, headers = urllib.request.urlretrieve(url)
    html = open(local_filename)
    soup = BeautifulSoup(html, "html.parser")
    next = soup.find_all("a", class_="pagInfo-page-numbers-next empty")
    html.close()
    os.remove(local_filename)

    if len(next) == 0:
        return True
    else:
        return False

def url_diets(dataset, cuisine, diet):

    url = "https://www.bbc.com/food/recipes/search?cuisines%5B0%5D=" \
          + cuisine \
          + "&sortBy=lastModified&diets%5B0%5D=" + diet
    local_filename, headers = urllib.request.urlretrieve(url)
    html = open(local_filename)
    soup = BeautifulSoup(html, "html.parser")
    text = str(soup.find_all("div", id="queryBox"))
    text = text.split("<p>")[1].split(" ")[0]

    if text != "Please": # If the ampty page is NOT returned
        num_dished = int(text)
        upp = int(num_dished / num_of_dishes_for_page)
        if num_dished % num_of_dishes_for_page != 0:
            upp += 1


        for i in range(1, upp + 1):
            url = "https://www.bbc.com/food/recipes/search?page=" + \
                  str(i) + "&cuisines%5B0%5D=" + cuisine + \
                  "&sortBy=lastModified&diets%5B0%5D=" + diet

            local_filename, headers = urllib.request.urlretrieve(url)
            html = open(local_filename)
            soup = BeautifulSoup(html, "html.parser")

            for dish in soup.find_all("div", class_="left with-image"):
                name = str(dish).split("</a>")[0].split(">")[-1]
                dataset.write(cuisine + ";" + name + "\n")

            html.close()
            os.remove(local_filename)


def text_diets(dataset, cuisine, pattern):
    url = "https://www.bbc.com/food/recipes/search?cuisines[]=" + cuisine
    local_filename, headers = urllib.request.urlretrieve(url)
    html = open(local_filename)
    soup = BeautifulSoup(html, "html.parser")
    text = str(soup.find_all("div", id="queryBox"))
    text = text.split("<p>")[1].split(" ")[0]
    num_dished = int(text)

    upp = int(num_dished / num_of_dishes_for_page)
    if num_dished % num_of_dishes_for_page != 0:
        upp += 1

    for i in range(1, upp+1):
        url = "https://www.bbc.com/food/recipes/search?page=" \
              + str(i) +"&cuisines%5B0%5D=" \
              + cuisine + "&sortBy=lastModified"
        local_filename, headers = urllib.request.urlretrieve(url)
        html = open(local_filename)
        soup = BeautifulSoup(html, "html.parser")

        for dish in soup.find_all("div", class_="left with-image"):
            domain = "https://www.bbc.com"
            link = str(dish).split("href=")[1].split("\"")[1]
            name = str(dish).split("</a>")[0].split(">")[-1]

            url2 = domain + link
            file, h = urllib.request.urlretrieve(url2)
            html2 = open(file)
            soup2 = BeautifulSoup(html2, "html.parser")

            for description in soup2.find_all("p", class_="recipe-description__text"):
                if pattern in str(description):
                    dataset.write(cuisine + ";" + name + "\n")

            html2.close()
            os.remove(file)

        html.close()
        os.remove(local_filename)



cuisines = ["african", "american",  "british", "caribbean",
           "chinese", "east_european", "french", "greek",
           "indian", "irish", "italian", "japanese",
           "korean", "mexican", "nordic", "north_african",
           "pakistani", "portuguese", "south_american",
           "spanish", "thai_and_south-east_asian",
           "turkish_and_middle_eastern"]


#"dairy_free", "egg_free", "gluten_free", "nut_free", "pregnancy_friendly",
# "vegan", "vegetarian",
diets = ["low_Glycemic_Index", "Low_calorie"]


recepies_dataset = "/home/umberto/Desktop/Filters/"


for diet in diets:
    print("Current diet: ", diet)
    for cuisine in cuisines:
        num_of_dishes_for_page = 15
        print("\tCurrent letter: ", cuisine)
        dataset_name = recepies_dataset + diet + ".csv"
        dataset = open(dataset_name, "a")

        #if diet in diets[0:-2]:
        #    url_diets(dataset, cuisine, diet)
        if diet is "low_Glycemic_Index":
            text_diets(dataset, cuisine, "high protein, low GI")
        elif diet is "Low_calorie":
            text_diets(dataset, cuisine, "kcal")

        dataset.close()
