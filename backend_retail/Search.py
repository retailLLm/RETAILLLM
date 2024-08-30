!pip install Flask-Cors
!pip install flask flask-cors pyngrok
from flask import Flask, request, jsonify
from flask_cors import CORS
from pyngrok import ngrok
import torch

app = Flask(__name__)
CORS(app)

!pip install chromadb
!pip install langchain
!pip install langchain_community
!pip install sentence_transformers
!pip install transformers
!pip install accelerate
!pip install bitsandbytes
!pip install chromadb
import pandas as pd

from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

# Hiding warnings
import warnings
warnings.filterwarnings("ignore")
from langchain_community.document_loaders.csv_loader import CSVLoader
# loader = CSVLoader(file_path="product.csv")
loader = CSVLoader(file_path="test1.csv", encoding="latin-1")
document = loader.load()
print(document)
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,
                                chunk_overlap = 20)
splitted_texts = splitter.split_documents(document)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
chroma_database = Chroma.from_documents(splitted_texts,embedding_model,persist_directory = 'chroma_db')
retriever = chroma_database.as_retriever(search_type="similarity", search_kwargs={"k": 3})

retrieved_docs = retriever.invoke("Herbal hair oil")

len(retrieved_docs)
print(retrieved_docs[0].page_content)

!huggingface-cli login --token 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
from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
model = "meta-llama/Llama-2-7b-chat-hf"
quantization_config = BitsAndBytesConfig(
    load_in_8bit=True,
        device_map='auto'
        )
tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForCausalLM.from_pretrained(model,quantization_config=quantization_config)
pipe = pipeline(
      "text-generation",
       model=model,
       tokenizer=tokenizer,
       max_new_tokens = 600,
       do_sample=True,
       top_k=3,
       num_return_sequences=1,
       eos_token_id=tokenizer.eos_token_id
       )
llm = HuggingFacePipeline(pipeline=pipe)
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you"
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
                )

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt),
     ("human", "{input}"),])
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
#example query == "give me all the details of the caster herbal hair oil"
def run_rag_model(query):
    response = rag_chain.invoke({"input": query})
    assistant = response["answer"].split("Assistant: ")[1].split("(Concise answer)")[0].strip()
    return assistant

@app.route('/')
def index():
    return "RAG Model API is running!"

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query')
    
    if not user_query:
        return jsonify({"error": "Query not provided"}), 400
    
    # Call your RAG model
    result = run_rag_model(user_query)
    
    return jsonify({"reply": result})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    # Start ngrok tunnel
    !ngrok config add-authtoken 2lO2Ro2WuwTtGrfzCwhdeJg6ObP_7KTjvvygv223Ffa1So3Vo
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")
    
    app.run(port=5000)
