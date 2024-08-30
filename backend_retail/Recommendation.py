!pip install transformers sentence_transformers pandas numpy hnswlib torch
from transformers import AutoTokenizer, AutoModelForCausalLM
# This library provides pre-trained models and tokenizers for various NLP tasks, including text generation, translation, and question answering.
# AutoTokenizer: Used to convert text into numerical representations that models can understand.
# AutoModelForCausalLM: A class of models designed for causal language modeling, often used for text generation.
# Causal language modeling is the task of predicting the token following a sequence of tokens.
from sentence_transformers import SentenceTransformer
# SentenceTransformer: Loads a pre-trained sentence embedding model.

import pandas as pd
import numpy as np

import hnswlib
# hnswlib: A library for approximate nearest neighbor search, often used for efficient similarity search in high-dimensional spaces.
import torch

df_purchases=pd.read_csv("/content/data[1].csv",encoding='unicode_escape')
# Your string has a non ascii character encoded in it.Not being able to decode with utf-8 may happen if you've needed to use other encodings in your code.
# elimination of NaN values
df_purchases.dropna(inplace=True)
# elimination of duplicate rows
df_purchases.drop_duplicates(inplace=True)
# elimination of cancelled orders
df_purchases = df_purchases[~df_purchases['InvoiceNo'].str.startswith('C')]
# User purchase history
customer_history_dict = df_purchases.groupby("CustomerID")['StockCode'].apply(lambda x: sorted(list(set(x)))).to_dict()

# product to description dictionary
df_product_descriptions = df_purchases[["StockCode", "Description"]]
# Multiple transaction of same products are removed.
df_product_descriptions.drop_duplicates(inplace=True)
# dictionary generation
product_to_description_dict = dict(zip(df_product_descriptions['StockCode'], df_product_descriptions['Description']))

def get_previous_purchases(user_id, k=3):
  """Gets previous purchases of the user"""
  product_list = customer_history_dict.get(user_id, [])
  purchase_descriptions = ""
  for i, product in enumerate(product_list[:k]):
    product_description = product_to_description_dict.get(product, "")
    purchase_descriptions += f"{i+1}. {product_description}\n"

  return purchase_descriptions
# Sequence Transformer
embedding_model = SentenceTransformer("thenlper/gte-small")

def get_embedding(text: str) -> list[float]:
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []

    embedding = embedding_model.encode(text)

    return embedding.tolist()

df_product_descriptions["embedding"] = df_product_descriptions["Description"].apply(get_embedding)
# Embedding model dimension
dim = embedding_model.get_sentence_embedding_dimension()

num_elements = df_product_descriptions.shape[0]
# hnswlib initialization with cosine similarity
p = hnswlib.Index(space='cosine', dim=dim)

p.init_index(max_elements=num_elements, ef_construction=100, M=16)

p.set_ef(10)

embeddings = np.vstack(df_product_descriptions["embedding"].values)
p.add_items(embeddings)
def vector_search(user_query, k):
    """Gets user input query and return top k similar items"""

    # Generate embedding for the user query
    query_embedding = get_embedding(user_query)

    if query_embedding is None:
        return "Invalid query or embedding generation failed."


    labels, distances = p.knn_query(query_embedding, k=k)
    results = df_product_descriptions.iloc[list(labels[0])].to_dict('records')
    return results
def get_search_result(query, k):
    """Aggregate similar product descriptions into one string"""
    get_knowledge = vector_search(query, k)

    search_result = ""
    for i, result in enumerate(get_knowledge):
        search_result += f"{i+1}. {result.get('Description', 'N/A')}\n"

    return search_result
# Gets top k similar products w.r.t provided query
k = 3
query = "lantern"
source_information = get_search_result(query, k)
combined_information = f"Similar Results:\n{source_information}"

print(combined_information)
from huggingface_hub import notebook_login
notebook_login()

!pip install accelerate
# Load model directly


tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")

device = torch.device("cpu")

model = AutoModelForCausalLM.from_pretrained("google/gemma-2b-it")
# use gpu if available
user_id = 15781

query = "BAG CHARM"
k = 3
# get similar items
source_information = get_search_result(query, k)
previous_purchases = get_previous_purchases(user_id)

# Providing example prompts (few-shot learning) to get the desired output
example_prompt = f"""Given a customer's 'Previous Purchases', rerank a list of 'Recommended Products' from most to least relevant to the customer's preferences. Only recommend products from latest'Recommended Products' section The relevance should be determined by considering the types and themes of products the customer has bought before.

Example 1:
- User Input:
Previous Purchases:
1. BLUE CALCULATOR RULER
2. DOORMAT TOPIARY
3. PARTY BUNTING
Recommended Products:
1. CRYSTAL FROG PHONE CHARM
2. PINK CRYSTAL SKULL PHONE CHARM
3. BLUE LEAVES AND BEADS PHONE CHARM

- Model Output:
Reranked Recommendations:
1. BLUE LEAVES AND BEADS PHONE CHARM
2. CRYSTAL FROG PHONE CHARM
3. PINK CRYSTAL SKULL PHONE CHARM

Example 2:
- User Input:
Previous Purchases:
1. PANTRY HOOK SPATULA
2. BIRDCAGE DECORATION TEALIGHT HOLDER
3. REGENCY TEA PLATE PINK
Recommended Products:
1. SWEETHEART CAKESTAND 3 TIER
2. CAKESTAND, 3 TIER, LOVEHEART
3. REGENCY CAKESTAND 3 TIER

- Model Output:
Reranked Recommendations:
1. REGENCY CAKESTAND 3 TIER
2. SWEETHEART CAKESTAND 3 TIER
3. CAKESTAND, 3 TIER, LOVEHEART

"""
combined_information = f"""{example_prompt}

Your Turn:
<start_of_turn>user
Previous Purchases:
{previous_purchases}
Recommended Products:
{source_information}
<end_of_turn>
<start_of_turn>model
"""

input_ids = tokenizer(combined_information, return_tensors="pt").to(device)
response = model.generate(**input_ids, max_new_tokens=500)
print(tokenizer.decode(response[0]))
# User id to check result of personalized recommendation
user_id = 12583

query = "BAG CHARM"
k = 3
# get similar items
source_information = get_search_result(query, k)
previous_purchases = get_previous_purchases(user_id)

# Providing example prompts (few-shot learning) to get the desired output
example_prompt = f"""Given a customer's 'Previous Purchases', rerank a list of 'Recommended Products' from most to least relevant to the customer's preferences. Only recommend products from latest 'Recommended Products' section The relevance should be determined by considering the types and themes of products the customer has bought before. Also give brief explanation about reranking reason.

Example 1:
- User Input:
Previous Purchases:
1. BLUE CALCULATOR RULER
2. DOORMAT TOPIARY
3. PARTY BUNTING
Recommended Products:
1. CRYSTAL FROG PHONE CHARM
2. PINK CRYSTAL SKULL PHONE CHARM
3. BLUE LEAVES AND BEADS PHONE CHARM

- Model Output:
Reranked Recommendations:
1. BLUE LEAVES AND BEADS PHONE CHARM - Matches blue theme; visually appealing.
2. CRYSTAL FROG PHONE CHARM - Playful, aligns with fun items.
3. PINK CRYSTAL SKULL PHONE CHARM - Decorative, less color relevance noted.

Example 2:
- User Input:
Previous Purchases:
1. PANTRY HOOK SPATULA
2. BIRDCAGE DECORATION TEALIGHT HOLDER
3. REGENCY TEA PLATE PINK
Recommended Products:
1. SWEETHEART CAKESTAND 3 TIER
2. CAKESTAND, 3 TIER, LOVEHEART
3. REGENCY CAKESTAND 3 TIER

- Model Output:
Reranked Recommendations:
1. REGENCY CAKESTAND 3 TIER - Matches Regency style; highly relevant.
2. SWEETHEART CAKESTAND 3 TIER - Elegant, complements table setting decor.
3. CAKESTAND, 3 TIER, LOVEHEART - Decorative, thematic but less specific.
"""

combined_information = f"""{example_prompt}

Your Turn:
- User Input:
Previous Purchases:
{previous_purchases}
Recommended Products:
{source_information}
- Model Output:
"""

# will be used to extract last prompt
key_text = 'Your Turn:'

# input ids
input_ids = tokenizer(combined_information, return_tensors="pt").to(device)
response = model.generate(**input_ids, max_new_tokens=500)
output_text = tokenizer.decode(response[0])
output_text = output_text[output_text.index(key_text) + len(key_text):]

print(f"Query: {query}")
print(output_text)