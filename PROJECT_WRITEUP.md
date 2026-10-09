# Order Assistant — Project Write-up

## 1. Architecture

I built the frontend using HTML, CSS, and JavaScript and the backend using Python and FastAPI. When a user asks a question, the frontend sends it to the backend. The backend processes the question using the order dataset and Groq AI, then sends the answer back to the website.

## 2. Tool Choices

I used FastAPI to build the backend API, CSV to store order details, and Groq API to connect the AI model. HTML, CSS, and JavaScript were used to build the website. I used GitHub to manage my code and Render to deploy the project.

## 3. Guardrails

I added input validation to ensure that questions are not empty and are within the allowed length. The backend handles errors without showing internal technical details to users. I also keep my API key in an environment variable instead of uploading it to GitHub.

## 4. Deployment

I pushed my project to GitHub and deployed it using Render. I tested the live website by asking for the status of order ORD-1001, and the assistant returned the correct status.

## 5. Future Improvements

I would like to add secure login, better order search, automated testing, and stronger checks to make AI responses more reliable.
