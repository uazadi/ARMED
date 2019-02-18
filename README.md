# ARMED
## Analogy-based Recommender system of multi-ethnic dishes

Recently, even in the smallest town of Italy can be found an increasing number of restaurants that offer dishes originated from __all over the world__. With such a heterogeneous offer it is likely that the average person will not know a priori which type of cuisine or more specifically which dishes will be likely to meet his/her taste.

The purpose of this project is to support the customers in this specific decision making step, by __suggesting them a dish of a cuisine never tasted before based on their preferences in a known cuisine__, as for example the cuisine of their home country.

The main features are:
* Exploit a __multi-modal embedding__ representation of dishes in order to accomplish the __analogical inference__ through which the recommendation is obtained;
* Keep into consideration __specific diets__ such as: vegetarian, vegan, dairy-free, ...
* Allow the users to __add their own recipes__ and use them to obtain the recommendations

### What is shared through this repository?
* The scripts that accomplish the __crawling process__ through which the recipes have been downloaded from [BBC Food](https://www.bbc.com/food) (available [here](https://github.com/uazadi/ARMED/tree/master/src/crawling));
* The jupyter notebook through which the __recepies and images embedding__ can be explored (available [here](https://github.com/uazadi/ARMED/tree/master/src/notebook_for_embedding)); 
* The __"ready-to-use" application__ comprehensive of the GUI that allows to exploit the main functionalities described above (available [here](https://github.com/uazadi/ARMED/tree/master/src))