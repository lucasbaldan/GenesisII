import datetime
from langgraph.prebuilt import create_react_agent # FunÃ§Ã£o principal do LangGraph para criar agentes ReAct
from langchain_core.messages import SystemMessage # Para definir a mensagem de sistema (persona)
from langchain_core.tools import tool # Decorador para definir ferramentas
from langchain_openai import ChatOpenAI;
from langchain_community.embeddings import OpenAIEmbeddings # Para embeddings
from langchain_community.vectorstores import FAISS # Para armazenar os embeddings
from langchain.schema import Document # Para definir documentos a serem gravados no FAISS
import os
from dotenv import load_dotenv

load_dotenv()
chave_api = os.getenv("OPENAI_API_KEY")
caminho_faiss = os.getenv("FAISS_PATH")

embedding_model = OpenAIEmbeddings()

if os.path.exists(caminho_faiss):
    faiss = FAISS.load_local(caminho_faiss, embedding_model, allow_dangerous_deserialization=True)
else:
    documentos = [
        Document(
            page_content="O nome do setor responsável pela tecnologia da secretaria de educação é o Setor de Informática Educacional",
            metadata={"origem": "sistema", "data": "2025-05-02", "tipo": "contato"}
        )
    ]
    faiss = FAISS.from_documents(documentos, embedding_model)
    faiss.save_local(caminho_faiss)


@tool
def salvar_info_faiss(texto: str, tipo: str):
    """
    Salva uma nova informação útil no banco vetorial FAISS para uso futuro.

    Parâmetros:
    - texto: o conteúdo informativo a ser registrado.
    - tipo: a categoria da informação. Deve ser uma palavra-chave como 'contato', 'estrutura', 'procedimento', etc.

    A IA deve inferir o tipo com base no conteúdo da informação.
    """
    documento = Document(
        page_content=texto,
        metadata={
            "origem": "usuario",
            "tipo": tipo,
            "data": datetime.now().strftime("%Y-%m-%d"),
        }
    )
    faiss.add_documents([documento])
    faiss.save_local(caminho_faiss)

@tool
def buscar_info_faiss(pergunta_usuario: str) -> list[str] | None:
    """Busca as informação mais relevantes no índice FAISS com base na pergunta feita pelo usuário."""
    resultados = faiss.similarity_search(pergunta_usuario, k=3)
    if resultados:
        return [r.page_content for r in resultados] 
    else:
        return None



model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=chave_api
)

system_message = SystemMessage(content="""
                                            Você é o E-du, um agente de IA criado para atender aos usuários do sistema de gestão educacional da empresa EL.
                                            Você deve responder de forma clara e objetiva. 
                                            Sempre que o usuário fornecer uma informação nova e útil que possa ser usada para consultas futuras, salve a informação usando a ferramenta `salvar_info_faiss`, você deve:
                                            - Identificar o tipo da informação com uma das categorias: 'contato', 'estrutura', 'procedimento', 'evento', etc.
                                            - Preencher esse tipo corretamente no parâmetro 'tipo'.
                                            
                                            Se a resposta for muito longa, resuma-a e pergunte se o usuário quer mais informações.
                                            """)



tools = [salvar_info_faiss, buscar_info_faiss] # Lista de ferramentas para o agente

graph = create_react_agent(
    model,
    tools=tools,
    prompt=system_message
)