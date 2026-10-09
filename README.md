# Order Assistant

## About the Project

I developed this project to make it easier for users to get order details by asking questions in simple English. Instead of searching through order data manually, users can ask the assistant about an order and receive a response.

## What I Built

* A web interface where users can interact with the order assistant.
* A backend using Python and FastAPI.
* An order dataset stored in a CSV file.
* An AI assistant that answers order-related questions using the Groq API.
* An API endpoint to check whether the application is running.

## Technologies I Used

* Python
* FastAPI
* HTML, CSS and JavaScript
* Groq API
* CSV
* GitHub and Render

## How It Works

The user enters a question on the website. The frontend sends the question to the FastAPI backend. The assistant processes the question using the order data and AI model, then returns an answer to the user.

## How to Run the Project

1. Install the required packages using `pip install -r requirements.txt`.
2. Add the Groq API key to a local `.env` file.
3. Run the application using `uvicorn main:app --reload`.
4. Open `http://127.0.0.1:8000` in a browser.

## What I Learned

While building this project, I learned how to connect a frontend with a Python backend, work with APIs, use an AI model, manage project files with GitHub, and deploy a web application using Render.

## Future Improvements

I would like to add proper user authentication, improve error handling, and add more features for searching and managing orders.
