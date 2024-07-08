from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

classifier = pipeline("sentiment-analysis")

res = classifier("i don't know what to say about this.")

print(res)

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)


classifier = pipeline("sentiment-analysis", tokenizer=tokenizer, model=model)
res = classifier("i don't know what to say about this.")

print(res)

sequence = "Using a Transformer network is simple"
res = tokenizer(sequence)
print(f"res > {res}")
tokens = tokenizer.tokenize(sequence)
print(f"tokens > {tokens}")
ids = tokenizer.convert_tokens_to_ids(tokens)
print(f"ids > {ids}")
decoded_string = tokenizer.decode(ids)
print(f"decoded_string > {decoded_string}")