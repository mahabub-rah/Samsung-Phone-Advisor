from agent_1 import data_extractor
import pandas as pd


def review_generator(question):
    df = data_extractor(question)
    
    m1 = df.iloc[0]
    m2 = df.iloc[1]
    improvements = []
    
    for col in df.columns:
        if col == "model_name":
            continue
            
        val1 = m1[col]
        val2 = m2[col]

        # Numeric comparison
        try:
            num1 = float(str(val1).replace("GB","").replace("MP","").replace("mAh",""))
            num2 = float(str(val2).replace("GB","").replace("MP","").replace("mAh",""))
            
            if num2 > num1:
                if col == "battery":
                    improvements.append("better battery life")
                elif col == "rear_camera":
                    improvements.append("better camera performance")
                elif col == "ram":
                    improvements.append("more RAM")
                elif col == "storage":
                    improvements.append("more storage")
                    
        except:
            if val1 != val2:
                improvements.append(f"different {col.replace('_', ' ')}")
    print(improvements)
    # Create natural sentence
    if improvements:
        sentence = f"Compared to {m1['model_name']}, {m2['model_name']} has " + " and ".join(improvements) + "."
    else:
        sentence = f"Compared to {m1['model_name']}, {m2['model_name']} has similar specifications."
    
    return {
        "question": question, "answer": sentence
    }
  

