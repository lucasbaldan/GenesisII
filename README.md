# utilize o poetry para gerenciar as dependências do projeto
# utilize o docker para rodar o projeto com o mesmo ambiente do servidor

# COMANDOS ÚTEIS
- Para testar o código específico da IA com o LangChain, LangGraph e a interface do LangSmith, utilize o comando *langgraph dev* na pasta raiz do projeto

- Criar Migração para banco de dados SQL 
-> alembic revision --autogenerate -m "nome da migração"

- Subir as migrações para o banco de dados SQL
-> alembic upgrade head

-Rodar servidor local uvicorn sem Docker (se necessário)
-> uvicorn src.api.server:app --reload ou task run