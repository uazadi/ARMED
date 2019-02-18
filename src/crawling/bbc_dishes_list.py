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

def get_num_dished(cuisine):
    url = "https://www.bbc.com/food/recipes/search?cuisines[]=" + cuisine
    local_filename, headers = urllib.request.urlretrieve(url)
    html = open(local_filename)
    soup = BeautifulSoup(html, "html.parser")
    text = str(soup.find_all("div", id="queryBox"))
    text = text.split("<p>")[1].split(" ")[0]
    return int(text)

def det_add_dishes_dict(cuisine):
    dict_add_dish = {}
    with open("/home/umberto/Desktop/NoLinkIngr/" + cuisine + ".txt") as file:
        for line in file:
            line = line.replace("\n", "")
            name = line.split("| ")[0]
            new_name = line.split("| ")[1]
            dict_add_dish[name.replace(" ", "")] = new_name

    return dict_add_dish

#
cuisines = [#"african", "american", "british", "caribbean",
            #"chinese", "east_european", "french", "greek",
           #"indian", "irish", "italian", "japanese",
           #"korean",
            "mexican", "nordic", "north_african",
           "pakistani", "portuguese", "south_american",
           "spanish", "thai_and_south-east_asian",
           "turkish_and_middle_eastern"]

recepies_dataset = "/home/umberto/Desktop/data/DetasetRecepies/"
#images_dataset = "/home/umberto/Desktop/DatasetImages/"

file_url = open("/home/umberto/Desktop/data/urls.csv", "a")

for cuisine in cuisines:
    num_of_dishes_for_page = 15
    num_dished = get_num_dished(cuisine)
    print("Current letter: ", cuisine, "  --  num of dishes: ", num_dished)

    dataset_name = recepies_dataset + cuisine + ".csv"
    dataset = open(dataset_name, "w")

    upp = int(num_dished/num_of_dishes_for_page)
    if num_dished % num_of_dishes_for_page != 0:
        upp += 1

    dict_add_dish = det_add_dishes_dict(cuisine)

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

            for ingr in soup2.find_all("a", class_="recipe-ingredients__link"):
                list_ingr += str(ingr).split(">")[1][:-3] + ";"

            for ingr in soup2.find_all("li", class_="recipe-ingredients__list-item"):
                if "</a>" not in str(ingr):
                    name_ing = str(ingr).split("<")[1].split(">")[-1]
                    if name_ing != "":
                        dict_value = dict_add_dish[name_ing.replace(" ", "")]
                        if dict_value != " ":
                            list_ingr += dict_value + ";"


            dataset.write(name + ";" + list_ingr + "\n")
            file_url.write(name + ";" + url2 + "\n")

            #imm = soup2.find_all("div", class_="responsive-image-container__16/9")[0]
            #link_imm = str(imm).split("src=")[1].split("\"")[1]

            #if not os.path.exists(images_dataset + cuisine):
            #    os.makedirs(images_dataset + cuisine)

            #urllib.request.urlretrieve(link_imm, images_dataset + cuisine + "/" + name + ".jpg")


            html2.close()
            os.remove(file)

        file_url.flush()

        html.close()
        os.remove(local_filename)
    dataset.close()
file_url.close()