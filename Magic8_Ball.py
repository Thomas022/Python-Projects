"""Magic 8-Ball
The Magic 8-Ball is a popular toy developed in the 1950s for fortune-telling or advice seeking.

Write a magic8.py Python program that can answer any “Yes” or “No” question with a different fortune each time it executes."""
#Creating a Magic 8-Ball game using Controllflow if/elif/else

# importing random library
import random
random_number = random.randint(1,9)

#Setting Variables
name = " "
question = "Will i win the lottery?"
answer = ""

#Creating controllflow and answer varible
if random_number == 1:
  answer = "Yes - definitely"
elif random_number == 2:
  answer = "It is decidely so"
elif random_number == 3:
  answer = "Without a doubt"
elif random_number == 4:
  answer = "Reply hazy, try again"
elif random_number == 5:
  answer = "Ask again later"
elif random_number == 6:
  answer = "Better not tell you now"
elif random_number == 7:
  answer = "My sources say no"
elif random_number == 8:
  answer = "Outlook not so good"
elif random_number == 9:
  answer = "Very doubtful"
else:
  answer = "Error"

#Setting up error_controll is name variable is empyt + Magic 8-ball Answer
if name == "" or " ":
  print(f"Question: {question}")
else:
  print(f"{name} ask: {question}")
print(f"Magic 8-Ball's answer: {answer}")
print(random_number)
