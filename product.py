from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # ================= VARIABLES =================
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.var_pid = StringVar()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.cat_list = []
        self.sup_list = []

        self.fetch_cat_sup()

        # ================= LEFT FRAME =================
        product_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        Label(product_Frame, text="Manage Product Details",
              font=("goudy old style", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        # ================= FORM =================
        labels = ["Category", "Supplier", "Name", "Price", "Quantity", "Status"]
        y_positions = [60, 110, 160, 210, 260, 310]

        for i in range(len(labels)):
            Label(product_Frame, text=labels[i],
                  font=("goudy old style", 18), bg="white").place(x=30, y=y_positions[i])

        self.cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat,
                                     values=self.cat_list, state='readonly', justify=CENTER)
        self.cmb_cat.place(x=150, y=60, width=200)

        self.cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup,
                                     values=self.sup_list, state='readonly', justify=CENTER)
        self.cmb_sup.place(x=150, y=110, width=200)

        Entry(product_Frame, textvariable=self.var_name, bg="lightyellow").place(x=150, y=160, width=200)
        Entry(product_Frame, textvariable=self.var_price, bg="lightyellow").place(x=150, y=210, width=200)
        Entry(product_Frame, textvariable=self.var_qty, bg="lightyellow").place(x=150, y=260, width=200)

        self.cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status,
                                        values=("Active", "Inactive"), state='readonly', justify=CENTER)
        self.cmb_status.place(x=150, y=310, width=200)

        # ================= BUTTONS =================
        Button(product_Frame, text="Save", command=self.add,
               bg="#2196f3", fg="white").place(x=10, y=400, width=100)

        Button(product_Frame, text="Update", command=self.update,
               bg="#4caf50", fg="white").place(x=120, y=400, width=100)

        Button(product_Frame, text="Delete", command=self.delete,
               bg="#f44336", fg="white").place(x=230, y=400, width=100)

        Button(product_Frame, text="Clear", command=self.clear,
               bg="#607d8b", fg="white").place(x=340, y=400, width=100)

        # ================= SEARCH =================
        SearchFrame = LabelFrame(self.root, text="Search Product", bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        self.cmb_search = ttk.Combobox(SearchFrame, textvariable=self.var_searchby,
                                        values=("Select", "Category", "Supplier", "name"),
                                        state='readonly')
        self.cmb_search.place(x=10, y=10, width=180)
        self.cmb_search.current(0)

        Entry(SearchFrame, textvariable=self.var_searchtxt, bg="lightyellow").place(x=200, y=10)

        Button(SearchFrame, text="Search", command=self.search,
               bg="#4caf50", fg="white").place(x=410, y=9, width=150, height=30)

        # ================= TABLE =================
        product_frame = Frame(self.root, bd=3, relief=RIDGE)
        product_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(product_frame, orient=VERTICAL)
        scrollx = Scrollbar(product_frame, orient=HORIZONTAL)

        self.ProductTable = ttk.Treeview(product_frame,
                                          columns=("pid", "Category", "Supplier", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set,
                                          xscrollcommand=scrollx.set)

        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.pack(side=BOTTOM, fill=X)

        scrolly.config(command=self.ProductTable.yview)
        scrollx.config(command=self.ProductTable.xview)

        self.ProductTable.heading("pid", text="ID")
        self.ProductTable.heading("Category", text="Category")
        self.ProductTable.heading("Supplier", text="Supplier")
        self.ProductTable.heading("name", text="Name")
        self.ProductTable.heading("price", text="Price")
        self.ProductTable.heading("qty", text="Qty")
        self.ProductTable.heading("status", text="Status")

        self.ProductTable["show"] = "headings"

        for col in self.ProductTable["columns"]:
            self.ProductTable.column(col, width=100)

        self.ProductTable.pack(fill=BOTH, expand=1)

        self.ProductTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================= FETCH CATEGORY & SUPPLIER =================
    def fetch_cat_sup(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT name FROM category")
            cat = cur.fetchall()
            self.cat_list = ["Select"] + [i[0] for i in cat]

            cur.execute("SELECT name FROM supplier")
            sup = cur.fetchall()
            self.sup_list = ["Select"] + [i[0] for i in sup]

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= ADD PRODUCT =================
    def add(self):
        if self.var_cat.get() == "Select" or self.var_sup.get() == "Select":
            messagebox.showerror("Error", "Select Category and Supplier")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM product WHERE name=?", (self.var_name.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Product already exists")
                return

            cur.execute("""
                INSERT INTO product (Category, Supplier, name, price, qty, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                self.var_cat.get(),
                self.var_sup.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_qty.get(),
                self.var_status.get()
            ))

            con.commit()
            messagebox.showinfo("Success", "Product Added")
            self.show()
            self.clear()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= SHOW =================
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()

            self.ProductTable.delete(*self.ProductTable.get_children())

            for row in rows:
                self.ProductTable.insert("", END, values=row)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= SELECT ROW =================
    def get_data(self, ev):
        f = self.ProductTable.focus()
        row = self.ProductTable.item(f)["values"]

        if row:
            self.var_pid.set(row[0])
            self.var_cat.set(row[1])
            self.var_sup.set(row[2])
            self.var_name.set(row[3])
            self.var_price.set(row[4])
            self.var_qty.set(row[5])
            self.var_status.set(row[6])

    # ================= UPDATE =================
    def update(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Select Product")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("""
                UPDATE product SET
                Category=?, Supplier=?, name=?, price=?, qty=?, status=?
                WHERE pid=?
            """, (
                self.var_cat.get(),
                self.var_sup.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_qty.get(),
                self.var_status.get(),
                self.var_pid.get()
            ))

            con.commit()
            messagebox.showinfo("Success", "Updated")
            self.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= DELETE =================
    def delete(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Select Product")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("DELETE FROM product WHERE pid=?", (self.var_pid.get(),))
            con.commit()

            messagebox.showinfo("Success", "Deleted")
            self.show()
            self.clear()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= CLEAR =================
    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    # ================= SEARCH =================
    def search(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            if self.var_searchby.get() == "Select":
                messagebox.showerror("Error", "Select search type")
                return

            query = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE ?"
            cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))

            rows = cur.fetchall()

            self.ProductTable.delete(*self.ProductTable.get_children())

            for row in rows:
                self.ProductTable.insert("", END, values=row)

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()