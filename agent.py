
import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "orders.csv"

load_dotenv(BASE_DIR / ".env")


# TOOL 1: Find a specific order
def find_order(order_id: str):
    df = load_orders()

    matches = df[
        df["order_id"].astype(str).str.upper()
        == order_id.strip().upper()
    ]

    if matches.empty:
        return {
            "found": False,
            "message": f"No order found with ID {order_id}."
        }

    return {
        "found": True,
        "order": matches.iloc[0].to_dict()
    }


# Load and validate the dataset
def load_orders():
    if not CSV_FILE.exists():
        raise FileNotFoundError("orders.csv was not found.")

    df = pd.read_csv(CSV_FILE)

    required_columns = [
        "order_id", "order_date", "customer_name", "city",
        "product", "category", "quantity", "unit_price_inr",
        "total_inr", "payment_method", "status"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing dataset columns: {missing}")

    return df


# TOOL 2: Analyze orders and calculate statistics
def analyze_orders(category: str, status: str, month: str):
    df = load_orders()

    if category:
        df = df[
            df["category"].astype(str).str.casefold()
            == category.strip().casefold()
        ]

    if status:
        df = df[
            df["status"].astype(str).str.casefold()
            == status.strip().casefold()
        ]

    if month:
        try:
            month_number = int(month)
        except ValueError:
            return {"error": "Month must be a number from 1 to 12."}

        if not 1 <= month_number <= 12:
            return {"error": "Month must be between 1 and 12."}

        dates = pd.to_datetime(df["order_date"], errors="coerce")
        df = df[dates.dt.month == month_number]

    if df.empty:
        return {
            "order_count": 0,
            "cancelled_count": 0,
            "revenue_inr": 0,
            "quantity_sold": 0,
            "top_customer": None,
            "top_customer_spending_inr": 0,
            "message": "No orders matched the filters."
        }

    revenue = pd.to_numeric(
        df["total_inr"], errors="coerce"
    ).fillna(0)

    quantity = pd.to_numeric(
        df["quantity"], errors="coerce"
    ).fillna(0)

    spending = (
        df.assign(_revenue=revenue)
        .groupby("customer_name")["_revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    cancelled = df["status"].astype(str).str.casefold().isin(
        ["cancelled", "canceled"]
    ).sum()

    return {
        "order_count": int(len(df)),
        "cancelled_count": int(cancelled),
        "revenue_inr": round(float(revenue.sum()), 2),
        "quantity_sold": int(quantity.sum()),
        "top_customer": str(spending.index[0]),
        "top_customer_spending_inr": round(
            float(spending.iloc[0]), 2
        )
    }


# AI AGENT: The model chooses which tool to call
def ask_order_assistant(question: str):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "Groq API is not configured. Add GROQ_API_KEY "
            "to your .env file and restart the server."
        )

    try:
        client = Groq(
            api_key=api_key,
            timeout=30.0,
            max_retries=0
        )

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "find_order",
                    "description": (
                        "Find one order using its order ID. "
                        "Use for questions about an individual order."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "order_id": {"type": "string"}
                        },
                        "required": ["order_id"],
                        "additionalProperties": False
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_orders",
                    "description": (
                        "Calculate order count, revenue, cancelled orders, "
                        "quantity sold, and top customer spending. "
                        "Supports category, status, and month filters. "
                        "Use empty strings for unused filters."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {"type": "string"},
                            "status": {"type": "string"},
                            "month": {
                                "type": "string",
                                "description": "Month number 1-12 or empty."
                            }
                        },
                        "required": ["category", "status", "month"],
                        "additionalProperties": False
                    }
                }
            }
        ]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an order-data assistant. You must use the "
                    "provided tools for questions about order records "
                    "or statistics. Choose the correct tool based on "
                    "the user's question. Never invent data. If no order "
                    "is found, say so clearly. Explain results in simple "
                    "English. All money amounts are in Indian rupees (INR)."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]

        # Allow multiple tool calls, with a limit to prevent endless loops.
        for _ in range(5):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0
            )

            message = response.choices[0].message
            messages.append(message)

            if not message.tool_calls:
                return message.content or "Sorry, I could not generate an answer."

            for tool_call in message.tool_calls:
                try:
                    arguments = json.loads(tool_call.function.arguments)

                    if tool_call.function.name == "find_order":
                        result = find_order(**arguments)

                    elif tool_call.function.name == "analyze_orders":
                        result = analyze_orders(**arguments)

                    else:
                        result = {"error": "Unknown tool requested."}

                except Exception as exc:
                    print("TOOL ERROR:", type(exc).__name__, str(exc))
                    result = {
                        "error": "The tool failed to process this request."
                    }

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, default=str)
                })

        return "Too many tool steps. Please try a simpler question."

    except Exception as exc:
        print("AI ERROR:", type(exc).__name__, str(exc))
        return (
            "The AI request failed. Check the VS Code terminal "
            "for the error details."
        )

