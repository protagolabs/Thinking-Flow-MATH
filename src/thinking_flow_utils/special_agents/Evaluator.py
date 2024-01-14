""" 
@file_name: Evaluator.py
@author: Netmind.AI BlackSheep team 
@date: 2024-1-10 
To define the Evaluator agent which can cheack if an answer is right.
"""


import sys
from io import StringIO
import io
import contextlib
import traceback

from src.thinking_flow_utils.prompts import evaluator_algebra, evaluator_contra, evaluator_flow
from src.thinking_flow_utils.BSAgent import BSAgent

class Evaluator:
    
    def __init__(self, llm="gpt-4-1106-preview") -> None:
        """init the Evaluator class

        Args:
            llm (str, optional): the large language model which we want to use. Defaults to "gpt-4-1106-preview".
            you can choose: 'gpt-4', 'gpt-3.5'
        """
        
        self.evaluator_contradiction = BSAgent(template=evaluator_contra, llm=llm)
        self.evaluator_algebra = BSAgent(template=evaluator_algebra, llm=llm)
        self.evaluator_flow = BSAgent(template=evaluator_flow, llm=llm)
        
    def __call__(self, question, answer="", method="contradiction")->tuple:
        """Call the Evaluator class, and get the result if this answer is right or wrong.

        Args:
            question (str): The question which we want to verify.
            answer (str): The answer of this question.
            method (str): The method we want to use to evaluate this answer.

        Returns:
            result (str): From the generation model, we can get the result of this question.
            if_right (bool): If the answer is right, return True, else return False.
            if_different (bool): If the answers from LLM and coding is different, return True, else return False.
        """
        
        # If you want to use the contradiction method, please use the parameters: question, answer
        if method == "contradiction":
            result, if_right = self._evaluate(question, answer, self.evaluator_contradiction)
            return result, if_right
        elif method == "algebra":
            result, if_right = self._evaluate(question, answer, self.evaluator_algebra)
            return result, if_right
        elif method == "flow":  
            result, if_right = self._evaluate(question, answer, self.evaluator_flow)
            return result, if_right
        else:
            raise ValueError(f"The method {method} is not in the Evaluator class.")

    def _evaluate(self, question, answer, agent)->tuple:
        """Use the contradiction method to evaluate the answer.    
        """
         
        result = agent.run(question=question, answer=answer)
        if_right = "|||RIGHT|||" in result
        
        if "```python" in result:
            code = self.extract_code(result, start_str="```python", end_str="```")
            code_result = self._run_code(code)
            if_right_2 = not "False" in code_result
            if_right = if_right and if_right_2
            
            result += "\n" + code_result
        
        return result, if_right 
    
    @staticmethod
    def extract_code(text, start_str="```python", end_str="```"):
        import re
        pattern = re.escape(start_str) + r"(.*?)" + re.escape(end_str)
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return None
    

    def _run_code(self, sample)->str:
        """Run the code part in the text.

        Args:
            sample (str): the code part in the text.

        Returns:
            str: the 'print' parts in the code or the error message.
        """
                 
        sample = sample.strip()    
        
        # Create a new output stream
        output = io.StringIO()
        error_message = None

        # try to run the code
        try:
            with contextlib.redirect_stdout(output):
                exec(sample, globals())
            print_output = output.getvalue()
            return print_output
        except Exception as e:
            error_message = traceback.format_exc()
            return error_message
        
    @contextlib.contextmanager
    def stdoutIO(self, stdout=None)->str:
        old = sys.stdout
        if stdout is None:
            stdout = StringIO()
        sys.stdout = stdout
        yield stdout
        sys.stdout = old
        
    def _extract_content(self, text):
        import re
        pattern = r"\|\|\|(.+?)\|\|\|"
        matches = re.findall(pattern, text, re.DOTALL)
        return matches
    
    