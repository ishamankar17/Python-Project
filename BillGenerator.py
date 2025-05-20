from tkinter import *
import random
from tkinter import messagebox
import os

root = Tk()
root.geometry("1250x700")
root.title("Billing Software")

# Create bills folder if not exists
if not os.path.exists("bills"):
    os.mkdir("bills")

# Prices
prices = {
    "Lays": 10, "Kurkure": 15, "Biscuits": 20, "Chips": 10,
    "Popcorn": 25, "Namkeen": 20, "Chocolate": 30, "Sugar": 40,
    "Oil": 100, "Wheat": 60, "Rice": 50, "Dal": 70, "Salt": 10, "Tea": 120,
    "Soap": 25, "Shampoo": 60, "Toothpaste": 40, "Facewash": 70,
    "Sanitizer": 50, "Tissue": 30, "Handwash": 45
}

# Variables
items = {k: IntVar() for k in prices}
c_name = StringVar()
c_phone = StringVar()
bill_no = StringVar()
bill_no.set(str(random.randint(1000, 9999)))
snacks_total = StringVar()
grocery_total = StringVar()
hygiene_total = StringVar()
total_bill = StringVar()

# Functions
def clear():
    for var in items.values():
        var.set(0)
    c_name.set("")
    c_phone.set("")
    bill_no.set(str(random.randint(1000, 9999)))
    snacks_total.set("")
    grocery_total.set("")
    hygiene_total.set("")
    total_bill.set("")
    text_area.delete("1.0", END)

def total():
    stotal = sum(items[i].get() * prices[i] for i in ['Lays', 'Kurkure', 'Biscuits', 'Chips', 'Popcorn', 'Namkeen', 'Chocolate'])
    gtotal = sum(items[i].get() * prices[i] for i in ['Sugar', 'Oil', 'Wheat', 'Rice', 'Dal', 'Salt', 'Tea'])
    htotal = sum(items[i].get() * prices[i] for i in ['Soap', 'Shampoo', 'Toothpaste', 'Facewash', 'Sanitizer', 'Tissue', 'Handwash'])
    
    snacks_total.set(f"₹ {stotal}")
    grocery_total.set(f"₹ {gtotal}")
    hygiene_total.set(f"₹ {htotal}")
    total_bill.set(f"₹ {stotal + gtotal + htotal}")

def bill_area():
    if not c_name.get() or not c_phone.get():
        messagebox.showerror("Error", "Customer Details are Required!")
        return
    if not c_phone.get().isdigit() or len(c_phone.get()) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit phone number")
        return

    text_area.delete("1.0", END)
    text_area.insert(END, "\tWelcome to My Store\n")
    text_area.insert(END, f"\nBill No: {bill_no.get()}")
    text_area.insert(END, f"\nCustomer Name: {c_name.get()}")
    text_area.insert(END, f"\nPhone No: {c_phone.get()}")
    text_area.insert(END, "\n====================================")
    text_area.insert(END, "\nProduct\t\tQty\tPrice")
    text_area.insert(END, "\n====================================")

    total_amt = 0
    for item in prices:
        qty = items[item].get()
        if qty > 0:
            cost = qty * prices[item]
            text_area.insert(END, f"\n{item}\t\t{qty}\t₹ {cost}")
            total_amt += cost

    text_area.insert(END, "\n====================================")
    text_area.insert(END, f"\nTotal Bill:\t\t\t{total_bill.get()}")
    text_area.insert(END, "\n====================================")

def save_bill():
    data = text_area.get("1.0", END)
    if not data.strip():
        messagebox.showerror("Error", "No bill to save.")
        return
    with open(f"bills/{bill_no.get()}.txt", "w") as f:
        f.write(data)
    messagebox.showinfo("Saved", f"Bill {bill_no.get()} saved successfully!")

def print_bill():
    file = f"bills/{bill_no.get()}.txt"
    save_bill()
    os.startfile(file, "print")

# Customer Details Frame
F1 = LabelFrame(root, text="Customer Details", font=("times new roman", 15, "bold"), fg="gold", bg="cadetblue")
F1.pack(fill=X)

Label(F1, text="Customer Name", bg="cadetblue", fg="white", font="arial 12 bold").grid(row=0, column=0, padx=20, pady=5)
Entry(F1, textvariable=c_name, width=20).grid(row=0, column=1, padx=10)

Label(F1, text="Phone Number", bg="cadetblue", fg="white", font="arial 12 bold").grid(row=0, column=2, padx=20, pady=5)
Entry(F1, textvariable=c_phone, width=20).grid(row=0, column=3, padx=10)

Label(F1, text="Bill Number", bg="cadetblue", fg="white", font="arial 12 bold").grid(row=0, column=4, padx=20, pady=5)
Entry(F1, textvariable=bill_no, width=20).grid(row=0, column=5, padx=10)

# Product Category Frames
def create_product_frame(title, items_list, row_start):
    frame = LabelFrame(root, text=title, font=("times new roman", 15, "bold"), fg="gold", bg="cadetblue")
    frame.place(x=5, y=row_start, width=325, height=240)
    for i, item in enumerate(items_list):
        Label(frame, text=item, font="arial 12 bold", bg="cadetblue", fg="white").grid(row=i, column=0, padx=10, pady=5)
        Entry(frame, textvariable=items[item], width=10).grid(row=i, column=1, padx=10, pady=5)

create_product_frame("Snacks", ['Lays', 'Kurkure', 'Biscuits', 'Chips', 'Popcorn', 'Namkeen', 'Chocolate'], 70)
create_product_frame("Grocery", ['Sugar', 'Oil', 'Wheat', 'Rice', 'Dal', 'Salt', 'Tea'], 320)
create_product_frame("Hygiene", ['Soap', 'Shampoo', 'Toothpaste', 'Facewash', 'Sanitizer', 'Tissue', 'Handwash'], 570)

# Bill Area Frame
F4 = Frame(root, bd=10, relief=GROOVE)
F4.place(x=340, y=70, width=620, height=560)
bill_title = Label(F4, text="Bill Area", font="arial 15 bold", bd=7, relief=GROOVE).pack(fill=X)
scroll_y = Scrollbar(F4, orient=VERTICAL)
text_area = Text(F4, yscrollcommand=scroll_y.set)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_y.config(command=text_area.yview)
text_area.pack(fill=BOTH, expand=1)

# Button Frame
F5 = LabelFrame(root, text="Bill Menu", font=("times new roman", 15, "bold"), fg="gold", bg="cadetblue")
F5.place(x=975, y=70, width=270, height=200)

Label(F5, text="Snacks Total", font="arial 12 bold", bg="cadetblue", fg="white").grid(row=0, column=0, padx=10, pady=5)
Entry(F5, textvariable=snacks_total, width=15).grid(row=0, column=1, padx=10, pady=5)

Label(F5, text="Grocery Total", font="arial 12 bold", bg="cadetblue", fg="white").grid(row=1, column=0, padx=10, pady=5)
Entry(F5, textvariable=grocery_total, width=15).grid(row=1, column=1, padx=10, pady=5)

Label(F5, text="Hygiene Total", font="arial 12 bold", bg="cadetblue", fg="white").grid(row=2, column=0, padx=10, pady=5)
Entry(F5, textvariable=hygiene_total, width=15).grid(row=2, column=1, padx=10, pady=5)

Label(F5, text="Total Bill", font="arial 12 bold", bg="cadetblue", fg="white").grid(row=3, column=0, padx=10, pady=5)
Entry(F5, textvariable=total_bill, width=15).grid(row=3, column=1, padx=10, pady=5)

F6 = Frame(root, bd=7, relief=GROOVE)
F6.place(x=975, y=280, width=270, height=160)

Button(F6, text="Total", command=total, bg="cadetblue", fg="white", width=12, pady=10, font="arial 12 bold").grid(row=0, column=0, padx=10, pady=10)
Button(F6, text="Generate Bill", command=bill_area, bg="cadetblue", fg="white", width=12, pady=10, font="arial 12 bold").grid(row=0, column=1, padx=10, pady=10)
Button(F6, text="Save Bill", command=save_bill, bg="cadetblue", fg="white", width=12, pady=10, font="arial 12 bold").grid(row=1, column=0, padx=10, pady=10)
Button(F6, text="Print Bill", command=print_bill, bg="cadetblue", fg="white", width=12, pady=10, font="arial 12 bold").grid(row=1, column=1, padx=10, pady=10)
Button(F6, text="Clear", command=clear, bg="cadetblue", fg="white", width=27, pady=10, font="arial 12 bold").grid(row=2, columnspan=2, pady=10)

root.mainloop()
