"""Knowledge base management with RAG"""
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

class KnowledgeManager:
    def __init__(self, knowledge_base_dir: str = 'data/knowledge_base'):
        self.knowledge_base_dir = knowledge_base_dir
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vectorstore = None
        self.qa_chain = None
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load and index knowledge base documents"""
        documents = []
        
        # Load all text files from knowledge base directory
        if os.path.exists(self.knowledge_base_dir):
            for filename in os.listdir(self.knowledge_base_dir):
                if filename.endswith('.txt'):
                    filepath = os.path.join(self.knowledge_base_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            'content': content,
                            'source': filename
                        })
        
        if not documents:
            print("Warning: No knowledge base documents found")
            return
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        texts = []
        metadatas = []
        for doc in documents:
            chunks = text_splitter.split_text(doc['content'])
            texts.extend(chunks)
            metadatas.extend([{'source': doc['source']} for _ in chunks])
        
        # Create vector store
        self.vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas,
            persist_directory=".chromadb"
        )
        
        # Create QA chain
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3,
            convert_system_message_to_human=True
        )
        
        template = """You are a helpful Global TV customer support assistant. Use the following context to answer the question. 
If you don't know the answer, say so politely and offer to connect them with a human agent.

Context: {context}

Question: {question}

Answer: """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt}
        )
    
    def get_answer(self, question: str) -> str:
        """Get answer from knowledge base"""
        if self.qa_chain is None:
            return "I apologize, but I'm having trouble accessing my knowledge base right now. Please contact our support team directly."
        
        try:
            result = self.qa_chain.invoke({"query": question})
            return result['result']
        except Exception as e:
            print(f"Error getting answer: {e}")
            return "I apologize, but I encountered an error. Please try rephrasing your question or contact our support team."
    
    def search_knowledge_base(self, query: str, k: int = 3) -> list:
        """Search knowledge base and return relevant documents"""
        if self.vectorstore is None:
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error searching knowledge base: {e}")
            return []