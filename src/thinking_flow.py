""" 
@file_name: thinking_flow.py 
@author: Netmind.AI BlackSheep team 
@date: 2024-1-10 
To define the agents of the thinking flow.
"""


import re
import copy
import json
import numpy as np


from src.thinking_flow_utils.special_agents.MathCoding import MathCoding
from src.thinking_flow_utils.BSAgent import BSAgent
from src.thinking_flow_utils.retriever import retriever
from src.thinking_flow_utils.prompts import (
    plan_ctf, solving_ctf, fix_ctf, plan_correction, solving_correction, fix_correction
)      


# ================================== CTF: Solving a question by CTF

def CTF_thinking_flow(question:str, if_retrieval=True, llm="gpt-4-1106-preview") -> dict:
    """Solving a question by CTF

    Args:
        question (str): The question.
        if_retrieval (bool, optional): if you want to do the retrieval. Defaults to True.
        llm (str, optional): Which LLM you want to use. Defaults to "gpt-4-1106-preview".

    Returns:
        result_info: The result information.
    """

    # step 1: Create Agents
    plan_agent = BSAgent(template=plan_ctf, llm=llm)
    solving_agent = BSAgent(template=solving_ctf, llm=llm)
    calculus_agent = MathCoding(type=1)
    fix_agent = BSAgent(template=fix_ctf, llm=llm)

    # Step 2: Do the retrieval
    if if_retrieval:
        retrieval = retriever(question = question, k=4)
    else:
        retrieval = ""
        
    wrong = ""

    do_it = 0
    while do_it < 10:
        # Step 3: Generate a plan
        plan = plan_agent.run(hint=retrieval, wrong=wrong, question=question)
        hint = retrieval + "\nAnd we make a plan which you should follow:\n" + plan
            
        # Step 4: Solving this problem by following the plan
        process = solving_agent.run(hint=hint, question=question)

        # Step 5: Using coding method to re-do the solving process
        coding_answer = calculus_agent(question=question, answer=process)

        
        if coding_answer == "":
            wrong += f"\nThis plan is wrong, which can not solve this problem, please change another method:{plan}"
            do_it += 1
        else:
            do_it = 10

    # Step 6: Combain the llm-result and the coding-result
    final_answer = fix_agent.run(hint=hint, question=question, original=process, computed=coding_answer)

            
    return {"final_answer": final_answer, "solving_process":process, "coding_answer":coding_answer, "retrieval":retrieval, "plan":plan}

def CTF_thinking_flow_correction(question:str, old_plan:str, old_process:str, evaluate:str, if_retrieval=True, llm="gpt-4-1106-preview") -> dict:
    """Solving a question which be thought wrong by Evaluator

    Args:
        question (str): The question.
        old_plan (str_): The old plan for this question last time.
        old_process (str): The solving process for this question last time.
        evaluate (str): Wht the evaluator think about this question last time.
        if_retrieval (bool, optional): if you want to use the retrieval. Defaults to True.
        llm (str, optional): The model name from the openai. Defaults to "gpt-4-1106-preview".

    Returns:
        result_info: The result information.
    """
    
    
    # step 1: Create Agents
    plan_agent = BSAgent(template=plan_correction, llm=llm)
    solving_agent = BSAgent(template=solving_correction, llm=llm)
    calculus_agent = MathCoding(type=1)
    fix_agent = BSAgent(template=fix_correction, llm=llm)

    # Step 2: Do the retrieval
    if if_retrieval: 
        retrieval = retriever(question = question, k=4)
    else:
        retrieval = ""
        
    wrong = ""

    do_it = 0
    while do_it < 10:
        # Step 3: Generate a plan
        plan = plan_agent.run(hint=retrieval, old_plan=old_plan, old_process=old_process, evaluate=evaluate, question=question)
        hint = retrieval + "\nAnd we make a plan which you should follow:\n" + plan
            
        # Step 4: Solving this problem by following the plan
        process = solving_agent.run(hint=hint, old_plan=old_plan, old_process=old_process, evaluate=evaluate, question=question)

        # Step 5: Using coding method to re-do the solving process
        coding_answer = calculus_agent(question=question, answer=process)
        
        if coding_answer == "":
            wrong += f"\nThis plan is wrong, which can not solve this problem, please change another method:{plan}"
            do_it += 1
        else:
            do_it = 10

    # Step 6: Combain the llm-result and the coding-result
    final_answer = fix_agent.run(hint=hint,  old_plan=old_plan, old_process=old_process, evaluate=evaluate, 
                                              question=question, original=process, computed=coding_answer)
            
    return {"final_answer": final_answer, "solving_process":process, "coding_answer":coding_answer, "retrieval":retrieval, "plan":plan}

