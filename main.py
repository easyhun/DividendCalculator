import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

monthly_dividends = {}


# 표 업데이트
def update_data(): 
    stock_name = stock_name_entry.get()
    quantity = int(quantity_entry.get())
    dividend = int(dividend_entry.get())
    payment = payment_combobox.get()

    #monthly_dividend = quantity * dividend

    for item in tree.get_children():
        if tree.item(item, "text") == stock_name:
            tree.item(item, values=(quantity, dividend, payment))
            break
    else:
        tree.insert('', 'end', text=stock_name, values=(quantity, dividend, payment))
        save_data()

def delete_data():
    selected_item = tree.selection()[0]
    tree.delete(selected_item)
    save_data()       
    

#def update_combobox():
    #p_value = ["월배당", "36912"]
    #payment_combobox["values"] = p_value

def save_data():
    with open("stock_data.txt", "w") as file:
        for item in tree.get_children():
            stock_name = tree.item(item, "text")
            quantity, dividend, payment = tree.item(item, "values")
            file.write(f"{stock_name},{quantity},{dividend},{payment}\n")

def load_data():
    try:
        with open("stock_data.txt", "r") as file:
            for line in file:
                stock_name, quantity, dividend, payment = line.strip().split(",")
                tree.insert('', 'end', text=stock_name, values=(quantity, dividend, payment))
    except FileNotFoundError:
        pass


# tkinter
root = tk.Tk()
root.title("Stock Dividend Data")

# Frame 생성
frame = tk.Frame(root, bg="lightblue")
frame.pack(side="left", fill="both", expand=True)
frame2 = tk.Frame(root, bg="lightgreen")
frame2.pack(side="right", fill="both", expand=True)

# 표 생성
tree = ttk.Treeview(frame, columns=("Quantity", "Dividend per Share", "Payment"))
tree.heading("#0", text="종목명")
tree.heading("Quantity", text="수량")
tree.heading("Dividend per Share", text="주당 배당금")
tree.heading("Payment", text="주기")
tree.grid(row=0, column=0, columnspan=3, sticky="nsew")

# 위젯
stock_name_label = tk.Label(frame, text="종목명 :")
stock_name_label.grid(row=1, column=0, pady=5)
stock_name_entry = tk.Entry(frame)
stock_name_entry.grid(row=1, column=1, pady=5)

quantity_label = tk.Label(frame, text="수량 :")
quantity_label.grid(row=2, column=0, pady=5)
quantity_entry = tk.Entry(frame)
quantity_entry.grid(row=2, column=1, pady=5)

dividend_label = tk.Label(frame, text="주당 배당금 :")
dividend_label.grid(row=3, column=0, pady=5)
dividend_entry = tk.Entry(frame)
dividend_entry.grid(row=3, column=1, pady=5)

payment_label = tk.Label(frame, text="배당 주기 :")
payment_label.grid(row=4, column=0, pady=5)
payment_combobox = ttk.Combobox(frame, values=["월배당", "36912"])
payment_combobox.grid(row=4, column=1, pady=5)

update_button = tk.Button(frame, text="Update Data", command=update_data)
update_button.grid(row=5, column=0, columnspan=2, pady=10)
delete_button = tk.Button(frame, text="Delete Data", command=delete_data)
delete_button.grid(row=5, column=1, columnspan=2, pady=10)

# 콤보박스 업데이트
#update_button = tk.Button(frame, text="Update Combobox", command=update_combobox)
#update_button.grid(row=2, column=0, columnspan=2, pady=10)

load_data()
root.mainloop()
