import os
import google.generativeai as genai
from config import GEMINI_KEY
import typing_extensions as typing            
from dotenv import load_dotenv
import os

load_dotenv()
api_key = "AIzaSyBl8ZRptTPPTjCBK3zF7hYqwE9bVVSB9d8"

genai.configure(api_key=api_key)


#Note works with both flash and pro

def gemini_response(prompt, model_name, MAX_TOKENS_ANSWER=1000):
    model = genai.GenerativeModel(
    model_name,
    generation_config={
        "max_output_tokens": MAX_TOKENS_ANSWER,
        "temperature": 0.2,
        "response_mime_type": "application/json",
})
    response = model.generate_content(prompt)

    resp_json = response.candidates[0].content.parts[0].text
    return resp_json

class Recipe(typing.TypedDict):
  recipe_name: str

#Note works with only pro1.5

def gemini_json_response(prompt,json_out,model_name, MAX_TOKENS_ANSWER=1000):
    model = genai.GenerativeModel(
    model_name,
    generation_config={
        "max_output_tokens": MAX_TOKENS_ANSWER,
        "temperature": 0.2,
        "response_mime_type": "application/json",
        "response_schema": json_out,
})
    response = model.generate_content(prompt)

    resp_json = response.candidates[0].content.parts[0].text
    return resp_json
    
