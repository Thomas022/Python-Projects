#Len's Slice
#You work at Len’s Slice, a new pizza joint in the neighborhood. You are going to use your knowledge of Python lists to organize some of your sales data.

# Your code below:
toppings = ["pepperoni", "pineapple", "cheese", "sausage", "olives", "anchovies", "mushrooms"]

prices = [2, 6, 1, 3, 2, 7, 2]

#Occurrences of 2 in prices list + print
number_of_two = prices.count(2)

print(number_of_two)

#lengh of the toppings list in a variable
num_pizzas = len(toppings)

#Print the string "We sell [num_pizzas] different kinds of pizza!"
print(f"We sell {num_pizzas} differrent kinds of pizza!")

#Using the existing data about the pizza topping and prices create a new two-dimensional list called pizza_and_prices 

pizzas_and_price = [[2, "pepperoni"], [6, "pineapple"], [1, "cheese"], [3, "sausage"], [2, "olives"], [7, "anchovies"], [2, "mushrooms"]]

#sort pizzas_and_price ascending order
pizzas_and_price.sort()

print(pizzas_and_price)
#store the first element of pizza_and_prices in a variable
chepeast_pizza = pizzas_and_price[1]

#Man walks in the store and ask for the MOST EXPENSIVE pizza

pricest_pizza = pizzas_and_price[-1]

#Removing the pricest pizza, sold out

pizzas_and_price.remove([7, "anchovies"])

#adding new topping [2.5, "peppers"]

pizzas_and_price.insert(4, [2.5, "peppers"])

#Mice walk in the store and want three_cheapest pizza

three_cheapest = pizzas_and_price[:3]

print(three_cheapest)

