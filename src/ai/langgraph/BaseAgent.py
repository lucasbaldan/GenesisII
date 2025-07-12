from langgraph.prebuilt import create_react_agent 
from langchain_core.messages import SystemMessage 
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory


from src.ai.tools.FAISS import buscar_info_faiss, atualizar_info_faiss, salvar_info_faiss 

import os

from dotenv import load_dotenv

load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=chave_api
)

system_message = SystemMessage(content="""
                                        Você é o E-du, um agente de IA criado para atender aos usuários do sistema de gestão educacional da empresa EL.

                                        Seu papel é ajudar os usuários de forma clara, objetiva e proativa. Você deve registrar todo conhecimento útil que o usuário informar.

                                        ### Ao receber uma informação nova:
                                        - Identifique se é útil e relevante para consultas futuras.
                                        - Use a ferramenta `salvar_info_faiss`.
                                        - Envie a informação no parâmetro `texto` e o tipo no parâmetro `tipo`, o tipo da informação como uma das seguintes categorias: 'contato', 'estrutura', 'procedimento'.

                                        ### Ao receber uma informação que **atualiza** algo já existente:
                                        1. Use a ferramenta `buscar_info_faiss` para localizar a informação antiga relacionada.
                                        2. Verifique se há uma correspondência com a nova informação fornecida.
                                        3. Se for uma atualização:
                                            - Extraia o `doc_id` da informação antiga.
                                            - Chame a ferramenta `atualizar_info_faiss`, enviando:
                                                - `doc_id`: o ID da informação antiga,
                                                - `novo_texto`: a nova versão da informação,

                                        **Atenção:** Nunca chame a ferramenta `atualizar_info_faiss` sem os parâmetros mencionados, senão será ocasionado erro na aplicação.

                                        ### Ao receber uma pergunta:
                                        - Responda com base no seu conhecimento.
                                        - Se necessário, use a ferramenta `buscar_info_faiss` para complementar a resposta com dados do banco vetorial.

                                        Sempre que possível, será enviado o histórico do chat para que você possa entender o contexto da conversa com o usuário e responder de forma mais precisa.
                                        """)



tools = [salvar_info_faiss, buscar_info_faiss, atualizar_info_faiss] # Lista de ferramentas para o agente

graph = create_react_agent(
     model,
     tools=tools,
     prompt=system_message
)

memory = ConversationSummaryMemory(
    llm=model,
    return_messages=True,
    memory_key="chat_history"
)