import praw

reddit = praw.Reddit(
    client_id="CmE8lqF33R2qj8pN9Awtiw",
    client_secret="SEJr8Komd1l8putrNDRisH464WWs4Q",
    user_agent="python:u-coursemapscraper:v1.0 (by /u/Beneficial-Goat9925)"
)

subreddit = reddit.subreddit("uAlberta")
def fetch_posts(department, limit=20) -> list:
    """
    Fetch the most recent posts from the uAlberta subreddit related to a specific department.
    Args:
        department (str): Department code (e.g., 'cmput' for Computer Science).
        limit (int): Number of posts to fetch. Default is 20.
    Returns:
        list: A list of dictionaries containing post information.
              - Includes: 'title', 'url', 'score', 'id', 'created_utc', 'num_comments', 'selftext'
    """
    posts = []
    for submission in subreddit.search(f'title:"{department}"', limit=limit):
        post_info = {
            'title': submission.title,
            'url': submission.url,
            'score': submission.score,
            'id': submission.id,
            'created_utc': submission.created_utc,
            'num_comments': submission.num_comments,
            'selftext': submission.selftext
        }
        posts.append(post_info)
    return posts

    
def main():
    dept = input("Enter the department code (e.g., cmput or int d): ").strip().lower()
    dept = dept.replace(" ", "_")
    posts = fetch_posts(dept)
    for post in posts:
        print(f"Title: {post['title']}")
        print(f"URL: {post['url']}")
        print(f"Score: {post['score']}")
        print(f"Comments: {post['num_comments']}")
        print(f"Posted on (UTC): {post['created_utc']}")
        print(f"Content: \n{post['selftext'][:100]}...")  # Print first 100 characters of the post
        print("-" * 40)
if __name__ == "__main__":
    main()