from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


import os
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0.7)

"""Defining a prompt template

Use the PromptTemplate class to create a template named prompt with an instruction and a placeholder 
that is filled in at runtime. This template formats the user’s input into a complete prompt that the language model can understand."""

prompt = PromptTemplate.from_template("Explicar {Tema} in termos simples")

"""Creating a Chain

Create a chain named chain that links the prompt template, the language model, and a string output parser using the pipe operator (|) so each component passes its output to the next."""

chain = prompt | llm | StrOutputParser()

"""Executing the Chain

The topic variable is defined to collect the user input for the explanation.

Pass this input to the chain using .invoke() so it can generate the response, and store the result in a variable named response.

The print() statement is used to display the final explanation."""

#Get user input
Tema = input("Qual o tema: ")

#run the chain
response = chain.invoke({"Tema": Tema})

#print the response
print("\nResponse\n", response)