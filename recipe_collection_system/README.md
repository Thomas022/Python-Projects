# Recipe Collection System

A beginner-friendly Python project for organizing restaurant recipes and tracking cooking sessions. It practices dictionaries, sets, lists, tuples, loops, functions, and list comprehensions.

## Getting started

Install Python 3. No third-party packages are required.

From this project folder, run:

```bash
python3 recipe_collection.py
```

The script prints:

```text
Chocolate Chip Cookies (American) - easy
Vegetable Pasta (Italian) - medium
Chicken Stir Fry (Asian) - easy
Beef Wellington (British) - hard
['Chocolate Chip Cookies']
['Chocolate Chip Cookies', 'Chicken Stir Fry']
3
```

The last three lines show recipes taking less than 30 minutes, recipes marked easy, and the number of 5-star cooking sessions.

## Data structures

All project code and sample data are in `recipe_collection.py`.

| Variable | Purpose |
| --- | --- |
| `recipes` | Maps recipe names to cuisine type, prep time, cook time, servings, ingredients, and difficulty. Times are in minutes. |
| `all_ingredients` | A manually maintained set of the 20 unique sample ingredients. |
| `cooking_history` | A list of `(recipe_name, date, rating)` tuples, with dates formatted as `YYYY-MM-DD`. |
| `cuisine_index` | Groups recipe names into lists by cuisine type. |
| `quick_recipes` | Names of recipes whose prep time plus cook time is strictly less than 30 minutes. |
| `easy_recipes` | Names of recipes with difficulty equal to `"easy"`. |
| `recipe_ratings` | Average rating for each recipe with at least one cooking session. |
| `recipe_counts` | Number of cooking sessions per recipe, including zero for recipes not yet cooked. |
| `five_star_sessions` | `(recipe_name, date)` tuples for sessions rated 5. |

With the sample history, Chocolate Chip Cookies has been cooked twice; each other recipe has been cooked once. Their average ratings are 5.0, 4.0, 5.0, and 3.0 respectively, in the order shown above.

## Find recipes by ingredient

`recipes_with_ingredient(ingredient_to_find)` returns a list of matching recipe names without printing it. Matching uses the exact ingredient string and is case-sensitive.

```python
from recipe_collection import recipes_with_ingredient

matches = recipes_with_ingredient("butter")
print(matches)
# ['Chocolate Chip Cookies', 'Beef Wellington']
```

Importing the module also runs its existing top-level print statements. An ingredient that is not present returns an empty list.

## Update the collection

Edit the `recipes` dictionary to add or change recipes, and update `all_ingredients` when adding new ingredients. Add cooking sessions to `cooking_history` using the exact recipe name:

```python
("Vegetable Pasta", "2024-02-05", 5)
```

Run the script again to rebuild the cuisine index, filtered lists, ratings, and counts. Data is stored directly in the source file; the project does not currently provide interactive input or a database.
