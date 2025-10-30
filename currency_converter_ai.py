import tkinter as tk
from tkinter import ttk
import requests
import random

currencies = ["USD", "INR", "EUR", "GBP", "JPY", "CAD", "AUD"]

def get_live_rate(amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['rates'][to_currency]
    else:
        return None

def get_predicted_rate(from_currency, to_currency):
    # Yaha dummy AI prediction logic hai, real model/API ho toh wahi lagao
    base_rate = get_live_rate(1, from_currency, to_currency)
    if base_rate:
        variation = base_rate * (random.uniform(-0.03, 0.03))
        predicted_rate = base_rate + variation
        return round(predicted_rate, 4)
    return None

def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_combo.get()
        to_currency = to_combo.get()
        if from_currency == to_currency:
            result_label.config(text="Please select different currencies.")
            return
        converted = get_live_rate(amount, from_currency, to_currency)
        if converted:
            result_label.config(text=f"{amount} {from_currency} = {round(converted, 2)} {to_currency}")
        else:
            result_label.config(text="API error! Try again.")
    except ValueError:
        result_label.config(text="Please enter a valid number!")

def predict_currency_rate():
    from_currency = from_combo.get()
    to_currency = to_combo.get()
    if from_currency == to_currency:
        prediction_label.config(text="Select different currencies to predict.")
        return
    predicted_rate = get_predicted_rate(from_currency, to_currency)
    if predicted_rate:
        prediction_label.config(
            text=f"Predicted 1 {from_currency} = {predicted_rate} {to_currency} (next day)"
        )
    else:
        prediction_label.config(text="Prediction unavailable. Try again.")

root = tk.Tk()
root.title("Currency Converter with AI Prediction")
root.geometry("450x400")
root.config(bg="#1e1e1e")

title_label = tk.Label(
    root,
    text="💱 Currency Converter with AI Prediction",
    font=("Arial", 16, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title_label.pack(pady=10)

tk.Label(root, text="Enter Amount:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack()
amount_entry = tk.Entry(root, font=("Arial", 12), width=15)
amount_entry.pack(pady=5)

tk.Label(root, text="From:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack()
from_combo = ttk.Combobox(root, values=currencies, font=("Arial", 12))
from_combo.current(0)
from_combo.pack(pady=5)

tk.Label(root, text="To:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack()
to_combo = ttk.Combobox(root, values=currencies, font=("Arial", 12))
to_combo.current(1)
to_combo.pack(pady=5)

convert_btn = tk.Button(
    root,
    text="Convert",
    font=("Arial", 12, "bold"),
    bg="orange",
    fg="black",
    command=convert_currency
)
convert_btn.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="lightgreen")
result_label.pack(pady=10)

predict_btn = tk.Button(
    root,
    text="Predict NEXT Day Rate",
    font=("Arial", 12, "bold"),
    bg="#4caf50",
    fg="white",
    command=predict_currency_rate
)
predict_btn.pack(pady=10)

prediction_label = tk.Label(root, text="", font=("Arial", 12, "italic"), bg="#1e1e1e", fg="yellow")
prediction_label.pack(pady=5)

root.mainloop()
