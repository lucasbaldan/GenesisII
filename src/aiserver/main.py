import os;
from dotenv import load_dotenv;
from langchain_openai import ChatOpenAI;
from langchain_core.prompts import ChatPromptTemplate;
from langchain_core.output_parsers import StrOutputParser;
from langchain_core.messages import SystemMessage, HumanMessage;


load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")

# mensagens = [
#     SystemMessage("Traduza o texto a seguir para o inglês"),
#     HumanMessage("Olá, esse é o meu primeito teste utilizando o LangChain e python"),
# ]
modelo = ChatOpenAI(api_key=chave_api, model="gpt-3.5-turbo", temperature=0.7)
parser = StrOutputParser()


template_mensagens = ChatPromptTemplate.from_messages([
    ("system", "Traduza o texto a seguir para o inglês."),
    ("user", "{texto}"),
])

chain = template_mensagens | modelo | parser

response = chain.invoke({"texto": "Olá, esse é o meu primeito teste utilizando o LangChain e python"})
print(response)