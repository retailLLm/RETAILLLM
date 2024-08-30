from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.llms import GooglePalm
from langchain_experimental.sql import SQLDatabaseChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector, PromptTemplate, FewShotPromptTemplate
from urllib.parse import quote
from langchain.utilities import SQLDatabase
import logging
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt

app = Flask(_name_)
CORS(app, resources={r"/": {"origins": ""}})

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure GooglePalm
api_key = "GOOGLE_API_KEY"
llm = GooglePalm(google_api_key=api_key, temperature=0.2)

# Configure SQL Database (replace with your actual database connection details)
db_user = "root"
db_password = "password"
db_host = "localhost"
db_name = "atliq_tshirts"
encoded_password = quote(db_password)

# Construct the connection string
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{encoded_password}@{db_host}/{db_name}",
                          sample_rows_in_table_info=3)

# Configure embeddings
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

# Configure database chain with LLM and SQLDatabase
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Example few shots for the prompt template (adjust as per your use case)
few_shots = [
    {'Question': "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery': "SELECT stock_quantity FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS'",
     'SQLResult': "Result of the SQL query",
     'Answer': 14},
    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery': "select sum(price*stock_quantity) from t_shirts where size = 'S'",
     'SQLResult': "Result of the SQL query",
     'Answer': 26772},
    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied, how much revenue will our store generate (post discounts)?",
     'SQLQuery': """select sum((price*stock_quantity)*(1-ifnull((pct_discount/100),0))) from t_shirts t left join discounts d on t.t_shirt_id = d.t_shirt_id where brand = 'Levi'""",
     'SQLResult': "Result of the SQL query",
     'Answer': 29118},
    {'Question': "If we have to sell all the Levi’s T-shirts today, how much revenue will our store generate without discount?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi'",
     'SQLResult': "Result of the SQL query",
     'Answer': 29118},
    {'Question': "How many white color Levi's shirts do I have?",
     'SQLQuery': "select sum(stock_quantity) from t_shirts where color = 'white' and brand = 'Levi'",
     'SQLResult': "Result of the SQL query",
     'Answer': 256},
    {'Question': "How much sales amount will be generated if we sell all large size t-shirts today in Nike brand after discounts?",
     'SQLQuery': """select sum((price*stock_quantity)*(1-ifnull((pct_discount/100),0))) from t_shirts t left join discounts d on t.t_shirt_id = d.t_shirt_id where brand = 'Nike' and size = 'L'""",
     'SQLResult': "Result of the SQL query",
     'Answer': 29118}
]

to_vectorize = [" ".join(str(value) for value in example.values()) for example in few_shots]
vectorstore = Chroma.from_texts(to_vectorize,embedding = embeddings,metadatas = few_shots)
                                
example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",)
                                
few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )
new_chain = SQLDatabaseChain.from_llm(llm,db,verbose = True, prompt = few_shot_prompt)

@app.route('/')
def index():
    return "Flask server is running!"

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.json
        query = data.get('query')
        
        # Log the received query
        logging.debug(f"Received query: {query}")

        # Process query using the database chain
        result = new_chain(query)

        # Log the result
        logging.debug(f"Generated SQL query result: {result}")
        
        answer = result['result']
        # Return response as JSON
        return jsonify({'reply': str(answer)})
    
    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        return jsonify({'error': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True,use_reloader=False,port=8000)
