import requests
import sqlite3 as sql
import json
import urllib
from random import randint

FILENAME = "test_recipe_03.db"

# ID set is used to ensure all recipes have unique ID
IDS = {-1}
APP_ID = "0255a605"
API_KEY = "f23a736c3c87e5e8fe252d6c82c8da38"
URL = f'https://api.edamam.com/search?/app_id=${APP_ID}&app_key=${API_KEY}'

def main():

    print()
    command = ''
    while command.lower() != 'q':
        print('1) Enter 1 or 2, 1- chose recipe based on a key word, 2- chose based on a health condition:')
        command = input("\t>> ")
        print()
        if command == '1':
            query_recipes()
        elif command == '2':
            function_health()
        else:
            break

def query_recipes():

    response = None
    success = False
    index = 0

    while not success:
        print("Please enter a keyword")
        key_word = input("\t>> ")
        data = make_request(get_url_q(key_word))
        data = data['hits']
        if len(data) > 0:
            success = True
        else:
            print(f'0 results for "{key_word}"')
            input("")

    index = display_recipe_labels(data, index)
    print(f"   Select Recipe # (1-{index})\n   (enter 'm' to see more)")
    select = select_from_index(index)
    # Allows user to request 20 more recipes with same keyword
    if select == 'm' and index == 20:
        _from = 20
        to = 40
        data2 = make_request(get_url_q(key_word, _from, to))
        data2 = data2['hits']
        index = display_recipe_labels(data2, index)
        # join the data of both requests together
        data += data2
        # selection has not yet been made
        select = -1
    select_recipe(data, index, select)

def display_recipe_labels(data, index):
    """
    Displays all recipe labels from a result of request.
    Returns the max index of list of recipes.
    """
    print()
    for recipe in data:
        index += 1
        print(f"   {index})", recipe['recipe']['label'])
    print()
    return index

def select_recipe_from_index(max_index):
    print(f"   Select Recipe # (1-{max_index})")
    return select_from_index(max_index)


def select_from_index(max_index):
    select = -1
    while select <= 0 or select > max_index:
        select = input("\t>> ")
        if select.lower() == 'q':
            return 'q'
        elif select.lower() == 'm':
            return 'm'
        try:
            select = int(select)
        except ValueError as e:
            print("Input must be an integer!")
            select = -1
    return select - 1

def filter_response(recipe):
    """
    Takes response object and returns dictionary with readable
    recipe data
    """
    curr_recipe = {
        "ingredients_line": recipe["ingredientLines"],
        "ingredients": recipe["ingredients"],
        "label": recipe["label"],
        "url": recipe["url"],
        "uri": recipe["uri"]}
    return curr_recipe


def display_recipe_dict(curr_recipe):
    """
    Displays dictionary curr_recipe.
    Dictionary curr_recipe keys include:
        - "ingredients_line"
        - "ingredients"
        - "label"
        - "url"
    """
    print()
    print("====================================================")
    print(f"{curr_recipe['label']}:")
    print("----------------------------------------------------")
    for line in curr_recipe["ingredients_line"]:
        print(f"    - {line}")
    print()
    print(f"Directions: {curr_recipe['url']}")
    print("====================================================")
    input()
def make_request(url):
    """
    Returns a request response from a given URL.
    """
    response = requests.get(url)
    data = response.json()
    return data

def get_url_q(key_word, _from=0, to=20):
    url = URL + f'&q=${key_word}&to={to}&from={_from}'
    return url


def get_url_r(uri):
    return URL + f'&r={uri}'

def select_recipe(data, max_index, select):
    """
    Select & save unsaved recipe.
    """
    # If select == -1, no selection has been made
    invalid = True
    while invalid:
        if select == -1:
            select = select_recipe_from_index(max_index)
        if select == 'm':
            display_recipe_labels(data, 0)
            select = select_recipe_from_index(max_index)
        if select == 'q':
            print()
            return
        try:
            select = int(select)
            invalid = False
        except ValueError:
            invalid = True
            select = -1

    recipe_response = data[select]
    recipe = recipe_response["recipe"]
    curr_recipe = filter_response(recipe)
    print(curr_recipe.values())


    values = curr_recipe.values()
    list_ingredients = str(values)

    list_ingredients = list_ingredients.split(" ")
    print(list_ingredients)
    print(list_ingredients[2])

    for i in list_ingredients:
        a = input('check the ingredients! Write here any ingredient you want to know if it is present in the recipe(if you dont wish to know the ingredient enter q):')
        if i == a:
            print('yes, there is', a, 'in this recipe')
        elif a == 'q':
            break
        else:
            print('no')
            break

    for i in range(0,10000):
        a = input('here:')
        if list_ingredients[i] == a:
            print('yes')
            break
        else:
            print('no')
            break

    display_recipe_dict(curr_recipe)



main()


