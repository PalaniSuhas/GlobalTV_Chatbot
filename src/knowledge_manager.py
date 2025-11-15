"""Smart Knowledge Manager with conversation context awareness - FIXED"""
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pinecone import Pinecone, ServerlessSpec
import os
import time
from docx import Document
from typing import List, Dict

class SmartKnowledgeManager:
    def __init__(self, knowledge_base_dir: str = 'data/knowledge_base'):
        self.knowledge_base_dir = knowledge_base_dir
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.vectorstore = None
        self.llm = None
        self.index_name = "globaltv-kb"
        self.load_knowledge_base()
    
    def extract_text_from_docx(self, filepath: str) -> str:
        """Extract text from a .docx file"""
        try:
            doc = Document(filepath)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
            return '\n'.join(text)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ""
    
    def load_knowledge_base(self):
        """Load and index knowledge base documents"""
        documents = []
        
        if os.path.exists(self.knowledge_base_dir):
            for filename in os.listdir(self.knowledge_base_dir):
                filepath = os.path.join(self.knowledge_base_dir, filename)
                
                if filename.endswith('.txt'):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            documents.append({
                                'content': content,
                                'source': filename
                            })
                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
                
                elif filename.endswith('.docx'):
                    content = self.extract_text_from_docx(filepath)
                    if content:
                        documents.append({
                            'content': content,
                            'source': filename
                        })
        
        if not documents:
            print("Warning: No knowledge base documents found")
            return
        
        print(f"Loaded {len(documents)} documents from knowledge base")
        
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
        
        print(f"Created {len(texts)} text chunks for vector store")
        
        try:
            api_key = os.getenv("PINECONE_API_KEY")
            if not api_key:
                print("Error: PINECONE_API_KEY not found in environment variables")
                return
            
            pc = Pinecone(api_key=api_key)
            existing_indexes = [index.name for index in pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                print(f"Creating Pinecone index: {self.index_name}")
                pc.create_index(
                    name=self.index_name,
                    dimension=768,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
                while not pc.describe_index(self.index_name).status['ready']:
                    time.sleep(1)
                print(f"Index {self.index_name} created successfully")
            else:
                print(f"Using existing Pinecone index: {self.index_name}")
            
            self.vectorstore = PineconeVectorStore.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas,
                index_name=self.index_name
            )
            print("Vector store created successfully with Pinecone")
            
        except Exception as e:
            print(f"Error creating Pinecone vector store: {e}")
            return
        
        # Initialize LLM
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                temperature=0.2
            )
            print("LLM initialized successfully")
        except Exception as e:
            print(f"Error initializing LLM: {e}")
    
    def get_answer(self, question: str, conversation_history: List[Dict] = None) -> str:
        """Get answer from knowledge base with conversation context"""
        if self.vectorstore is None or self.llm is None:
            return """I apologize, but I'm having trouble accessing my knowledge base right now. 

**Please contact our support team:**
- **Phone**: 1-800-GLOBAL-TV (1-800-456-2258)
- **Email**: webmaster@globaltv.com"""
        
        try:
            # Search for relevant documents
            relevant_docs = self.vectorstore.similarity_search(question, k=5)
            
            if not relevant_docs:
                return """I couldn't find specific information about that in my knowledge base.

**Please contact our support team for assistance:**
- **Phone**: 1-800-GLOBAL-TV (1-800-456-2258)
- **Email**: webmaster@globaltv.com"""
            
            # Format context from documents
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Format conversation history
            chat_history = ""
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    role = msg.get('role', 'user')
                    content = msg.get('content', '')
                    if content and len(content) < 500:  # Avoid very long messages
                        chat_history += f"{role.upper()}: {content}\n\n"
            
            # Enhanced prompt with context awareness
            prompt = f"""You are a helpful Global TV customer support assistant.

CRITICAL RULES:
1. NEVER ask for information the user has ALREADY provided in the conversation history
2. Review the conversation history BEFORE responding
3. Acknowledge information they've shared: "Based on what you told me about your [device/issue]..."
4. Only ask for information that is MISSING and NECESSARY
5. Keep responses concise and helpful - don't repeat troubleshooting steps unnecessarily
6. If user says "thanks", "that helped", or similar - keep response SHORT and friendly
7. Use the Knowledge Base Context to provide accurate, specific answers

Conversation History (Review this carefully):
{chat_history}

Knowledge Base Context:
{context}

Current Question: {question}

Instructions:
- Check conversation history for already-provided information
- Give a helpful answer based on Knowledge Base + conversation context
- Be conversational and natural
- Don't be repetitive

Response:"""
            
            # Get response from LLM
            response = self.llm.invoke(prompt)
            
            # Extract text from response
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
            
        except Exception as e:
            print(f"Error getting answer: {e}")
            import traceback
            traceback.print_exc()
            
            return """I apologize, but I encountered an error searching for that information. 

**Please try:**
1. Rephrasing your question
2. Being more specific about your issue

**Or contact our support team:**
- **Phone**: 1-800-GLOBAL-TV (1-800-456-2258)
- **Email**: webmaster@globaltv.com"""
    
    def search_knowledge_base(self, query: str, k: int = 5) -> list:
        """Search knowledge base and return relevant documents"""
        if self.vectorstore is None:
            return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return [doc.page_content for doc in results]
        except Exception as e:
            print(f"Error searching knowledge base: {e}")
            return []