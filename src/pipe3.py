from transformers import pipeline

classifier = pipeline("zero-shot-classification")

res = classifier(
    "this is a course about python list comprehension",
    candidate_labels=["education", "politics", "sports"]
)

print(res)