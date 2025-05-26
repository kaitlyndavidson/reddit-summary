from etl import ingest, clean, save
from models import summarizer, classifier

# summarize the post content
def summarize_body(body_text, min_output=25, max_output=100):
    if not body_text.strip():
        return "(No body text to summarize.)"
    return summarizer.summarize_text(body_text, min_length=min_output, max_length=max_output)

# combines and summarizes a list of top comments
def summarize_comments(comments_list, max_words=512, min_output=25, max_output=100):
    if not comments_list:
        return "(No comments to summarize.)"
    # first, summarize long comments individually
    # allow each comment up to an equal portion of the max words
    max_words_per_comment = max_words // len(comments_list)
    comments_list_summarized = []
    for comment in comments_list:
        # if the comment is shorter than allowed, don't modify it
        if len(comment.split()) <= max_words_per_comment:
            comments_list_summarized.append(comment)
        # if the comment is longer than allowed, summarize it
        else:
            comment_summary = summarizer.summarize_text(comment, min_length=max_words_per_comment//2, max_length=max_words_per_comment)
            comments_list_summarized.append(comment_summary)

    # combine comments into one string
    text = "\n".join(comments_list_summarized)
    # summarize all comments together
    summary = summarizer.summarize_text(text, min_length=min_output, max_length=max_output)
    return summary


if __name__ == "__main__":
    subreddit_name = 'LifeProTips'
    post_limit = 10
    comment_limit = 10

    # fetch and save raw reddit data
    posts_data = ingest.fetch_post_data(subreddit_name=subreddit_name, post_limit=post_limit, comment_limit=comment_limit)
    save.save_raw(posts_data)

    # classification
    # doesn't perform super well - need more and better labeled data
    all_comments = []
    all_labels = []
    # collect comments and labels across all posts
    for post in posts_data:
        comments = post['comments']
        if comments:
            all_comments.extend(comments)
            all_labels.extend(classifier.generate_labels(comments))
    if all_comments and all_labels:
        classifier = classifier.CommentClassifier()
        classifier.fit(all_comments, all_labels)
        classifier.evaluate()
    else:
        print("No comments or labels available for training the classifier.")

    # summarize data
    results = []
    for post in posts_data:
        body_summary = summarize_body(post['body'])
        comments_summary = summarize_comments(post['comments'])
        results.append({'title': post['title'], 'body_summary': body_summary, 'comments_summary': comments_summary})

    # save summarized data
    save.save_summary(results)
    save.print_summary(results)
