from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import time
import os


class billClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        self.cart_list = []
        self.chk_print = 0

        # ---------------- VARIABLES ----------------
        self.var_search = StringVar()
        self.var_cname = StringVar()
        self.var_contact = StringVar()

        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        self.var_cal_input = StringVar()   # ✅ FIXED

        # ---------------- PRODUCT FRAME ----------------
        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        Label(ProductFrame1, text="All Products",
              font=("goudy old style", 20, "bold"),
              bg="#262626", fg="white").pack(fill=X)

        Entry(ProductFrame1, textvariable=self.var_search,
              bg="lightyellow").place(x=10, y=50, width=200)

        Button(ProductFrame1, text="Search", command=self.search).place(x=220, y=50)
        Button(ProductFrame1, text="Show All", command=self.show).place(x=300, y=50)

        self.product_Table = ttk.Treeview(ProductFrame1,
                                          columns=("pid", "name", "price", "qty", "status"),
                                          show="headings")

        for col in ("pid", "name", "price", "qty", "status"):
            self.product_Table.heading(col, text=col.upper())
            self.product_Table.column(col, width=80)

        self.product_Table.place(x=0, y=100, relwidth=1, height=430)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        # ---------------- CUSTOMER ----------------
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        Entry(CustomerFrame, textvariable=self.var_cname).place(x=80, y=35, width=180)
        Entry(CustomerFrame, textvariable=self.var_contact).place(x=380, y=35, width=140)

        # ---------------- CART ----------------
        Cart_Frame = Frame(self.root, bd=3, relief=RIDGE)
        Cart_Frame.place(x=420, y=190, width=530, height=350)

        self.CartTable = ttk.Treeview(Cart_Frame,
                                      columns=("pid", "name", "price", "qty"),
                                      show="headings")

        for col in ("pid", "name", "price", "qty"):
            self.CartTable.heading(col, text=col.upper())
            self.CartTable.column(col, width=100)

        self.CartTable.pack(fill=BOTH, expand=1)

        # ---------------- BILL AREA ----------------
        billFrame = Frame(self.root, bd=2, relief=RIDGE)
        billFrame.place(x=953, y=110, width=400, height=410)

        self.txt_bill_area = Text(billFrame)
        self.txt_bill_area.pack(fill=BOTH, expand=1)

        self.show()
        self.update_date_time()

    # ---------------- PRODUCT LOAD ----------------
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT pid,name,price,qty,status FROM product")
        rows = cur.fetchall()

        self.product_Table.delete(*self.product_Table.get_children())
        for r in rows:
            self.product_Table.insert('', END, values=r)

        con.close()

    # ---------------- SEARCH ----------------
    def search(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        cur.execute("SELECT pid,name,price,qty,status FROM product WHERE name LIKE ?",
                    ('%' + self.var_search.get() + '%',))
        rows = cur.fetchall()

        self.product_Table.delete(*self.product_Table.get_children())
        for r in rows:
            self.product_Table.insert('', END, values=r)

        con.close()

    # ---------------- SELECT PRODUCT ----------------
    def get_data(self, ev):
        f = self.product_Table.focus()
        if not f:
            return

        row = self.product_Table.item(f)['values']
        if not row:
            return

        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    # ---------------- CLOCK ----------------
    def update_date_time(self):
        time_ = time.strftime("%H:%M:%S")
        date_ = time.strftime("%d-%m-%Y")

        self.root.after(1000, self.update_date_time)