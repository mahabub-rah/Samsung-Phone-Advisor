from db_model import engine
import pandas as pd
import re

def rag_search(question):
    df = pd.read_sql_table("smartphone_specs", engine)
    q = question.lower()

    found_phone = None
    model_match = re.search(
    r'(?:samsung\s*(?:galaxy)?\s*)?('
    r'[a-z]\s*(?:fold|flip)\s*\d+|'  # z fold 7, z flip 6
    r'(?:fold|flip)\s*\d+|'          # fold 7, flip 6  
    r'[a-z]\d{2,}\s*(?:plus|ultra|edge|fe|pro)?'  # a15, s24 ultra, m14 pro
    r')\s*(?:4g|5g)?',  # network 
    q)
    target_model = model_match.group(1) if model_match else None
    
    for name in df["model_name"]:
        name_lower = name.lower()
    
        # model number match
        if target_model and re.search(rf'\b{re.escape(target_model)}\b', name_lower):
            found_phone = name
            break
    
        # question is substring of model name
        if q in name_lower:
            found_phone = name
            break
    
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
            found_phone = name


    if not found_phone:
        return {"question": question, "answer": "Sorry, I couldn’t find that phone in the database."}


    phone = df[df["model_name"] == found_phone].iloc[0]

    if any(word in q for word in ["price", "cost", "tk", "taka", "amount"]):
        return {"question": question, "answer": f"The price of {phone['model_name']} is {phone['price']}."}

    if any(word in q for word in ["battery", "mah", "power"]):
        return {"question": question, "answer": f"The battery capacity of {phone['model_name']} is {phone['battery']}."}

    if any(word in q for word in ["camera", "photo", "picture"]):
        return {"question": question, "answer": f"{phone['model_name']} has a {phone['rear_camera']} rear camera and a {phone['f_camera']} front camera."}

    if any(word in q for word in ["ram", "performance", "speed"]):
        return {"question": question, "answer": f"{phone['model_name']} comes with {phone['ram']} RAM."}

    if any(word in q for word in ["storage", "memory", "gb", "rom"]):
        return {"question": question, "answer": f"{phone['model_name']} offers {phone['storage']} of internal storage."}


    return {
        "question": question, "answer": f"{phone['model_name']} has {phone['battery']} battery and {phone['rear_camera']} rear camera, with {phone['ram']} ram."
    }

