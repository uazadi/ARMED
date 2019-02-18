from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from termcolor import colored
import sys

def search_dish_vector(dish, file):
    with open(file) as f:
        for line in f:
            name = line.split(";")[0]
            if name.replace(" ", "") == dish.replace(" ", ""):
                vec = [float(v) for v in line.split(";")[1:]]
                return np.array(vec)
    print("[ERROR] origin dish (",dish,") or cuisine not found!", file=sys.stderr)
    print("__________________________________________________________", file=sys.stderr)
    return None


def get_cuisine_vector(file):
    _sum = None
    with open(file) as f:
        count = 0
        for line in f:
            vec = np.array([float(v) for v in line.split(";")[1:]])
            if _sum is None:
                _sum = vec
                count += 1
            else:
                _sum = _sum + vec
                count += 1
    return _sum / count


def get_dishes_matrix(file, filters=None, filters_path=""):
    matrix = []
    cuisine = file.split("/")[-1].split(".")[0]
    with open(file) as f:
        for line in f:
            vec = np.array([float(v) for v in line.split(";")[1:]])

            to_be_add = True
            if filters is not None and filters != []:
                to_be_add = False
                name = line.split(";")[0]
                for filter in filters:
                    with open(filters_path + filter + ".csv", 'r') as filter_file:
                        content = filter_file.read()
                        if cuisine + ";" + name in content:
                            to_be_add = True
                            continue

            if to_be_add:
                matrix.append(vec)

    return np.array(matrix)


def search_dish_name(vector, file):
    with open(file) as f:
        for line in f:
            vec = np.array([float(v) for v in line.split(";")[1:]])
            if np.array_equal(vec, vector):
                return str(line.split(";")[0])


def closest_node(node, nodes, num_of_suggestion):
    nodes = np.asarray(nodes)
    sim_vec = cosine_similarity([node], nodes)[0]
    indexes = sim_vec.argsort()[-num_of_suggestion:][::-1]

    similarities = []
    for i in indexes:
        sim = cosine_similarity([node], [nodes[i]])
        similarities.append(sim)
    return zip(indexes, similarities)


def get_urls_dict(urls_path):
    urls_dict = {}
    with open(urls_path) as file:
        for line in file:
            name = line.split(";")[0]
            link = line.split(";")[1]
            urls_dict[name] = link.replace("\n", "")
    return urls_dict

def apply_analogy(origin_cuisine,
                  origin_dish,
                  destination_cuisine,
                  data_path = "./data/",
                  num_of_suggestion=3,
                  filters=None
                  ):
    """
    :param origin_cuisine: the cuisine known by the user
    :param origin_dish: the dish that the user like
    :param destination_cuisine: the cuisine for which the recommendation have to be computed
    :param data_path: the path to the folder "data"
    :param num_of_suggestion: the number of dished to be suggested
    :param filters: list of the filter that have to be applied
    :return: a list of lists with the following structure:
            [[<name of the 1° suggested dish>, <confidence>, <directory of the images>, <url to the recipe>], ....]
    """

    emb_path =    data_path + "embeddings/"
    images_path = data_path + "DatasetImages/"
    urls_path =   data_path + "urls.csv"
    filers_path = data_path + "Filters/"
    estension = ".csv"


    origin_cuisine = emb_path + origin_cuisine + estension
    destination_name = destination_cuisine
    destination_cuisine = emb_path + destination_cuisine + estension

    dish = search_dish_vector(origin_dish, origin_cuisine)
    orig = get_cuisine_vector(origin_cuisine)
    dest = get_cuisine_vector(destination_cuisine)


    info = np.subtract(dish, orig)
    recommendation = np.add(dest, info)

    matrix = get_dishes_matrix(destination_cuisine, filters, filers_path)
    points = closest_node(recommendation, matrix, num_of_suggestion)

    result = []

    urls_dict = get_urls_dict(urls_path)

    count = 1
    for index, sim in points:
        print("With confidence ", sim[0][0], " the " + str(count) + "° suggestion is:  ", end="")
        name = search_dish_name(matrix[index], destination_cuisine)
        print(colored(name, 'blue', attrs=['bold']))
        count += 1
        result.append([name, sim[0][0], images_path + destination_name + "/" + name + ".jpg", urls_dict[name]])

    return result



res = apply_analogy(origin_cuisine="spanish",
                    origin_dish="Flamenco eggs",
                    destination_cuisine="american",
                    num_of_suggestion=5,
                    filters=[])
                    #data_path="/home/umberto/Desktop/data/")

print(res)