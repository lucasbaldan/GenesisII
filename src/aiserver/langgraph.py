from langgraph.prebuilt import create_react_agent # FunÃ§Ã£o principal do LangGraph para criar agentes ReAct
from langchain_core.messages import SystemMessage # Para definir a mensagem de sistema (persona)
from langchain_core.tools import tool # Decorador para definir ferramentas
from langchain_openai import ChatOpenAI;
import os
from dotenv import load_dotenv

load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=chave_api
)

system_message = SystemMessage(content="""Você é o E-du, um agente de IA criado para atender aos usuários do sistema de gestão educacional da empresa EL.
                                Você deve saber que para alterar um horário de turma é necessário primeiro bloquear o período letivo e depois fazer as alterações pela tela /Secretaria/Horário/Horário Turma do módulo acadêmico da escola.
                                Você deve responder de forma clara e objetiva.
                                Se a resposta for muito longa, resuma-a e pergunte se o usuÃ¡rio quer mais informações.""")


tools = [] # Lista de ferramentas para o agente

graph = create_react_agent(
    model,
    tools=tools,
    prompt=system_message # Aplica a persona
)