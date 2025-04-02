from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

import os

class DocumentQA:
    def __init__(self):
        self.persist_directory = "docs_index"
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        if not os.path.exists(self.persist_directory):
            self._index_documents()
        self.db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        prompt = ChatPromptTemplate.from_template(
            "Answer the following question based on the provided context:\n\n{context}\n\nQuestion: {input}"
        )
        self.chain = create_stuff_documents_chain(self.llm, prompt)

    # ***May be add Reranking later on***
    def answer_query(self, query):
        docs = self.db.similarity_search(query, k=3)
        return self.chain.invoke({"input": query, "context": docs})
