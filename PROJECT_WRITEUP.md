# Order Assistant — Project Write-up

## 1. Architecture

I built the frontend using HTML, CSS, and JavaScript and the backend using Python and FastAPI. When a user asks a question, the frontend sends it to the backend. The backend processes the question using the order dataset and Groq AI, then sends the answer back to the website.

## 2. Tool Choices

I used FastAPI to build the backend API, CSV to store order details, and Groq API to connect the AI model. HTML, CSS, and JavaScript were used to build the website. I used GitHub to manage my code and Render to deploy the project.

## 3. Guardrails

I added input validation to ensure that questions are not empty and are within the allowed length. The backend handles errors without showing internal technical details to users. I also keep my API key in an environment variable instead of uploading it to GitHub.

## 4. Deployment

I pushed my project to GitHub and deployed it using Render. I tested the live website by asking for the status of order ORD-1001, and the assistant returned the correct status.

## Agent Tool Selection

The AI agent uses Groq's language model with function calling. It provides two tools: `find_order` to retrieve a specific order and `analyze_orders` to calculate order statistics. The model uses `tool_choice="auto"` to select the appropriate tool based on the user's question. Tool results are returned to the model so it can explain the answer in simple English.

## AI Tools Used

- **Groq API:** Runs the language model used by the deployed order assistant.
- **ChatGPT:** Assisted with development guidance, debugging, documentation, and testing.
- **Pytest:** Runs automated tests for order lookup and order statistics.

## 5. Future Improvements

I would like to add secure login, better order search, automated testing, and stronger checks to make AI responses more reliable.
