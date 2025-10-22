from db_model import engine
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import re
import os


load_dotenv()
api = OpenAI(api_key=os.getenv("open_api"))

def data_extractor(question):

    q = question.lower()
    cleaned_q = re.sub(r'\b(?:compare|compared|vs|versus|comparison|difference|between)\b', '', q)
    cleaned_q = re.sub(r'\s+', ' ', cleaned_q).strip()

    df = pd.read_sql_table("smartphone_specs", engine)

    phones = []
    model_match = re.findall(
    r'(?:samsung\s*(?:galaxy)?\s*)?('
    r'[a-z]\s*(?:fold|flip)\s*\d+|'  # z fold 7, z flip 6
    r'(?:fold|flip)\s*\d+|'          # fold 7, flip 6  
    r'[a-z]\d{2,}\s*(?:plus|ultra|edge|fe|pro)?'  # a15, s24 ultra, m14 pro
    r')\s*(?:4g|5g)?',  # network 
    cleaned_q)
    target_models = [match.strip() for match in model_match] if model_match else []
    
    for name in df["model_name"]:
        name_lower = name.lower()
    
        # model number match
        for target_model in target_models:
            if target_model and re.search(rf'\b{re.escape(target_model)}\b', name_lower):
                phone_data = df[df["model_name"] == name].iloc[0]
                phones.append(phone_data)
    
        # question is substring of model name
        if q in name_lower:
            phone_data = df[df["model_name"] == name].iloc[0]
            phones.append(phone_data)
    
        # word-based matching 
        name_w = re.findall(r"[a-z0-9]+", name_lower)
        ques_w = re.findall(r"[a-z0-9]+", q)
    
        # Filter out common non-model words to avoid false matches
        common_words = {'samsung', 'galaxy', 'price', 'cost', 'spec', 'specs', 'feature', 'features'}
        filtered_name_w = [w for w in name_w if w not in common_words and len(w) > 2]
        filtered_ques_w = [w for w in ques_w if w not in common_words and len(w) > 2]
    
        keyword = 0
        for w in filtered_name_w:
            if any(re.search(rf"\b{re.escape(w)}\b", q_word) for q_word in filtered_ques_w):
                keyword += 1

        #at least 2 keyword matches
        if keyword >= 2:
            phone_data = df[df["model_name"] == name].iloc[0]
            phones.append(phone_data)


    if len(phones) ==0 :
        return {"question": question, "answer": "Sorry, I couldn’t find that phone in the database."}
    phones = pd.DataFrame(phones).drop_duplicates()
    return phones



