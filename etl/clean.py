import re

def clean_comment(comment):
    # remove URLs
    comment = re.sub(r"http\S+", "", comment)
    # remove newlines/tabs
    comment = comment.replace('\n', ' ').replace('\r', ' ').strip()
    # remove multiple spaces
    comment = re.sub(' +', ' ', comment)
    return comment
