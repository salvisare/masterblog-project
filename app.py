import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define the file path to your JSON file
BLOG_POSTS_FILE = 'blog_posts.json'


# Load blog posts from JSON file
def load_posts():
    """Load posts from the JSON file."""
    try:
        with open(BLOG_POSTS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    """Save posts to the JSON file."""
    with open(BLOG_POSTS_FILE, 'w') as file:
        json.dump(posts, file, indent=4)


# Function to fetch a post by its ID
def fetch_post_by_id(post_id):
    posts = load_posts()
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


# Function to get the next available ID
def get_next_id(posts):
    """Get the next available ID for a new post."""
    return max(post['id'] for post in posts) + 1 if posts else 1


@app.route('/')
def home():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Get data from form submission
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        # Load the current blog posts from the JSON file
        blog_posts = load_posts()

        # Create a new post with the next available ID
        new_post = {
            'id': get_next_id(blog_posts),  # Get a unique ID
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post to the blog_posts list
        blog_posts.append(new_post)

        # Save the updated list back to the JSON file
        save_posts(blog_posts)

        # Redirect to the home page to see the new post
        return redirect(url_for('home'))

    # If the request is GET, render the add.html form
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing posts
    blog_posts = load_posts()

    # Find the blog post with the given id and remove it from the list
    updated_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated posts
    save_posts(updated_posts)

    # Redirect back to the home page
    return redirect(url_for('home'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog post by its ID
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post with the form data
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        # Load existing posts, update, and save them back to the JSON file
        posts = load_posts()
        for i, p in enumerate(posts):
            if p['id'] == post_id:
                posts[i] = post  # Update the post
                break
        save_posts(posts)

        # Redirect back to the home page after updating
        return redirect(url_for('home'))

    # If it's a GET request, render the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
