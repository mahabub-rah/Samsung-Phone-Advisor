from agent_1 import data_extractor

def review_generator(question):
    df = data_extractor(question)
    
    return df
if __name__ == "__main__":
    review_generator(("Compare S24 FE and S25 FE and s25 ultra"))