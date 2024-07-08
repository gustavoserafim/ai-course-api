import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
from huggingface_hub import login
from decouple import config

HUGGINGFACE_TOKEN = config("HUGGINGFACE_TOKEN")
login(HUGGINGFACE_TOKEN)

def ask(model: str, question: str) -> str:
    # load model and tokenizer
    model_name = "mistralai/Mistral-7B-Instruct-v0.3"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # move the model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # encode the input text
    input_text = "Explique a teoria da relatividade em termos simples."

    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    # Generate the output
    outputs = model.generate(inputs["input_ids"], max_length=150, num_return_sequences=1)

    # Decode and print the output
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(generated_text)
