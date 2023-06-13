from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"},
    {"id": 3, "title": "Book 3", "author": "Author 3"}
]

# GET REQUEST - TEST TO CHECK IF WORKING
@app.route('/api/test', methods=['GET'])
def get_books():
    return jsonify(books)


# EXECUTE SERVER
if __name__ == '__main__':
    app.run(port=3001)