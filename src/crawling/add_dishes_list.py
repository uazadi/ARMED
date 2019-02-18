from bs4 import BeautifulSoup
import urllib
import os
import glob


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

def get_num_dished(cuisine):
    url = "https://www.bbc.com/food/recipes/search?cuisines[]=" + cuisine
    local_filename, headers = urllib.request.urlretrieve(url)
    html = open(local_filename)
    soup = BeautifulSoup(html, "html.parser")
    text = str(soup.find_all("div", id="queryBox"))
    text = text.split("<p>")[1].split(" ")[0]
    return int(text)



cuisines = ["british", "caribbean",
           "chinese", "east_european", "french", "greek",
           "indian", "irish", "italian", "japanese",
           "korean", "mexican", "nordic", "north_african",
           "pakistani", "portuguese", "south_american",
           "spanish", "thai_and_south-east_asian",
           "turkish_and_middle_eastern"]




#recepies_dataset = "/home/umberto/Desktop/DetasetRecepies2/"

id_ingredients = {}
id_traker = 0
count = 0
for file in glob.glob("/home/umberto/Desktop/DetasetRecepies/*.csv"):
    with open(file) as recipes:
        for line in recipes:
            recipe = line.split(";")[:-1]
            name = recipe[0]
            ingrs = recipe[1:]
            for ingr in ingrs:
                key = ingr
                if not(key in id_ingredients):
                    id_ingredients[key] = id_traker
                    id_traker += 1
            if count % 100 == 0:
                print(count, end=", ")
            count += 1

id_ingredients["water"] = id_traker
id_traker += 1


for cuisine in cuisines:
    num_of_dishes_for_page = 15
    num_dished = get_num_dished(cuisine)
    print("Current letter: ", cuisine, "  --  num of dishes: ", num_dished)

    no_link_ing = open("/home/umberto/Desktop/NoLinkIngr/" + cuisine + ".txt", "w")

    #dataset_name = recepies_dataset + cuisine + ".csv"
    #dataset = open(dataset_name, "w")

    upp = int(num_dished/num_of_dishes_for_page)
    if num_dished % num_of_dishes_for_page != 0:
        upp += 1

    for i in range(1, upp+1):
        url = "https://www.bbc.com/food/recipes/search?page=" + str(i) +"&cuisines%5B0%5D=" + cuisine + "&sortBy=lastModified"
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
            list_ingr = ""

            #for ingr in soup2.find_all("a", class_="recipe-ingredients__link"):
             #   list_ingr += str(ingr).split(">")[1][:-3] + ";"

            for ingr in soup2.find_all("li", class_="recipe-ingredients__list-item"):
                if "</a>" not in str(ingr):
                    name = str(ingr).split("<")[1].split(">")[-1]
                    if "water" in name:
                        no_link_ing.write(name + "| water" + "\n")
                    elif "pork ribs" in name:
                        no_link_ing.write(name + "| pork ribs" + "\n")
                    elif "salt" in name or "pepper" in name:
                        if "salt" in name and "pepper" in name:
                            no_link_ing.write(name + "| salt; pepper" + "\n")
                        elif "salt" in name and "pepper" not in name:
                            no_link_ing.write(name + "| salt" + "\n")
                        elif "salt" not in name and "pepper" in name:
                            no_link_ing.write(name + "| pepper" + "\n")
                    elif " " not in name:
                        no_link_ing.write(name + "| " + name + "\n")
                    else:
                        no_link_ing.write(name + "| " + "\n")


            #dataset.write(name + ";" + list_ingr + "\n")

            html2.close()
            os.remove(file)

        html.close()
        os.remove(local_filename)
    #dataset.close()