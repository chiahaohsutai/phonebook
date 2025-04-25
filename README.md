# Phonebook

A simple contacts application built with Flask, HTMX, and Alpine.js. This project is inspired by the contacts app from the book Hypermedia Systems.

I created this project to learn more about low-JS libraries and explore alternatives to traditional SPAs (Single Page Applications). One key difference from the book’s version is that this project uses MongoDB as a database, instead of the in-memory dummy database used in the book.

If your introduction to web development was primarily through SPAs, I highly recommend Hypermedia Systems. It offers a fresh perspective on building modern web apps by leveraging HTTP and hypermedia — allowing you to accomplish a lot with minimal JavaScript.

## Local Installation
1. Create and activate a Python virtual environment:
```bash
# Create a new Python virtual environment
python -m venv .venv

# Activate the virtual environment (macOS/Linux)
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3.	Set up MongoDB:
- You’ll need to run a local MongoDB server or use a MongoDB Atlas deployment.
- By default, the project connects to a local MongoDB instance. You can update the connection string in the code if needed.

4.	Run the Flask server:
```bash
flask run
```
5. Visit the app:
- Open your browser and go to http://127.0.0.1:5000
