import json
from flask import Flask, render_template, request


app = Flask(__name__)

# Load blog posts from JSON file
def load_blog_posts():
    try:
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return []  # Return an empty list in case of error
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return []  # Return an empty list if file is missing

@app.route('/')
def home():
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/about')
def about():
    return 'About Page'


@app.route('/contact')
def contact():
    return 'Contact Page'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
