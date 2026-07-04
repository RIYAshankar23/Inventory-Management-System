from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # ================= VARIABLES =================
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.var_searchtxt = StringVar()

        # ================= TITLE =================
        Label(self.root, text="Supplier Details",
              font=("goudy old style", 20, "bold"),
              bg="#0f4d7d", fg="white").place(x=50, y=10, width=1000, height=40)

        # ================= SEARCH =================
        Label(self.root, text="Invoice No.", bg="white",
              font=("goudy old style", 15)).place(x=700, y=80)

        Entry(self.root, textvariable=self.var_searchtxt,
              font=("goudy old style", 15),
              bg="lightyellow").place(x=850, y=80, width=160)

        Button(self.root, text="Search", command=self.search,
               font=("goudy old style", 15),
               bg="#4caf50", fg="white").place(x=980, y=79, width=100, height=28)

        # ================= INPUT FIELDS =================
        labels = ["Invoice No.", "Name", "Contact", "Description"]
        y = [80, 120, 160, 200]

        for i in range(3):
            Label(self.root, text=labels[i],
                  font=("goudy old style", 15),
                  bg="white").place(x=50, y=y[i])

        Entry(self.root, textvariable=self.var_sup_invoice,
              bg="lightyellow").place(x=180, y=80, width=180)

        Entry(self.root, textvariable=self.var_name,
              bg="lightyellow").place(x=180, y=120, width=180)

        Entry(self.root, textvariable=self.var_contact,
              bg="lightyellow").place(x=180, y=160, width=180)

        Label(self.root, text="Description",
              font=("goudy old style", 15),
              bg="white").place(x=50, y=200)

        self.txt_desc = Text(self.root, bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=470, height=120)

        # ================= BUTTONS =================
        Button(self.root, text="Save", command=self.add,
               bg="#2196f3", fg="white").place(x=180, y=370, width=110, height=35)

        Button(self.root, text="Update", command=self.update,
               bg="#4caf50", fg="white").place(x=300, y=370, width=110, height=35)

        Button(self.root, text="Delete", command=self.delete,
               bg="#f44336", fg="white").place(x=420, y=370, width=110, height=35)

        Button(self.root, text="Clear", command=self.clear,
               bg="#607d8b", fg="white").place(x=540, y=370, width=110, height=35)

        # ================= TABLE =================
        sup_frame = Frame(self.root, bd=3, relief=RIDGE)
        sup_frame.place(x=700, y=120, width=380, height=350)

        scroll = Scrollbar(sup_frame, orient=VERTICAL)

        self.SupplierTable = ttk.Treeview(
            sup_frame,
            columns=("invoice", "name", "contact", "desc"),
            yscrollcommand=scroll.set
        )

        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=self.SupplierTable.yview)

        self.SupplierTable.pack(fill=BOTH, expand=1)

        self.SupplierTable.heading("invoice", text="Invoice")
        self.SupplierTable.heading("name", text="Name")
        self.SupplierTable.heading("contact", text="Contact")
        self.SupplierTable.heading("desc", text="Description")

        self.SupplierTable["show"] = "headings"

        for col in ("invoice", "name", "contact", "desc"):
            self.SupplierTable.column(col, width=90)

        self.SupplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================= ADD =================
    def add(self):
        if self.var_sup_invoice.get() == "":
            messagebox.showerror("Error", "Invoice is required")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?",
                        (self.var_sup_invoice.get(),))

            if cur.fetchone():
                messagebox.showerror("Error", "Invoice already exists")
                return

            cur.execute("""
                INSERT INTO supplier (invoice, name, contact, desc)
                VALUES (?, ?, ?, ?)
            """, (
                self.var_sup_invoice.get(),
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_desc.get("1.0", END)
            ))

            con.commit()
            messagebox.showinfo("Success", "Supplier Added")
            self.clear()
            self.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= SHOW =================
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()

            self.SupplierTable.delete(*self.SupplierTable.get_children())

            for row in rows:
                self.SupplierTable.insert("", END, values=row)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= SELECT =================
    def get_data(self, ev):
        f = self.SupplierTable.focus()
        row = self.SupplierTable.item(f).get("values")

        if row:
            self.var_sup_invoice.set(row[0])
            self.var_name.set(row[1])
            self.var_contact.set(row[2])

            self.txt_desc.delete("1.0", END)
            self.txt_desc.insert(END, row[3])

    # ================= UPDATE =================
    def update(self):
        if self.var_sup_invoice.get() == "":
            messagebox.showerror("Error", "Invoice required")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("""
                UPDATE supplier SET
                name=?, contact=?, desc=?
                WHERE invoice=?
            """, (
                self.var_name.get(),
                self.var_contact.get(),
                self.txt_desc.get("1.0", END),
                self.var_sup_invoice.get()
            ))

            con.commit()
            messagebox.showinfo("Success", "Updated")
            self.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= DELETE =================
    def delete(self):
        if self.var_sup_invoice.get() == "":
            messagebox.showerror("Error", "Select Invoice")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("DELETE FROM supplier WHERE invoice=?",
                        (self.var_sup_invoice.get(),))

            con.commit()
            messagebox.showinfo("Success", "Deleted")
            self.clear()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= CLEAR =================
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.var_searchtxt.set("")
        self.txt_desc.delete("1.0", END)
        self.show()

    # ================= SEARCH =================
    def search(self):
        if self.var_searchtxt.get() == "":
            messagebox.showerror("Error", "Enter Invoice No.")
            return

        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM supplier WHERE invoice=?",
                        (self.var_searchtxt.get(),))

            row = cur.fetchone()

            self.SupplierTable.delete(*self.SupplierTable.get_children())

            if row:
                self.SupplierTable.insert("", END, values=row)
            else:
                messagebox.showerror("Error", "No record found")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()