import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import styles

# 차트 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
styles.default_font()
plt.rc('font', family=font_name)

monthly_dividends = {i: 0 for i in range(1, 13)}  # 월별 총 배당금을 저장할 딕셔너리

def update_monthly_dividends():
    # 초기화
    for i in range(1, 13):
        monthly_dividends[i] = 0

    # 트리뷰 데이터를 기반으로 월별 배당금 계산
    for item in tree.get_children():
        quantity, dividend, payment, divResult = tree.item(item, "values") #수량, 배당금, 주기, 총배당금
        quantity = int(quantity)
        dividend = int(dividend)
        divResult = int(divResult)
        if payment == "월배당":
            for i in range(1, 13):
                monthly_dividends[i] += divResult
        elif payment == "36912":
            for i in [3, 6, 9, 12]:
                monthly_dividends[i] += divResult

# 표 업데이트
def update_data():
    stock_name = stock_name_entry.get()
    quantity = int(quantity_entry.get())
    dividend = int(dividend_entry.get())
    payment = payment_combobox.get()
    divResult = quantity * dividend

    for item in tree.get_children():
        if tree.item(item, "text") == stock_name:
            tree.item(item, values=(quantity, dividend, payment, divResult))
            break
    else:
        tree.insert('', 'end', text=stock_name, values=(quantity, dividend, payment, divResult))

    update_monthly_dividends()
    save_tree_data()
    save_dividends()
    plot_chart()

def delete_data():
    selected_item = tree.selection()[0]
    tree.delete(selected_item)
    update_monthly_dividends()
    save_tree_data()
    save_dividends()
    plot_chart()

def save_tree_data():
    with open("stock_data.txt", "w") as file:
        for item in tree.get_children():
            stock_name = tree.item(item, "text")
            quantity, dividend, payment, divResult = tree.item(item, "values")
            file.write(f"{stock_name},{quantity},{dividend},{payment},{divResult}\n")

def load_data():
    if os.path.exists("stock_data.txt"):
        with open("stock_data.txt", "r") as file:
            for line in file:
                stock_name, quantity, dividend, payment, divResult = line.strip().split(",")
                tree.insert('', 'end', text=stock_name, values=(quantity, dividend, payment, divResult))

def save_dividends():
    with open("dividends.txt", "w") as file:
        for month, dividend in monthly_dividends.items():
            file.write(f"{month},{dividend}\n")

def load_dividends():
    if os.path.exists("dividends.txt"):
        with open("dividends.txt", "r") as file:
            for line in file:
                month, dividend = line.strip().split(",")
                monthly_dividends[int(month)] = int(dividend)

# 차트 설정
def plot_chart():
    # 기존 차트 삭제
    for widget in frame2.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)  # 행, 열, 인덱스
    periods = list(range(1, 13))
    values = [monthly_dividends[i] for i in periods]
    ax.bar(periods, values, color='lightblue')
    ax.set_xlabel('월')
    ax.set_ylabel('총 배당금')
    ax.set_title('배당금 차트')

    # X축 눈금 위치와 레이블 설정
    ax.set_xticks(periods)
    ax.set_xticklabels([str(i) for i in periods])

    canvas = FigureCanvasTkAgg(fig, master=frame2)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        stock_name = item["text"]
        quantity, dividend, payment, divResult = item["values"]
        stock_name_entry.delete(0, tk.END)
        stock_name_entry.insert(0, stock_name)
        quantity_entry.delete(0, tk.END)
        quantity_entry.insert(0, quantity)
        dividend_entry.delete(0, tk.END)
        dividend_entry.insert(0, dividend)
        payment_combobox.set(payment)

# tkinter
root = tk.Tk()
root.title("Stock Dividend Data")

# Frame 생성
frame = tk.Frame(root, bg="#AD88C6")
frame.pack(side="left", fill="both", expand=True)
frame2 = tk.Frame(root, bg="lightgreen")
frame2.pack(side="right", fill="both", expand=True)
styles.frame(frame)

# 표 생성
tree = ttk.Treeview(frame, columns=("Quantity", "Dividend per Share", "Payment", "DivResult"))
tree.heading("#0", text="종목명")
tree.heading("Quantity", text="수량")
tree.heading("Dividend per Share", text="주당 배당금")
tree.heading("Payment", text="주기")
tree.heading("DivResult", text="총 배당금")
tree.grid(row=0, column=0, columnspan=3, sticky="nsew")
tree.bind("<<TreeviewSelect>>", on_tree_select)
styles.treeview(tree)

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

load_data()
update_monthly_dividends()
load_dividends()
plot_chart()
root.mainloop()
