""" 
@file_name: solve_competition.py
@date: 2024-1-14
@author: Netmind.AI BlackSheep team 
This script is used to solve the AAAI-K-12-Math-Competition question.
"""

import os 
import openai 
import argparse
from tqdm.auto import tqdm
openai.api_key = ""
os.environ["OPENAI_API_KEY"] = ""

from src.SolvingMachine import SolvingMachine 
from src.file_io_utils import read_json, save_json

def get_args():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", type=str, default="./data/TAL-SAQ6K-EN.jsonl", help="The file name of the question data.")
    parser.add_argument("--save_name", type=str, default="./result/TAL_SAQ6K_EN_prediction.json", help="The file name of the question data.")
    parser.add_argument("--max_evaluate_times", type=int, default=15, help="The max times that we can evaluate the answer.")
    parser.add_argument("--if_retrieval", type=bool, default=True, help="If we want to use the retrieval method.")
    parser.add_argument("--llm", type=str, default="gpt-4-1106-preview", help="Which LLM we want to use.")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    
    args = get_args()
    
    solver = SolvingMachine( max_evaluate_times=args.max_evaluate_times , if_retrieval=args.if_retrieval, llm=args.llm)
    file_name = args.file_name
    save_path = args.save_name
    
    problem_data = read_json(file_name) 
    result = {}
    
    for problem in tqdm(problem_data):
        question = problem["problem"]
        
        ans = solver(question)
        
        id_ = problem['queId']
        result[id_] = ans
        
        save_json(result, save_path)
    
    