from transformers import pipeline

# initialize a HuggingFace summarization model
# facebook/bart-large-cnn is the top HuggingFace summarization model
# max input length of 1024 tokens
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# summarize text using the summarization model
def summarize_text(text, min_length=25, max_length=100):
    summary = summarizer(text, min_length=min_length, max_length=max_length)
    return summary[0]['summary_text']