# ELENA and Sebastian and ELENA Code
# This code matches a list of ingredients with ingredients in a recipe and tells you which ones you have to go buy
# still working on extending functionality search


import requests
import sqlite3 as sql
import json
import urllib
from random import randint
from itertools import compress

FILENAME = "test_recipe_03.db"
con = sql.connect(FILENAME)
C = con.cursor()

# ID set is used to ensure all recipes have unique ID
IDS = {-1}
APP_ID = "a395a114"
API_KEY = "8a66976d95a0a0fe1b484360704840a6"
URL = f'https://api.edamam.com/search?/app_id=${APP_ID}&app_key=${API_KEY}'


def main():
    """
    This program allows the user to search for recipes online using the
    Edamam API. It also allows the user to save lookup info for favorite
    recipes into a database. Finally, the user can look up saved recipes.
    """
    print()
    command = ''
    while command.lower() != 'q':
        print("1) Find New Recipe")
        command = input("\t>> ")
        print()
        if command == '1':
            query_recipes()
    C.close()


def query_recipes():
    response = None
    success = False
    index = 0
    while not success:
        print("Please enter a keyword")
        key_word = input("\t>> ")
        data = make_request(get_url_q(key_word))
        data = data['hits']
        # print(data[1].items())
        if len(data) > 0:
            success = True
        else:
            print(f'0 results for "{key_word}"')
            input("")

        fridge2 = input(
            'Write a list of the food you have on your fridge here and separated by a coma:')  # what if we did the ingredient list like this?
        fridge = [fridge2.split(', ')]
        print(fridge)

        fridge_food = ["bacon", 'bread', 'mayonnaise', 'lettuce', 'tomato', 'sea salt', 'black pepper', "water"]

        print(sort_recipes(data, fridge_food))

        '''for recipe_name in sort_recipes.keys():
            print(get_name(recipe))
            print("-----------------------------------------------------")
            print("you have ", sum(food_match(fridge_food, recipe)),"/", len(food_match(fridge_food, recipe)), " of the ingredients for this recipe")
            print(shopping_list(fridge_food, recipe))  
            print(get_uri(recipe))              #if yes change here 
            print(get_food_in_recipe_percetage(fridge_food, recipe))
            print("-----------------------------------------------------")
            print("-----------------------------------------------------")
            print("-----------------------------------------------------")'''


def shopping_list(fridge_food, recipe):
    food_in_recipe = food_match(fridge_food, recipe)
    shop_items = list(compress(get_food(recipe), [not elem for elem in food_in_recipe]))
    if len(shop_items) == 0:
        return shop_items
        print("You have all the ingredients you need for this recipe")
    return shop_items


def food_match(fridge_food, recipes):
    food_in_recipe = []
    for food in get_food(recipes):
        if " " in food:
            for i in food.split():
                if i in fridge_food:
                    food_in_recipe.append(True)
                    break

            food_in_recipe.append(False)

        else:
            food_in_recipe.append(food in fridge_food)

    return food_in_recipe


def get_uri(recipe):
    return recipe['recipe']['uri']


def get_name(recipe):
    return recipe['recipe']['label']


def get_food(recipes):
    ingredients_list = []
    for food in recipes["recipe"]["ingredients"]:
        ingredients_list.append(food["food"])
    return ingredients_list


def get_food_in_recipe_percetage(fridge_food, recipe):
    return sum(food_match(fridge_food, recipe)) / len(food_match(fridge_food, recipe))


def sort_recipes(data, fridge_food):
    sorted_recipes = {}
    n = 0
    for recipe in data:
        n += 1
        print(get_name(recipe))
        sorted_recipes[get_name(recipe)] = [get_food_in_recipe_percetage(fridge_food, recipe)]
    print(sorted_recipes)
    return sorted(sorted_recipes.items(), key=lambda item: item[1], reverse=True)


"""-----------------------MAKE REQUESTS--------------------------"""


def make_request(url):
    """
    Returns a request response from a given URL.
    """
    response = requests.get(url)
    data = response.json()
    return data


def get_url_q(key_word):
    url = URL + f'&q=${key_word}'  # I deleted here the range of the results, bc I think it makes more sense to 'look' at all of the recipes and the select the ones with the highest sc
    return url


def get_url_r(uri):
    return URL + f'&r={uri}'

