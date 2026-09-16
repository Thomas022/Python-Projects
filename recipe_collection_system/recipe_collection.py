recipes = {
    "Chocolate Chip Cookies": {
        "cuisine_type": "American",
        "prep_time": 15,
        "cook_time": 12,
        "servings": 24,
        "ingredients": [
            "flour",
            "butter",
            "sugar",
            "eggs",
            "chocolate chips",
            "vanilla",
        ],
        "difficulty": "easy",
    },
    "Vegetable Pasta": {
        "cuisine_type": "Italian",
        "prep_time": 10,
        "cook_time": 20,
        "servings": 4,
        "ingredients": [
            "spaghetti",
            "eggs",
            "tomatoes",
            "parmesan",
            "black pepper",
            "olive oil",
        ],
        "difficulty": "medium",
    },
    "Chicken Stir Fry": {
        "cuisine_type": "Asian",
        "prep_time": 20,
        "cook_time": 15,
        "servings": 4,
        "ingredients": [
            "chicken",
            "soy sauce",
            "ginger",
            "garlic",
            "vegetables",
            "rice",
        ],
        "difficulty": "easy",
    },
    "Beef Wellington": {
        "cuisine_type": "British",
        "prep_time": 45,
        "cook_time": 40,
        "servings": 6,
        "ingredients": [
            "beef tenderloin",
            "mushrooms",
            "puff pastry",
            "eggs",
            "butter",
        ],
        "difficulty": "hard",
    },
}

all_ingredients = {
    "flour",
    "butter",
    "sugar",
    "eggs",
    "chocolate chips",
    "vanilla",
    "spaghetti",
    "tomatoes",
    "parmesan",
    "black pepper",
    "olive oil",
    "chicken",
    "soy sauce",
    "ginger",
    "garlic",
    "vegetables",
    "rice",
    "beef tenderloin",
    "mushrooms",
    "puff pastry",
}

cooking_history = [
    ("Chocolate Chip Cookies", "2024-01-15", 5),
    ("Vegetable Pasta", "2024-01-18", 4),
    ("Chicken Stir Fry", "2024-01-20", 5),
    ("Chocolate Chip Cookies", "2024-01-25", 5),
    ("Beef Wellington", "2024-02-01", 3),
]

cuisine_index = {}

for recipe_name, recipe_details in recipes.items():
    cuisine_type = recipe_details["cuisine_type"]
    if cuisine_type not in cuisine_index:
        cuisine_index[cuisine_type] = []
    cuisine_index[cuisine_type].append(recipe_name)

for recipe_name, recipe_details in recipes.items():
    print(f"{recipe_name} ({recipe_details['cuisine_type']}) - {recipe_details['difficulty']}")

quick_recipes = [
    recipe_name
    for recipe_name, recipe_details in recipes.items()
    if recipe_details["prep_time"] + recipe_details["cook_time"] < 30
]
print(quick_recipes)

easy_recipes = [
    recipe_name
    for recipe_name, recipe_details in recipes.items()
    if recipe_details["difficulty"] == "easy"
]
print(easy_recipes)


def recipes_with_ingredient(ingredient_to_find):
    return [
        recipe_name
        for recipe_name, recipe_details in recipes.items()
        if ingredient_to_find in recipe_details["ingredients"]
    ]


recipe_ratings = {}

for recipe_name in recipes:
    ratings = [
        rating
        for cooked_recipe, date, rating in cooking_history
        if cooked_recipe == recipe_name
    ]
    if ratings:
        recipe_ratings[recipe_name] = sum(ratings) / len(ratings)

recipe_counts = {recipe_name: 0 for recipe_name in recipes}

for recipe_name, date, rating in cooking_history:
    recipe_counts[recipe_name] = recipe_counts.get(recipe_name, 0) + 1

five_star_sessions = [
    (recipe_name, date)
    for recipe_name, date, rating in cooking_history
    if rating == 5
]
print(len(five_star_sessions))
