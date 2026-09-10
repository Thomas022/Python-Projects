#Gradebook
#You are a student and you are trying to organize your subjects and grades using Python. Let’s explore what we’ve learned about lists to organize your subjects and scores.

last_semester_gradebook = [["politics", 80], ["latin", 96], ["dance", 97], ["architecture", 65]]

# Your code below: 

#Task 1: Create a list called subjects
subjects = ["physics", "calculus", "poetry", "history"]

#Task 2: Create a list called grades
grades = [98, 97, 85, 88]

#Task 3: Manually creating a 2D-List
gradebook = [["physics", 98], ["calculus", 97], ["poetry", 85], ["history", 88]]

#Task 4: Print Gradebook
print(f"Current Grades: {gradebook}")

#Task 5: Using append() method to add list with values
gradebook.append(["computer science", 100])

#Task 6: using Append() method again
gradebook.append(["visual arts", 93])

#Task 7: accessing the Index of a grade in the list to increase it by 5
gradebook[-1][-1] = 98

#Task 8: Changing grade method and removeing the value for "poetry"
gradebook[2].remove(85)

#Task 9: Using the append method to add "Pass" in the place of the removed value
gradebook[2].append("Pass")

#Task 10: Adding the last_semester_gradebook to currently gradebook
full_gradebook = gradebook + last_semester_gradebook

print(f"All Grades: {full_gradebook}")
