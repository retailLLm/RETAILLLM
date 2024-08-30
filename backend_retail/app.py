from pipes import quote
from dotenv import load_dotenv
load_dotenv()
import streamlit as st # type: ignore
import os
import pymysql
from langchain.llms import Ollama
import pandas as pd

# Configure Ollama
ollama = Ollama(base_url="http://localhost:11434", model="phi3")

def get_llama2_response(question, prompt):
    # Combine prompt and question into a single input for the Llama2 model
    combined_input = prompt + "\n\n" + question
    response = ollama.invoke(combined_input)
    return response.strip()

def read_sql_query(sql, db):
    config = {
        'user': 'root',
        'password': quote('Rishika@a041'),
        'host': 'localhost',
        'database': 'retail',
        'cursorclass': pymysql.cursors.DictCursor
    }
    cnx = pymysql.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cnx.commit()
    cnx.close()
    return rows


prompt = """You are an expert in converting English questions to SQL queries.
Please return only the SQL query without any additional text or explanations.

The SQL database is named RETAIL and has the following columns:
- Transaction ID
- Date
- Customer ID
- Gender
- Age
- Product Category
- Quantity
- Price per Unit
- Total Amount

For example:
Example 1 - What is the number of transactions per year and month?
SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, COUNT(*) AS num_transaction FROM retail.retail_sales_dataset GROUP BY YEAR(Date), MONTH(Date) ORDER BY Year, Month;

Example 2 - What is the number of transactions across different age groups of customers?
SELECT Age, COUNT(*) AS num_transactions FROM retail.retail_sales_dataset GROUP BY Age;

Example 3 - What is the total sales amount per product category?
SELECT `Product Category`, SUM(`Total Amount`) AS Total_Sales FROM retail.retail_sales_dataset GROUP BY `Product Category` ORDER BY Total_Sales DESC;

Example 4 - What is the average quantity purchased per product category?
SELECT `Product Category`, AVG(Quantity) AS Average_Quantity FROM retail.retail_sales_dataset GROUP BY `Product Category` ORDER BY Average_Quantity DESC; 

Example 5 - How many transactions were made by each gender?
SELECT Gender, COUNT(*) AS num_transactions FROM retail.retail_sales_dataset GROUP BY Gender;

Example 6 - What is the total number of transactions per month in 2023?
SELECT MONTH(Date) AS Month, COUNT(*) AS num_transactions FROM retail.retail_sales_dataset WHERE YEAR(Date) = 2023 GROUP BY MONTH(Date) ORDER BY Month;

Example 7 - What is the total revenue generated per customer?
SELECT `Customer ID`, SUM(`Total Amount`) AS Total_Revenue FROM retail.retail_sales_dataset GROUP BY `Customer ID` ORDER BY Total_Revenue DESC; 

Example 8 - Which age group has the highest total spending?
SELECT Age, SUM(`Total Amount`) AS Total_Spending FROM retail.retail_sales_dataset GROUP BY Age ORDER BY Total_Spending DESC;

Example 9 - What is the highest and lowest total amount spent in a single transaction?
SELECT MAX(`Total Amount`) AS Max_Spend, MIN(`Total Amount`) AS Min_Spend FROM retail.retail_sales_dataset;

Example 10 - What is the average age of customers who made purchases in each product category?
SELECT `Product Category`, AVG(Age) AS Average_Age FROM retail.retail_sales_dataset GROUP BY `Product Category` ORDER BY Average_Age DESC;

Example 11 - What are the top 5 most expensive items purchased?
SELECT `Product Category`, MAX(`Price per Unit`) AS Max_Price FROM retail.retail_sales_dataset GROUP BY `Product Category` ORDER BY Max_Price DESC LIMIT 5;

Example 12 - How many transactions were made in each month for each year?
SELECT YEAR(Date) AS Year, MONTH(Date) AS Month, COUNT(*) AS num_transactions FROM retail.retail_sales_dataset GROUP BY YEAR(Date), MONTH(Date) ORDER BY Year, Month;

Return only the SQL query."""



def clean_sql_query(response):
    # Remove any Markdown code block indicators and unnecessary text
    response = response.replace("```", "").strip()
    
    # Assume the first "SELECT" starts the query and everything before is not needed
    start_index = response.upper().find("SELECT")
    if start_index != -1:
        return response[start_index:].strip()
    
    return response.strip()

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Product Sales Analysis")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_llama2_response(question, prompt)
    print("Generated SQL Query:", response)
    
    # Clean the SQL query to remove any extraneous text
    cleaned_query = clean_sql_query(response)
    print("Cleaned SQL Query:", cleaned_query)
    
    try:
        sql_result = read_sql_query(cleaned_query, "retail")
        df = pd.DataFrame(sql_result)
        st.subheader("The Response is")
        # for row in sql_result:
        #     print(row)
        #     st.write(row)
        st.write(df)
        
        # Convert the result to a pandas DataFrame
       
       
        
    except pymysql.MySQLError as e:
        st.error(f"Error executing query: {e}")
        print(f"Error executing query: {e}")