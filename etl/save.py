import json

# saves raw reddit data
def save_raw(data, filename="outputs/raw_reddit_data.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# saves the reddit post titles and summaries of the comments
def save_summary(data, filename="outputs/summary_output.txt"):
    with open(filename, 'w') as f:
        for post in data:
            f.write(f"Title:\n{post['title']}\n")
            f.write(f"Body summary:\n{post['body_summary']}\n")
            f.write(f"Top comments summary:\n{post['comments_summary']}\n\n")

# prints the reddit post titles and summaries of the comments to the terminal
def print_summary(data):
    print("=" * 80)
    for post in data:
        print(f"Post Title:\n{post['title']}")
        print("-" * 80 + "\nBody summary:")
        print(post['body_summary'])
        print("-" * 80 + "\nTop comments summary:")
        print(post['comments_summary'])
        print("=" * 80)
