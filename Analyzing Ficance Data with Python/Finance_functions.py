# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def display_as_percentage(val):
  return '{:.1f}%'.format(val * 100)

# Write code here

def calculate_simple_return(start_price, end_price, dividend = 0):
  R = (end_price - start_price + dividend) / start_price
  return R
simple_return = calculate_simple_return(200,250, 20)
simple_return_per = display_as_percentage(simple_return)
print(f"The simple rate of return is {simple_return_per}%")

daily_return_a = 0.001
monthly_return_b = 0.022

# Write code here
#Aggregate Across TIme, time frame of the investment
daily_return_perze_a = display_as_percentage(daily_return_a)
Monthly_return_perze = display_as_percentage(monthly_return_b)
print(f"The daily rate of return for Investment A is {daily_return_perze_a}%")
print(f"The monthly rate of return for Investment B is {Monthly_return_perze}%")

#Converted the rate of return
def annualize_return(log_return, t):
  T = log_return * t
  return T
annual_return_a = annualize_return(daily_return_a, 252)
annual_return_a_per = display_as_percentage(annual_return_a)
print(f"The annual rate of return for Investment A is {annual_return_a_per}%")

annual_return_b = annualize_return(monthly_return_b, 12)
annual_return_b_per = display_as_percentage(annual_return_b)
print(f"The annual rate of return for Investment B is {annual_return_b_per}%")

# Import library here
from math import log

def display_as_percentage(val):
  return '{:.1f}%'.format(val * 100)

# Write code here
#Defininf a fucantion called calculate_log_return() that has 2 parameter
def calculate_log_return(start_price, end_price):
  R = log(end_price/start_price)
  return R

log_return = calculate_log_return(200,250)
log_return_perze = display_as_percentage(log_return)
print(f"The log rate of return is {log_return_perze}%")

def display_as_percentage(val):
  return '{:.1f}%'.format(val * 100)

daily_return_a = 0.001
monthly_return_b = 0.022

# Write code here
#Aggregate Across TIme, time frame of the investment
daily_return_perze_a = display_as_percentage(daily_return_a)
Monthly_return_perze = display_as_percentage(monthly_return_b)
print(f"The daily rate of return for Investment A is {daily_return_perze_a}%")
print(f"The monthly rate of return for Investment B is {Monthly_return_perze}%")

#Converted the rate of return
def annualize_return(log_return, t):
  T = log_return * t
  return T
annual_return_a = annualize_return(daily_return_a, 252)
annual_return_a_per = display_as_percentage(annual_return_a)
print(f"The annual rate of return for Investment A is {annual_return_a_per}%")

annual_return_b = annualize_return(monthly_return_b, 12)
annual_return_b_per = display_as_percentage(annual_return_b)
print(f"The annual rate of return for Investment B is {annual_return_b_per}%")

#Converts a Decimal Value into a percentage string
def display_as_percentage(val):
  return '{:.1f}%'.format(val * 100)

daily_returns = [0.002, -0.002, 0.003, 0.002, -0.001]

# Write code here
#Aggregate Across Time II
def convert_returns(log_returns, t):
  #Converts a list of log returns from one time scale to another.
  #Takes the average log return per period, then scales it by 't'
  #(the number of periods in the new time frame) to annualize
  #Formula: r = (sum of log returns / number of returns) * t
  T = (sum(log_returns) / len(log_returns)) * t
  return T

#Annualize the daily returns by multiplying the average daily
#by 252 (the typical number of trading days in a year)
annual_return = convert_returns(daily_returns,252)
print('The annual rate of return is', display_as_percentage(annual_return))

#Sum the daily 5 returns directly to get the total return for the week
# (no averaging needed since we already have exactly one week of data)
weekly_return = sum(daily_returns)
print('The weekly rate of return is', display_as_percentage(weekly_return))

import numpy as np

# Sample historical returns for Disney and CBS Stocks
returns_disney = [0.22, 0.12, 0.01, 0.05, 0.04]
returns_cbs = [-0.13, -0.15, 0.31, -0.06, -0.29]

# Calculate variance using numpy's built-in function
# (used here for comparison/verification against our manual calculation below)
variance_disney = np.var(returns_disney)
variance_cbs = np.var(returns_cbs)

# Write code here
# Example dataset used to test the custom variance function
dataset = [10, 8, 9, 10, 12]


def calculate_variance(dataset):
    # Step 1: calculate the mean(average) of the dataset
    mean = (sum(dataset) / len(dataset))
    numerator = 0
    for number in dataset:
        # Step 2: sum up the squared differences between each value and the mean
        # (this measures how far each point is from the average, squared so,
        # negative and positive differences don't cancel out)
        numerator += (number - mean) ** 2

        # Step 3: divide by the number of data points to get the average
        # squared deviation - this is the variance

    variance = numerator / len(dataset)
    return variance


# Apply the custom variance function to the stock return dataset
variance_disney = calculate_variance(returns_disney)
variance_cbs = calculate_variance(returns_cbs)

print('The variance of Disney stock returns is', variance_disney)
print('The variance of CBS stock returns is', variance_cbs)

from utils import calculate_variance
import numpy as np
# Import library here
from math import sqrt

def display_as_percentage(val):
  return '{:.1f}%'.format(val * 100)

returns_disney = [0.22, 0.12, 0.01, 0.05, 0.04]
returns_cbs = [-0.13, -0.15, 0.31, -0.06, -0.29]

stddev_disney = np.std(returns_disney)
stddev_cbs = np.std(returns_cbs)

# Write code here
dataset = [10, 8, 9, 10, 12]


def calculate_stddev(dataset):
  # Standard deviation is just the squarre root of variance
  # Step 1: get the variance using our previously built function
  variance = calculate_variance(dataset)
  # Step 2: take the square root to convert variance back into
  # the original units (variance squares the units, stddev undoes that)
  stddev = sqrt(variance)
  return stddev

# Apply the custom stddev function to the stock return datasets
stddev_disney = calculate_stddev(returns_disney)
stddev_cbs = calculate_stddev(returns_cbs)

print('The standard deviation of Disney stock returns is', display_as_percentage(stddev_disney))
print('The standard deviation of CBS stock returns is', display_as_percentage(stddev_cbs))

from utils import calculate_correlation
import numpy as np

returns_general_motors = [0.018, -0.005, -0.047, -0.009, -0.012, 0.003, -0.027, -0.014, 0.029, -0.062, 0.009]
returns_ford = [0.002, -0.004, -0.027, -0.022, -0.001, 0.002, -0.006, -0.017, 0.035, -0.029, 0.002]
returns_exxon_mobil = [0.008, 0.015, 0.009, 0.012, 0.003, -0.007, 0.006, 0.005, -0.048, 0.025, -0.012]
returns_apple = [-0.002, 0.007, -0.004, -0.004, 0.002, 0.013, -0.011, 0.017, -0.001, 0.012, 0.006]

corr_gm_ford = calculate_correlation(returns_general_motors, returns_ford)
print('The correlation coefficient between General Motors and Ford is', corr_gm_ford)

# Write code here
corr_gm_exon = calculate_correlation(returns_general_motors, returns_exxon_mobil)
print(f"The correlation coefficient between General Motors and ExxonMobil is {corr_gm_exon}")

corr_gm_apple = calculate_correlation(returns_general_motors, returns_apple)
print(f"The correlation coefficient between General Motors and Apple is {corr_gm_apple}")

corrcoef_matrix = np.corrcoef([returns_general_motors, returns_ford, returns_exxon_mobil, returns_apple])
print(f"the correlation of all is {corrcoef_matrix}")

from data import returns_general_motors, returns_ford, returns_exxon_mobil, returns_apple
from math import sqrt
import numpy as np


def calculate_correlation(set_x, set_y):
    # Sum of all values in each dataset
    sum_x = sum(set_x)
    sum_y = sum(set_y)

    # Sum of all squared values in each dataset
    sum_x2 = sum([x ** 2 for x in set_x])

    sum_y2 = sum([y ** 2 for y in set_y])

    # Sum of the product of each respective element in each dataset
    sum_xy = 0
    for xa, ya in zip(set_x, set_y):
        sum_xy += set_x * set_y

    # Length of dataset
    n = len(set_x)

    # Calculate correlation coefficient
    numerator = n * sum_xy - sum_x * sum_y
    denominator = sqrt((n * sum_x2 - sum_x ** 2) * (n * sum_y2 - sum_y ** 2))

    return numerator / denominator


# Function calls
print('The correlation coefficient between General Motors and Ford is',
      calculate_correlation(returns_general_motors, returns_ford))
print('The correlation coefficient between General Motors and ExxonMobil is',
      calculate_correlation(returns_general_motors, returns_exxon_mobil))
print('The correlation coefficient between General Motors and Apple is',
      calculate_correlation(returns_general_motors, returns_apple))

from utils import calculate_variance, calculate_stddev

def display_as_percentage(val):
  return '{:.1f}%'.format(val * 100)

annual_returns = [0.02, 0.05, -0.04, 0.04, 0.02, -0.02, 0.01, 0.03, 0.05, 0.02]

# Write code here

annual_returns_percentage = [display_as_percentage(val) for val in annual_returns]

print("The historical annual rates of return are:","," .join(annual_returns_percentage))

variance = calculate_variance(annual_returns)

print(f"The variance of the rates of return is {variance}")

stddev = display_as_percentage(calculate_stddev(annual_returns))

print(f"The standard deviation of the rates of return is {stddev}")




