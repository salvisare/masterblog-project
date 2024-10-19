from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'About Page'


@app.route('/contact')
def contact():
    return 'Contact Page'



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
