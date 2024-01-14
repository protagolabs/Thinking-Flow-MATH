""" 
@file_name: SolvingMachine.py
@author: Netmind.AI BlackSheep team 
@date: 2024-1-10 
Combain all the agents to solve a AAAI-K-12-Math-Competition question.
"""


from src.thinking_flow import CTF_thinking_flow, CTF_thinking_flow_correction
from src.thinking_flow_utils.special_agents.Evaluator import Evaluator 
from src.thinking_flow_utils.BSAgent import BSAgent
from src.thinking_flow_utils.prompts import CLEAN


class SolvingMachine:
    
    def __init__(self, max_evaluate_times=5, if_retrieval=True, llm="gpt-4-1106-preview"):
        """Init the SolvingMachine class
        
        Args:   
            max_evaluate_times (int): The max times that we can evaluate the answer. Defaults to 10.
            if_retrieval (bool): If we want to use the retrieval method. Defaults to True.
            llm (str): Which LLM we want to use. Defaults to "gpt-4-1106-preview".
        """
        
        self.max_evaluate_times = max_evaluate_times
        self.if_retrieval = if_retrieval
        self.llm = llm
        self.evaluator = Evaluator(self.llm)
        self.ctf = CTF_thinking_flow
        self.ctf_correct = CTF_thinking_flow_correction
        self.clean_float_agent = BSAgent(template=CLEAN, llm=self.llm)
        
        
    def __call__(self, question) -> str:
        """Call the SolvingMachine class, and get the answer of this question.

        Args:
            question (str): The question which we want to solve.

        Returns:
            str: The answer of this question.
        """
        
        solving_time = 0 
        solving_info_eachtime = {}
        
        # Step 1: Do the CTF
        solving_info = self.ctf(question, if_retrieval=self.if_retrieval, llm=self.llm)
        
        # Step 2: Evaluate the answer
        evaluate_results = {}
        wrong_time = 0
        for method in ["contradiction", "algebra", "flow"]:
            evaluate_info, if_right = self.evaluator(question, solving_info["final_answer"], method=method)
            evaluate_results[method] = {"result": evaluate_info, "if_right": if_right}
            if not if_right:
                wrong_time += 1
                
        ans_loacl = solving_info['final_answer']
        solving_info_eachtime[ans_loacl] = wrong_time
        
        # Step 3: If the answer is right, return the result
        if wrong_time == 0:
            float_answer = self.clean_float_agent.run(info=solving_info["final_answer"])
            return float_answer
        # Step 4: If the answer is wrong, do the correction and re-evaluate, until the answer is right( we also have a max_evaluate_times)
        else:
            while solving_time < self.max_evaluate_times: 
                
                evaluate_info = ""
                for evaluate_result in evaluate_results.values():
                    if not evaluate_result["if_right"]:
                        evaluate_info  += evaluate_result["result"]
                old_plan = solving_info["plan"]
                old_process = solving_info["solving_process"]
                
                solving_info = self.ctf_correct(question, old_plan, old_process, evaluate_info, if_retrieval=self.if_retrieval, llm=self.llm)
                
                for method in ["contradiction", "algebra", "flow"]:
                    evaluate_info, if_right = self.evaluator(question, solving_info["final_answer"], method=method)
                    evaluate_results[method] = {"result": evaluate_info, "if_right": if_right}
                    if not if_right:
                        wrong_time += 1
                if wrong_time == 0:
                    float_answer = self.clean_float_agent.run(info=solving_info["final_answer"])
                    return float_answer
                else:
                    solving_time += 1
                    ans_loacl = solving_info['final_answer']
                    solving_info_eachtime[ans_loacl] = wrong_time
                    continue
        
        # Step 5: If the answer is still wrong, return the answer which has the least wrong times.
        solving_info_eachtime = self.sort_dict_by_value(solving_info_eachtime)
        ans_loacl = list(solving_info_eachtime.keys())[-1]
        float_answer = self.clean_float_agent.run(info=ans_loacl)
        return float_answer
                
    @staticmethod
    def sort_dict_by_value(d) -> dict:
        """ 
        Sort the dict by the value.
        """
        return dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
                
