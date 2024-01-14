"""
@file_name: BSAgent.py
@author: Netmind.AI BlackSheep team 
@date: 2024-1-10 
To define the BlackSheep-Agent(The BasicCLass of Agent)
"""

import time
from openai import OpenAI
import traceback

class BSAgent():

    def __init__(self, template={}, llm="gpt-4-1106-preview", temperature=0):

        self.llm = llm
        self.template = template
        self.temperature = temperature
        self.client = OpenAI()
        self._set_template()

    def _set_template(self):

        system = self.template["system"]
        user = self.template["user"]

        self.prompts = system + "||--||" + user

    def run(self, **kwargs):

        prefix = self.prompts.format(**kwargs)

        [system, user] = prefix.split("||--||")

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

        get_response_signal = False
        count = 0
        while not get_response_signal and count < 10:
            try:
                response = self.client.chat.completions.create(
                    model=self.llm,
                    messages=messages,
                    temperature=self.temperature,
                )
                get_response_signal = True
            except Exception as e:
                count += 1
                error_message = str(traceback.format_exc())
                print(f"The error: {error_message}")
                time.sleep(2)
        answer = response.choices[0].message.content
        
        return answer


