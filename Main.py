import requests
import tkinter as tk
from bs4 import BeautifulSoup
import math
import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# from googlesearch import search

# Beautiful soup does not render JS so remember to inspect with JS off

def getBestRecipe(dish):
    #get list of all recipes
    query = 'https://www.allrecipes.com/search/results/?wt=' + dish
    r = requests.get(query)
    soup = BeautifulSoup(r.content, 'html5lib')
    cookbook = soup.findAll('article', attrs = {'class': 'fixed-recipe-card'})
    bestscore = 0
    bestrecipe = ''
    for recipe in cookbook:
        #section with all the info
        info = recipe.find('div', attrs = {'class': 'fixed-recipe-card__info'})
        rating = float(info.find('span', {'class': 'stars'})['data-ratingstars'])
        reviews = float(info.find('format-large-number')['number'])
        weightedScore = (rating+1/(5.001-rating))*(math.log(reviews))
        if weightedScore > bestscore:
            bestscore = weightedScore
            bestrecipe = recipe.find('a')['href']
        print(bestrecipe)
        return bestrecipe

def extractrecipe(recipe):
    r = requests.get(recipe)
    soup = BeautifulSoup(r.content, 'html5lib')
    #print(soup.prettify())
    shoppinglist = []
    if soup.find('body', attrs={'class': 'template-recipe'}):
        ingredientsList = soup.findAll('li', attrs={'class':'ingredients-item'})
        for ingredient in ingredientsList:
            shoppinglist.append(ingredient.find('span', attrs={'class':'ingredients-item-name'}).text.strip())
    else:
        ingredientsList = soup.findAll('label', attrs={'ng-class': '{true: \'checkList__item\'}[true]'})
        for ingredient in ingredientsList:
            shoppinglist.append(ingredient['title'])
    return shoppinglist
# for i in extractrecipe('https://www.allrecipes.com/recipe/162760/fluffy-pancakes/'):
#     print(i)

def getCartFromDishes(textboxInput):
    dishes = textboxInput.split('\n')
    shoppinglist = []
    for dish in dishes:
        ingredients = extractrecipe(getBestRecipe(dish))
        for ingredient in ingredients:
            shoppinglist.append(ingredient)
    return shoppinglist

def seperateQuantity(recipeElement):
    # cases to consider
    # 1(16ounce) package
    # 1 egg
    return None

def launchList():

    def getShoppingList():
        pd.set_option('display.max_columns', None)
        df = pd.DataFrame(columns=['ingredient', 'quantity', 'unit', 'details'])
        dishes = textbox1.get('1.0', 'end-1c')
        list = getCartFromDishes(dishes)
        for i in list:
            ingredient, quantity, unit, details = parsePhrase(i)
            df = df.append({'ingredient': ingredient,
                       'quantity': quantity,
                       'unit': unit,
                       'details': details},
                      ignore_index=True)
            textbox2.insert(tk.END, i+'\n')
        textbox2.insert(tk.END, df)
    root = tk.Tk()
    frame = tk.Frame(root, width = 200, height = 120)
    textbox1 = tk.Text(root, height=10, width=180)
    textbox1.grid()
    textbox2 = tk.Text(root, height = 30, width = 180)
    textbox2.grid()
    button = tk.Button(root, text='get ingredients', command = getShoppingList)
    button.grid()
    tk.mainloop()
frac = [u'¼', u'½', u'¾', u'⅓', '⅔', u'⅛', u'⅜', u'⅝', u'⅞', u'⅙', u'⅚', u'⅒']
common_meas = ['cup', 'cups', 'tablespoon', 'tablespoons', 'teaspoon', 'pound', 'lbs', 'pounds'
               'oz', 'ounce', 'ounces', 'ml', 'gram', 'litre', 'quart', 'pint', 'bottle', 'can' ]
common_adj = ['fresh', 'ground']
def parsePhrase(phrase):
    quantity = ""
    unit = ""
    details = []
    ingredient = ""
    phrase = phrase.replace("-","")
    parray = phrase.split(" ")
    inBracket = 0
    for element in parray:
        if element.isnumeric():
            quantity = quantity + element
        elif element.startswith('('):
            inBracket = 1
            details.append(element)
        elif inBracket:
            details.append(element)
        elif element.endswith(')'):
            inBracket = 0
            details.append(element)
        elif element in frac:
            quantity = quantity + element
        elif element in common_meas:
            unit = element
        elif element.endswith('ed') or element.endswith('ly'):
            details.append(element)
        elif element in common_adj:
            details.append(element)


        else:
            ingredient = ingredient + " " + element

    return ingredient, quantity, unit, details

launchList()



# print(len(scores))
# print(np.shape(np.asarray(scores)))
# fig1, ax1 = plt.subplots()
# fig2, ax2 = plt.subplots()
# fig3, ax3 = plt.subplots()
# x = np.linspace(0,len(scores)-1,len(scores))
# ax1.plot(x, np.asarray(scores))
# ax2.plot(x, np.asarray(ratings))
# ax3.plot(x, np.asarray(reviewnumbers))
# plt.show()
