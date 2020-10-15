import math
import pandas
import unidecode
import numpy as np
frac = [u'¼', u'½', u'¾', u'⅓', '⅔', u'⅛', u'⅜', u'⅝', u'⅞', u'⅙', u'⅚', u'⅒']
common_meas = ['cup', 'cups', 'tablespoon', 'tablespoons', 'teaspoon', 'pound', 'lbs', 'pounds'
               'oz', 'ounce', 'ounces', 'ml', 'gram', 'litre', 'quart', 'pint', 'bottle', 'can' ]
common_adj = ['fresh', 'ground']
# 1  fresh mango - peeled, pitted, and chopped
# ¼ cup finely chopped red bell pepper
# ½  Spanish onion, finely chopped

phrase = "1  fresh mango - peeled, pitted, and chopped"
# phrase = phrase.replace(",", "")
# phrase.strip("-")

parray = phrase.split(" ")
#[quantity, unit, ingredient, detail]
tags = np.zeros((len(parray),4))
quantity = ""
unit = ""
details = []
ingredient = ""
for element in parray:
    if element.isnumeric():
        quantity = quantity + element
    elif element in frac:
        quantity = quantity + element
    elif element in common_meas:
        unit = element
    elif element.endswith('ed') or element.endswith('ly'):
        details.append(element)
    elif element in common_adj:
        details.append(element)
    else:
        ingredient = element

