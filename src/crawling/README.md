The scripts that accomplish the __crawling process__ through which the recipes have been downloaded from [BBC Food](https://www.bbc.com/food) (available [here](https://github.com/uazadi/ARMED/tree/master/src/crawling)):

* ingrs_list_creator.py create a list of all the ingredients available [here](https://www.bbc.com/food/ingredients/a-z/a/1#featured-content)
* bbc_filter_creators.py create a list of dish for nine categories: "dairy_free", "egg_free", "gluten_free", "nut_free", "pregnancy_friendly", "vegan", "vegetarian", "low_Glycemic_Index", "Low_calorie"
* bbc_dishes_list.py download the recipes from BBC food iff there is an image attached for each cuisine.
* add_dishes_list.py download all the string related to the ingredient that are not included in the list of ingredients that can be downloaded using "ingrs_list_creator.py"
