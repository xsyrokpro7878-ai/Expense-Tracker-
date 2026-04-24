import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# Глобальные переменные
expenses = []

# Файл для хранения данных
DATA_FILE = 'expenses.json'

# Загрузка данных из JSON
def load_data():
    global expenses
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            expenses = json.load(f)
    else:
        expenses = []

# Сохранение данных в JSON
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

# Добавление расхода
def add_expense():
    amount_str = entry_amount.get()
    category = entry_category.get()
    date_str = entry_date.get()

    # Проверка корректности ввода
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Введите корректную положительную сумму.")
        return

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_formatted = date_obj.strftime("%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
        return

    expense = {
        'amount': amount,
        'category': category,
        'date': date_formatted
    }
    expenses.append(expense)
    save_data()
    update_table()
    clear_entries()

# Очистка полей ввода
def clear_entries():
    entry_amount.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# Обновление таблицы
def update_table(filtered_expenses=None):
    for row in tree.get_children():
        tree.delete(row)
    data = filtered_expenses if filtered_expenses is not None else expenses
    for exp in data:
        tree.insert('', tk.END, values=(exp['amount'], exp['category'], exp['date']))
    calculate_total()

# Расчёт суммы за текущий фильтр/все
def calculate_total():
    total = 0
    for item in tree.get_children():
        vals = tree.item(item)['values']
        total += float(vals[0])
    label_total.config(text=f"Общая сумма: {total:.2f}")

# Фильтрация данных
def filter_expenses():
    category_filter = combo_category.get()
    date_from = entry_date_from.get()
    date_to = entry_date_to.get()

    filtered = expenses
    if category_filter != 'Все':
        filtered = [e for e in filtered if e['category'] == category_filter]
    if date_from:
        try:
            df = datetime.strptime(date_from, "%Y-%m-%d")
            filtered = [e for e in filtered if datetime.strptime(e['date'], "%Y-%m-%d") >= df]
        except:
            messagebox.showerror("Ошибка", "Некорректный формат даты (ГГГГ-ММ-ДД).")
            return
    if date_to:
        try:
            dt = datetime.strptime(date_to, "%Y-%m-%d")
            filtered = [e for e in filtered if datetime.strptime(e['date'], "%Y-%m-%d") <= dt]
        except:
            messagebox.showerror("Ошибка", "Некорректный формат даты (ГГГГ-ММ-ДД).")
            return

    update_table(filtered)

# Сброс фильтров
def reset_filters():
    combo_category.set('Все')
    entry_date_from.delete(0, tk.END)
    entry_date_to.delete(0, tk.END)
    update_table()

# Загрузка данных при запуске
load_data()

# Создание GUI
root = tk.Tk()
root.title("Expense Tracker")

# Ввод расхода
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Сумма:").grid(row=0, column=0, padx=5)
entry_amount = tk.Entry(frame_input)
entry_amount.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="Категория:").grid(row=0, column=2, padx=5)
entry_category = tk.Entry(frame_input)
entry_category.grid(row=0, column=3, padx=5)

tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4, padx=5)
entry_date = tk.Entry(frame_input)
entry_date.grid(row=0, column=5, padx=5)

btn_add = tk.Button(frame_input, text="Добавить расход", command=add_expense)
btn_add.grid(row=0, column=6, padx=5)

# Таблица расходов
columns = ('amount', 'category', 'date')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('amount', text='Сумма')
tree.heading('category', text='Категория')
tree.heading('date', text='Дата')
tree.pack(pady=10)

# Фильтр
frame_filter = tk.Frame(root)
frame_filter.pack(pady=10)

tk.Label(frame_filter, text="Фильтр по категории:").grid(row=0, column=0, padx=5)
categories = ['Все'] + list({e['category'] for e in expenses})
combo_category = ttk.Combobox(frame_filter, values=categories, state='readonly')
combo_category.set('Все')
combo_category.grid(row=0, column=1, padx=5)
combo_category.bind("<<ComboboxSelected>>", lambda e: filter_expenses())

tk.Label(frame_filter, text="Дата от:").grid(row=0, column=2, padx=5)
entry_date_from = tk.Entry(frame_filter)
entry_date_from.grid(row=0, column=3, padx=5)

tk.Label(frame_filter, text="Дата до:").grid(row=0, column=4, padx=5)
entry_date_to = tk.Entry(frame_filter)
entry_date_to.grid(row=0, column=5, padx=5)

btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=filter_expenses)
btn_filter.grid(row=0, column=6, padx=5)

btn_reset = tk.Button(frame_filter, text="Сбросить", command=reset_filters)
btn_reset.grid(row=0, column=7, padx=5)

# Общая сумма
label_total = tk.Label(root, text="Общая сумма: 0.00", font=('Arial', 14))
label_total.pack(pady=10)

# Обновление таблицы при запуске
update_table()

root.mainloop()