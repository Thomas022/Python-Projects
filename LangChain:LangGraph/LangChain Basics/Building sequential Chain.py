from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


import os
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0.7)

#Checkpoint 1
explanation_prompt = PromptTemplate.from_template(template = "Explicar tema {tema} em 2 frases")

#Creating summary prompttempalte Checkpoint 2
summary_prompt = PromptTemplate.from_template(template = "Fazer um Resumo desse tema: {explanation}")

#Building individual Processing Chains

explanation_chain = explanation_prompt | llm | StrOutputParser()
summary_chain = summary_prompt | llm | StrOutputParser()

#Implementing Sequential Chain Execution

def sequential_chain(tema):
    explanation = explanation_chain.invoke({"tema": tema})
    resumo = summary_chain.invoke({"explanation": explanation})

    return {
        "tema": tema,
        "explanation": explanation,
        "Summary": resumo,
    }

tema = input("Tema: ")
resultado = sequential_chain(tema)
print(resultado["explanation"])
print(resultado["Summary"])


