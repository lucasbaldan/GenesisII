import datetime
import uuid
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
            page_content="...",
            metadata={"id": str(uuid.uuid4()), "data": "2025-05-02", "tipo": "teste"}
        )
    ]
    faiss = FAISS.from_documents(documentos, embedding_model)
    faiss.save_local(caminho_faiss)


@tool
def salvar_info_faiss(texto: str, tipo: str) -> str | None:
    """
    Salva uma nova informação útil no banco vetorial FAISS para uso futuro.

    Parâmetros:
    - texto: o conteúdo informativo a ser registrado.
    - tipo: a categoria da informação. Deve ser uma palavra-chave como 'contato', 'estrutura', 'procedimento', etc.

    A IA deve inferir o tipo com base no conteúdo da informação.
    """
    try:
        doc_id = str(uuid.uuid4())  # Gerar um ID único para a memória

        documento = Document(
            page_content=texto,
            metadata={
                "id": doc_id,
                "tipo": tipo,
                "data": datetime.datetime.now().strftime("%Y-%m-%d")
            }
        )
        faiss.add_documents([documento], ids=[doc_id])
        faiss.save_local(caminho_faiss)
    
    except Exception as e:
        return(f"Erro ao salvar a informação no FAISS: {e}")


@tool
def buscar_info_faiss(pergunta_usuario: str) -> list[dict] | None | str:
    """
    Busca as informações mais relevantes no índice FAISS com base na pergunta feita pelo usuário.
    Retorna uma lista de dicionários contendo conteúdo, id e metadados.
    
    """
    try:
        resultados = faiss.similarity_search_with_score(pergunta_usuario, k=10)
        if resultados:
            return [
                {
                    "doc_id": r.metadata.get("id", "idnull"),
                    "page_content": r.page_content,
                    "score": score
                }
                for r, score in resultados if score < 1.5
            ]
        else:
            return None
    
    except Exception as e:
        return(f"Erro ao buscar informações no FAISS: {e}")

@tool
def atualizar_info_faiss(doc_id: str, novo_texto: str) -> str | None:
    """
    Exclui uma informação Salva no banco vetorial FAISS que está desatualizada e adiciona a nova informação atualização para uso futuro.

    Parâmetros:
    - doc_id: o ID do documento FAISS a ser deletado.
    - texto: o conteúdo atualizado a ser registrado.

    """
    try:
        old_doc = faiss.get_by_ids([doc_id])
        if not old_doc:
            return (f"Registro de memória não encontrado para o ID informado.")

        # Deletar o documento original
        faiss.delete([doc_id])

        documento_atualizado = Document(
            page_content=novo_texto,
            metadata={
                "id": doc_id,
                "tipo": old_doc[0].metadata.get("tipo", "desconhecido"),
                "data": datetime.datetime.now().strftime("%Y-%m-%d")
            }
        )

        faiss.add_documents([documento_atualizado], ids=[doc_id]) # Adicionar o novo documento ao índice
        faiss.save_local(caminho_faiss)
    
    except Exception as e:
        return(f"Erro ao atualizar a informação no FAISS: {e}")



model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=chave_api
)

system_message = SystemMessage(content="""
                                        Você é o E-du, um agente de IA criado para atender aos usuários do sistema de gestão educacional da empresa EL.

                                        Seu papel é ajudar os usuários de forma clara, objetiva e proativa. Você deve registrar todo conhecimento útil que o usuário informar, mantendo a base de dados sempre atualizada e precisa.

                                        ### Ao receber uma informação nova:
                                        - Identifique se é útil e relevante para consultas futuras.
                                        - Use a ferramenta `salvar_info_faiss`.
                                        - Classifique corretamente o tipo da informação como uma das seguintes categorias: 'contato', 'estrutura', 'procedimento', 'evento', etc.
                                        - Envie a informação no parâmetro `texto` e o tipo no parâmetro `tipo`.

                                        ### Ao receber uma informação que **atualiza** algo já existente:
                                        1. Use a ferramenta `buscar_info_faiss` para localizar a informação antiga relacionada.
                                        2. Verifique se há uma correspondência com a nova informação fornecida.
                                        3. Se for uma atualização:
                                            - Extraia o `doc_id` da informação antiga.
                                            - Chame a ferramenta `atualizar_info_faiss`, enviando:
                                                - `doc_id`: o ID da informação antiga,
                                                - `novo_texto`: a nova versão do conteúdo,

                                        **Atenção:** Nunca chame a ferramenta `atualizar_info_faiss` sem os parâmetros mencionados, senão será ocasionado erro na aplicação. Caso você não tenha as informações da memória, deve buscá-los primeiro usando a ferramenta `buscar_info_faiss`.

                                        ### Ao receber uma pergunta:
                                        - Responda com base no seu conhecimento.
                                        - Se necessário, use a ferramenta `buscar_info_faiss` para complementar a resposta com dados do banco vetorial.

                                        Sempre que possível, formate suas respostas em **Markdown** para facilitar a leitura.
                                        """)



tools = [salvar_info_faiss, buscar_info_faiss, atualizar_info_faiss] # Lista de ferramentas para o agente

graph = create_react_agent(
    model,
    tools=tools,
    prompt=system_message
)