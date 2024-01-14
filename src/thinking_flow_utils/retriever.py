""" 
@file_name: retriever.py
@date: 2023-8-17
@author: Netmind.AI BlackSheep team
Call the API to get the similar math questions
"""


import requests
import json


def retriever(question, k=4):
    # We have already set the top-k = 4. 

    # question = "$$David\textquotesingle s$$ cookies were cost thrice as much as $$Jeremy\textquotesingle s$$ cookies. $$David$$ had only $$$0.50$$ cookies while $$Jeremy$$ had~$\tfrac{3}{5}$~as many $$$0.50$$ cookies as $$$0.10$$ cookies. There were $$60$$ fewer $$$0.10$$ cookies than $$$0.50$$ cookies. How much were $$Jeremy\textquotesingle s$$ cookies worth?"
    url = f"https://retrieverk12.ngrok.io/retrieval/{question}"
    response = requests.request("GET", url)
    
    diction = eval(response.text)
    result = diction["retrieval"]

    return result