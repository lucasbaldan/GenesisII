from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    TextLoader,
)

class DocsLoaders:
    """
    Classe base para carregadores de documentos.
    Diferentes tipos de carregamento de documentos.
    """
    def __init__(self, doc_path: str):
        
        self.caminho = Path(doc_path)
        self.loaderErrors = []

        if not self.caminho.exists():
            self.loaderErrors.append(f"Arquivo não encontrado")
        if not self.caminho.is_file():
            raise ValueError(f"O caminho fornecido não é um arquivo válido")
        if self.caminho.name.__len__() < 1:
            raise ValueError(f"Não é possível carregar um documento com o nome vazio")
        self.loaderErrors.append(f"Caminho processado -> {doc_path}") if self.loaderErrors else None
        
        self.extensao = self.caminho.suffix.lower()
        self.nome = self.caminho.name.strip()
        self.result: List[Document] = []

    def PDFLoader(self) -> None:
        """
        Carrega um documento PDF e o processa em chunks.
        """
        documento = UnstructuredPDFLoader(str(self.caminho)).load()

        self.result = documento
        self.normalize()

    def MSWordLoader(self) -> None:
        """
        Carrega um documento Word e o processa em chunks.
        """
        documento = UnstructuredWordDocumentLoader(str(self.caminho)).load()

        self.result = documento
        self.normalize()

    def MSPowerPointLoader(self) -> None:
        """
        Carrega um documento PowerPoint e o processa em chunks.
        """
        documento = UnstructuredPowerPointLoader(str(self.caminho)).load()

        self.result = documento
        self.normalize()

    def TxtLoader(self) -> None:
        """
        Carrega um documento de texto TXT e o processa em chunks.
        """
        documento = TextLoader(str(self.caminho), autodetect_encoding=True).load()

        self.result = documento
        self.normalize()

    def normalize(self) -> None:
        """
        Normaliza o conteúdo do documento, removendo espaços em branco extras e quebras de linhas que bugam o chunker.
        """
        for doc in self.result:
            linhas = doc.page_content.splitlines()
            doc.page_content = " ".join(linha.strip() for linha in linhas if linha.strip())