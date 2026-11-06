# Ferramentas para acessar o modelo, montar instruções e extrair a resposta em texto.
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Permite configurar variáveis de ambiente, como a chave usada para acessar a API.
import os
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"]

# Configura o modelo de IA. A temperatura influencia a variedade das respostas.
llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0.7)

# Template da pergunta: {topico} será substituído pelo assunto digitado.
# Apesar do nome, Question_chain é apenas um template; sozinho, não chama a IA.
Question_chain = PromptTemplate.from_template(
    template = "Criar uma pergunta facil sobre esse tópico : {topico}"
)

# Template da resposta: {question} receberá a pergunta gerada na primeira etapa.
Answer_chain = PromptTemplate.from_template(
    template = "Entregar uma resposta clara para a pergunta : {question}"
)

# O operador | conecta as etapas: template -> modelo -> resposta em texto.
# StrOutputParser extrai o conteúdo textual retornado pelo modelo.
# Esta primeira cadeia gera uma pergunta sobre o tópico.
chain = Question_chain | llm | StrOutputParser()
# Esta segunda cadeia gera a resposta para a pergunta recebida.
chain1 = Answer_chain | llm | StrOutputParser()

# Executa as duas cadeias em sequência: a segunda depende do resultado da primeira.
def run_sequential_chain(topico):

    # Preenche {topico}, chama a IA e guarda a pergunta gerada como texto.
    # Use a cadeia completa: chamar apenas o template não executa o modelo.
    question = chain.invoke({"topico" : topico})
    # Passa a pergunta gerada para a segunda cadeia e guarda a resposta da IA.
    answer = chain1.invoke({"question" : question})

    # Devolve os dois textos em um dicionário para facilitar o acesso depois.
    return {
        "question" : question,
        "answer" : answer,
    }

# Solicita ao usuário o assunto que será usado para gerar a pergunta.
topico = input("Escolha um topico: ")

# Informa que a geração vai começar; as chamadas à API podem levar alguns segundos.
print("Carregando Cadeia")

# Executa o fluxo completo e recebe o dicionário com a pergunta e a resposta.
resultado = run_sequential_chain(topico)

# Esta mensagem aparece depois que as duas etapas terminam com sucesso.
print("Terminou")

# Acessa cada texto pela chave do dicionário e mostra os resultados no terminal.
print("Primeira Pergunta", resultado["question"])
print("Resposta", resultado["answer"])



