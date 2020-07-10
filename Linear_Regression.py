# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 23:18:56 2020

@author: thomas.musieracki
"""
#Linear Regression is when you have a group of points on a graph, and you find a line that approximately resembles that group of points.
# A good Linear Regression algorithm minimizes the error_, or the distance from each point to the line. 
#A line with the least error is the line that fits the data the best. We call this a line of _best fit.

def get_y(m, b, x):
    y = m * x + b
    return y


def calculate_error(m, b, point):
    x_point, y_point = point
    y = m * x_point + b
    diff = abs(y - y_point)
    return diff

datapoints = [(1, 2), (2, 0), (3, 4), (4, 4), (5, 3)]

def calculate_all_error(m, b, points):
    total_error = 0
    for point in datapoints:
        point_error = calculate_error(m, b, point)
        total_error += point_error
    return total_error

possible_ms = [m * 0.1 for m in range(-100,101)]

possible_bs = [b * 0.1 for b in range(-200, 201)]

datapoints = [(1, 2), (2, 0), (3, 4), (4, 4), (5, 3)]
smallest_error = float("inf")
best_m = 0
best_b = 0
for m in possible_ms:
    for b in possible_bs:
        error = calculate_all_error(m, b, datapoints)
        if error < smallest_error:
            best_m = m
            best_b = b
            smallest_error = error 

print(best_m, best_b, smallest_error)

#Now we have seen that for this set of observations on the bouncy balls, the line that fits the data best has an m of 0.3 and a b of 1.7: