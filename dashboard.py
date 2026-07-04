from tkinter import *
from tkinter import messagebox
import time
import sqlite3
import os

from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass


class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+110+80")
        self.root.title("Inventory Management System")
        self.root.resizable(False, False)
        self.root.config(bg="white")

        # ================= TITLE (NO IMAGE) =================
        title = Label(
            self.root,
            text="Inventory Management System",
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",
            anchor="w",
            padx=20
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        # ================= LOGOUT =================
        Button(
            self.root,
            text="Logout",
            font=("times new roman", 15, "bold"),
            bg="yellow",
            cursor="hand2",
            command=self.logout
        ).place(x=1150, y=10, height=50, width=150)

        # ================= CLOCK =================
        self.lbl_clock = Label(
            self.root,
            font=("times new roman", 15),
            bg="#4d636d",
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ================= LEFT MENU =================
        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        Label(LeftMenu, text="MENU", font=("times new roman", 20, "bold"),
              bg="#009688", fg="white").pack(side=TOP, fill=X)

        Button(LeftMenu, text="Employee", command=self.employee,
               font=("times new roman", 18, "bold"),
               bg="white", bd=2, cursor="hand2").pack(fill=X)

        Button(LeftMenu, text="Supplier", command=self.supplier,
               font=("times new roman", 18, "bold"),
               bg="white", bd=2, cursor="hand2").pack(fill=X)

        Button(LeftMenu, text="Cat egory", command=self.category,
               font=("times new roman", 18, "bold"),
               bg="white", bd=2, cursor="hand2").pack(fill=X)

        Button(LeftMenu, text="Products", command=self.product,
               font=("times new roman", 18, "bold"),
               bg="white", bd=2, cursor="hand2").pack(fill=X)

        Button(LeftMenu, text="Sales", command=self.sales,
               font=("times new roman", 18, "bold"),
               bg="white", bd=2, cursor="hand2").pack(fill=X)

        Button(LeftMenu, text="Exit", command=self.exit_app,
               font=("times new roman", 18, "bold"),
               bg="white", bd=2, cursor="hand2").pack(fill=X)

        # ================= DASHBOARD CARDS =================
        self.lbl_employee = Label(self.root, text="Total Employee\n[0]",
                                  bg="#33bbf9", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Total Supplier\n[0]",
                                  bg="#ff5722", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Total Category\n[0]",
                                  bg="#009688", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Total Product\n[0]",
                                 bg="#607d8b", fg="white",
                                 font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Total Sales\n[0]",
                               bg="#ffc107", fg="white",
                               font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # ================= FOOTER =================
        Label(self.root,
              text="IMS - Inventory Management System",
              font=("times new roman", 12),
              bg="#4d636d",
              fg="white").pack(side=BOTTOM, fill=X)

        self.update_content()

    # ================= MODULE OPEN =================
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    # ================= EXIT =================
    def exit_app(self):
        self.root.destroy()

    def logout(self):
        self.root.destroy()

    # ================= DASHBOARD UPDATE =================
    def update_content(self):
        try:
            con = sqlite3.connect("ims.db")
            cur = con.cursor()

            tables = ["product", "category", "employee", "supplier"]

            counts = []
            for t in tables:
                cur.execute(f"SELECT COUNT(*) FROM {t}")
                counts.append(cur.fetchone()[0])

            self.lbl_product.config(text=f"Total Product\n[{counts[0]}]")
            self.lbl_category.config(text=f"Total Category\n[{counts[1]}]")
            self.lbl_employee.config(text=f"Total Employee\n[{counts[2]}]")
            self.lbl_supplier.config(text=f"Total Supplier\n[{counts[3]}]")

            bill_folder = "bill"
            bill_count = len(os.listdir(bill_folder)) if os.path.exists(bill_folder) else 0
            self.lbl_sales.config(text=f"Total Sales\n[{bill_count}]")

            time_ = time.strftime("%H:%M:%S")
            date_ = time.strftime("%d-%m-%Y")

            self.lbl_clock.config(
                text=f"Inventory System\t\t Date: {date_}\t\t Time: {time_}"
            )

            self.lbl_clock.after(1000, self.update_content)

        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)


# ================= RUN =================
if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()