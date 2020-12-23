#! python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''.split('\n')


class FoodItem:
    def __init__(self, line):
        self.ingredients = FoodItem.__getIngredients(line)
        self.allergens   = FoodItem.__getAllergens(line)

    def __getIngredients(line):
        endpos = line.find(' (contains')
        return line[:endpos].split(' ')
    
    def __getAllergens(line):
        startpos = line.find('(contains ')+len('(contains ')
        return line[startpos:-1].split(', ')

    def __repr__(self):
        return '{{ingredients: {}, allergens: {}}}'.format(self.ingredients, self.allergens)

class AllergenMap:
    def __init__(self, foods):
        
        self.allergenMap = {}
        self.allergens   = {}
        self.allergenIngredients = {}
        self.foods       = foods
        for food in foods:
            for allergen in food.allergens:
                if allergen not in self.allergenMap:
                    self.allergenMap[allergen] = []
                self.allergenMap[allergen] += [food]

    def calculatePossibleIngredientsFrom(self, ingredientList):
        ingredientSet = set(ingredientList)
        for allergen in self.allergens:
            if self.allergens[allergen] in ingredientSet:
                ingredientSet.remove(self.allergens[allergen])
        return ingredientSet
    
    def AddAllergenAsIngredient(self, allergen, ingredient):
        assert allergen not in self.allergens
        self.allergens[allergen] = ingredient
        assert ingredient not in self.allergenIngredients
        self.allergenIngredients[ingredient] = allergen

    def DeduceFoodPerAllergen(self):
        done = False
        while not done:
            newallergens = []
            for allergen in self.allergenMap:
                possibleIngredients = None
                for food in self.allergenMap[allergen]:
                    if possibleIngredients is None:
                        possibleIngredients = self.calculatePossibleIngredientsFrom(food.ingredients)
                    else:
                        possibleIngredients = possibleIngredients.intersection( self.calculatePossibleIngredientsFrom(food.ingredients) )
                assert len(possibleIngredients) > 0, 'No possible list of ingredients from {} and known allergens {}'.format(self.allergen[allergen], self.knownAllergens)
                if len(possibleIngredients) == 1:
                    self.AddAllergenAsIngredient(allergen, list(possibleIngredients)[0])
                    newallergens += [allergen]
            print('newallergens:', newallergens)
            done = len(newallergens) == 0
            for allergen in newallergens:
                del self.allergenMap[allergen]

        
    def __repr__(self):
        return '{{ allergenMap: {}, allergens: {}}}'.format( self.allergenMap, self.allergens )


foods = []
for line in readInput():
    foods += [ FoodItem( line ) ]

allergenMap = AllergenMap(foods)
allergenMap.DeduceFoodPerAllergen()
goodIngredientCount = 0
for food in foods:
    for ingredient in food.ingredients:
        if ingredient not in allergenMap.allergenIngredients:
            goodIngredientCount += 1
            
print(goodIngredientCount)
print(allergenMap)
