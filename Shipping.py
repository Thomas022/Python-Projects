"""Sal's Shipping
Sal runs the biggest shipping company in the tri-county area, Sal’s Shippers. Sal wants to make sure that every single one of his customers has the best and most affordable experience shipping their packages.
In this project, you’ll build a program that will take the weight of a package and determine the cheapest way to ship that package using Sal’s Shippers.

Sal’s Shippers has several different options for a customer to ship their package:

Ground Shipping, which is a small flat charge plus a rate based on the weight of your package
Ground Shipping Premium, which is a much higher flat charge, but you aren’t charged for weight
Drone Shipping (new), which has no flat charge, but the rate based on weight is triple the rate of ground shipping
Here are the prices:

Ground Shipping

Weight of Package	Price per Pound	Flat Charge
2 lb or less	$1.50	$20.00
Over 2 lb but less than or equal to 6 lb	$3.00	$20.00
Over 6 lb but less than or equal to 10 lb	$4.00	$20.00
Over 10 lb	$4.75	$20.00

Ground Shipping Premium

Flat charge: $125.00

Drone Shipping

Weight of Package	Price per Pound	Flat Charge
2 lb or less	$4.50	$0.00
Over 2 lb but less than or equal to 6 lb	$9.00	$0.00
Over 6 lb but less than or equal to 10 lb	$12.00	$0.00
Over 10 lb	$14.25	$0.00

Write a shipping.py Python program that takes the weight of a package and then calculates which method of shipping is the cheapest and how much it will cost to ship the package using Sal’s Shippers."""
#Task 1: define weight variable
weight = 41.5
#Task 2: Ground Shipping controll flow cost calculation
if weight <= 2:
  ppp = (weight * 1.50) + 20
  print(f"${ppp:.2f}")
elif weight <= 6:
  ppp = (weight * 3.00) + 20
  print(f"${ppp:.2f}")
elif weight <= 10:
  ppp = (weight * 4.00) + 20
  print(f"${ppp:.2f}")
else:
  ppp = (weight * 4.75) + 20
  print(f"${ppp:.2f}")

#Task 3: Setting up Ground Shipping Premium
Shipping_Premium = 125
print(f"${Shipping_Premium:.2f} Ground Shipping Premium")

#Task 4: Setting up Drone Shipping cost calculation
if weight <= 2:
  ppp = (weight * 4.5)
  print(f"${ppp:.2f}")
elif weight <= 6:
  ppp = (weight * 9)
  print(f"${ppp:.2f}")
elif weight <= 10:
  ppp = (weight * 12)
  print(f"${ppp:.2f}")
else:
  ppp = (weight * 14.25)
  print(f"${ppp:.2f}")
