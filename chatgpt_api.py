from openai import OpenAI
from config import OPENAI_KEY
import time
import os
import json
client = OpenAI(api_key=OPENAI_KEY)

class ChatGPT(object):
    def __init__(self, MODEL):
        self.MODEL = MODEL
        self.temp = 0
        self.top_p = 0
        self.frequency_penalty = 0
        self.presence_penalty = 0
        self.retry = 3

    def get_chatgpt_response(self, prompt, max_answer_tokens, default_answer = "OPENAI_ERROR"):
        no_attempts = self.retry
        qu_attempts = 1
        answer = default_answer
        while qu_attempts<=no_attempts:
            try:
                response = client.chat.completions.create(model=self.MODEL,
                                                messages=[{"role": "user", "content": prompt}],
                                                temperature=self.temp,
                                                max_tokens=max_answer_tokens,
                                                top_p= self.top_p,
                                                frequency_penalty= self.frequency_penalty,
                                                presence_penalty= self.presence_penalty)
                answer = response.choices[0].message.content    
                qu_attempts = no_attempts + 1 # update to 6 to exit the while loop
            except Exception as e:
                print(f"Openai error, attempt {qu_attempts}, {e}")
                qu_attempts += 1
                time.sleep(5*qu_attempts)

        return answer
    
    def get_gpt_json_response(self, prompt, json_schema, max_answer_tokens, default_answer = "OPENAI_ERROR"):
        no_attempts = self.retry
        qu_attempts = 1
        answer = default_answer
        while qu_attempts<=no_attempts:
            try:
                response = client.chat.completions.create(model=self.MODEL,
                                                messages=[{"role": "system", "content": "Provide output in valid JSON. The data schema should be like this:"+ json.dumps(json_schema)},
                                                          {"role": "user", "content": prompt}],
                                                temperature=self.temp,
                                                response_format = {"type":"json_object"},
                                                max_tokens=max_answer_tokens,
                                                top_p= self.top_p,
                                                frequency_penalty= self.frequency_penalty,
                                                presence_penalty= self.presence_penalty)
                answer = response.choices[0].message.content
                
                qu_attempts = no_attempts + 1 # update to 6 to exit the while loop
            except Exception as e:
                print(f"Openai error, attempt {qu_attempts}, {e}")
                qu_attempts += 1
                time.sleep(5*qu_attempts)
        return answer
    
    def export_config(self):
        export_dict = {
            "temperature": self.temp,
            "top_p": self.top_p,
            "frequency_penalty": self.frequency_penalty,
            "presence_penalty" : self.presence_penalty,
            "num_retry": self.retry

        }
        return export_dict

