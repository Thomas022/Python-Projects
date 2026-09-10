"""Student Grade Tracker
Apply core Python programming concepts, including variables, data types, conditionals, loops, and functions, to create a functional grade tracking system.

Practice using Codex CLI to generate and improve code while maintaining an understanding of fundamental programming principles.

By the end of this lab, you’ll have created a working program that demonstrates proper use of variables, control flow, loops, functions, and Python naming conventions."""

def convert_to_letter_grade(score):
    """Convert a numeric test score to a letter grade.

    Args:
        score: The numeric test score to evaluate.

    Returns:
        A string containing the corresponding letter grade from A through F.
    """
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


student_name = "Maya Thompson"
student_age = 20
student_gpa = 3.75
is_full_time = True
test_score_1 = 92
test_score_2 = 85
test_score_3 = 78
test_score_4 = 96
test_score_5 = 88
total_score = test_score_1 + test_score_2 + test_score_3 + test_score_4 + test_score_5
average_score = total_score / 5

if student_gpa >= 3.5:
    grade_status = "Deans List"
elif student_gpa >= 3.0:
    grade_status = "Good Standing"
elif student_gpa >= 2.0:
    grade_status = "Passing"
else:
    grade_status = "Academic Probation"

print(f"Student Name: {student_name}")
print(f"Student Age: {student_age}")
print(f"Student GPA: {student_gpa}")
print(f"Full-Time Student: {is_full_time}")
print(f"Acedemic Status: {grade_status}")
print()

print("Grade Report :")
print(f"Test 1: {test_score_1} ({convert_to_letter_grade(test_score_1)})")
print(f"Test 2: {test_score_2} ({convert_to_letter_grade(test_score_2)})")
print(f"Test 3: {test_score_3} ({convert_to_letter_grade(test_score_3)})")
print(f"Test 4: {test_score_4} ({convert_to_letter_grade(test_score_4)})")
print(f"Test 5: {test_score_5} ({convert_to_letter_grade(test_score_5)})")
print(f"Average Score: {average_score:.2f}")
print()
print(f"Overall Average: {average_score:.2f} ({convert_to_letter_grade(average_score)})")
