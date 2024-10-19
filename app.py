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
            'id': len(blog_posts) + 1,  # Assign a new unique ID
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


@app.route('/contact')
def contact():
    return 'Contact Page'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
