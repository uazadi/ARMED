import PIL
import json
from shutil import copyfile
import numpy as np
from keras import Model
from keras.layers import Dense, Input
from keras.applications.mobilenet import MobileNet
from PIL import Image


def get_embedder(num_of_ingrs, model_path):
    input_img = Input(shape=(num_of_ingrs,))
    encoded = Dense(50, activation='relu')(input_img)
    decoded = Dense(num_of_ingrs, activation='sigmoid')(encoded)
    autoencoder = Model(input_img, decoded)
    autoencoder.load_weights(model_path)

    # Removing Decoder layer
    pop_layer(autoencoder)
    embedder = Model(inputs=autoencoder.input, outputs=autoencoder.layers[-1].output)

    return embedder


def image_preprocessing(image_path):
    img = Image.open(image_path)
    img = img.convert("RGB")
    img = img.resize((224, 224), PIL.Image.ANTIALIAS)
    im2arr = np.array(img)
    im2arr = im2arr / 255
    return im2arr


def pop_layer(model):
    if not model.outputs:
        raise Exception('Sequential model cannot be popped: model is empty.')

    model.layers.pop()
    if not model.layers:
        model.outputs = []
        model.inbound_nodes = []
        model.outbound_nodes = []
    else:
        model.layers[-1].outbound_nodes = []
        model.outputs = [model.layers[-1].output]
    model.built = False


def cnn():
    base_model = MobileNet(input_shape=(224, 224, 3),
                           include_top=True,
                           weights='imagenet')

    # Changing the topology of the network
    pop_layer(base_model)
    model = Model(inputs=base_model.input, outputs=base_model.layers[-5].output)

    return model


def add_new_dish(name,
                 cuisine,
                 ingredients,
                 path_image,
                 data_path="./data/"
                 ):
    """
    :param name: the name of the new dish
    :param cuisine: the cuisine of the new dish
    :param ingredients: the ingredient of the new dish. A string with the following structure is expeceted: <ingr1>;<ingr2>;...
    :param path_image: the path to the image related to the new dish
    :param data_path: the path to the folder data
    """

    path_ingredients =   data_path + "Ingredients.json"
    path_word_embedder = data_path + "auto_enconder.h5"
    images_path =        data_path + "DatasetImages/"
    emb_path =           data_path + "embeddings/"

    with open(path_ingredients, "r") as file:
        json1_str = file.read()
        dict_ingredients = json.loads(json1_str)
    sparse_vec = list(np.zeros(len(dict_ingredients)))

    # Ingredient embedding
    ingrs = ingredients.split(";")[:-1]

    for i in range(len(ingrs)):
        sparse_vec[dict_ingredients[ingrs[i]]] = 1
    row = np.array(sparse_vec, dtype='int32')
    embedder = get_embedder(len(dict_ingredients), path_word_embedder)
    re_embedding = str(list(embedder.predict(np.array([row], dtype='int32'))[0]))[1:-1].replace(",", ";").replace(" ", "")

    # Image embedding
    model = cnn()
    image = image_preprocessing(path_image)
    im_embedding = str(list(model.predict(np.array([image]))[0]))[1:-1].replace(",", ";").replace(" ", "")

    # Save image
    copyfile(path_image, images_path + cuisine + "/" + name + ".jpg")

    with open(emb_path + cuisine + ".csv", "a") as file:
        string = name + ";" + re_embedding + ";" + im_embedding
        file.write(string + "\n")


#add_new_dish(name="DishAddedForTest",
#             cuisine="african",
#             ingredients="tomatoes;thyme;linguine;tinned tuna;artichoke;chilli sauce;chicken thigh",
 #            path_image="/home/umberto/Pictures/DoctorWho.jpg")
             #path_ingredients="/home/umberto/Desktop/data/")
