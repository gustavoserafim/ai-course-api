import nltk

def input_stats(function_name: str, content: str):
    print(f"{function_name} >> INPUT LENGHT : {len(content)}")
    print(f"{function_name} >> INPUT TOKEN LENGHT:{len(nltk.word_tokenize(content))}")
    print(f"{function_name} >> INPUT:{content}")

def output_stats(function_name: str, content: str):
    print(f"{function_name} >> OUTPUT LENGHT : {len(content)}")
    print(f"{function_name} >> OUTPUT TOKEN LENGHT:{len(nltk.word_tokenize(content))}")
    print(f"{function_name} >> OUTPUT:{content}")
  
def breakline():
    print("\n\n========================================\n\n")