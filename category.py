from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x500+300+150")
        self.root.title("Inventory Management System | Category")
        self.root.config(bg="white")
        self.root.resizable(False, False)

        # ================= VARIABLES =================
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # ================= TITLE =================
        Label(self.root, text="Manage Product Category",
              font=("goudy old style", 25, "bold"),
              bg="#184a45", fg="white").pack(side=TOP, fill=X)

        # ================= INPUT FRAME =================
        Frame(self.root, bg="white").place(x=20, y=80, width=400, height=150)

        Label(self.root, text="Category Name",
              font=("goudy old style", 18), bg="white").place(x=30, y=100)

        Entry(self.root, textvariable=self.var_name,
              font=("goudy old style", 18),
              bg="lightyellow").place(x=30, y=140, width=250)

        Button(self.root, text="ADD", command=self.add,
               bg="#4caf50", fg="white",
               font=("goudy old style", 15)).place(x=290, y=140, width=80, height=30)

        Button(self.root, text="DELETE", command=self.delete,
               bg="red", fg="white",
               font=("goudy old style", 15)).place(x=290, y=180, width=80, height=30)

        # ================= TABLE FRAME =================
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=450, y=80, width=420, height=380)

        scroll = Scrollbar(cat_frame, orient=VERTICAL)

        self.CategoryTable = ttk.Treeview(
            cat_frame,
            columns=("cid", "name"),
            yscrollcommand=scroll.set,
            show="headings"
        )

        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=self.CategoryTable.yview)

        self.CategoryTable.heading("cid", text="ID")
        self.CategoryTable.heading("name", text="Category Name")

        self.CategoryTable.column("cid", width=80)
        self.CategoryTable.column("name", width=200)

        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================= ADD CATEGORY =================
    def add(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Category name required", parent=self.root)
                return

            cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
            row = cur.fetchone()

            if row:
                messagebox.showerror("Error", "Category already exists", parent=self.root)
            else:
                cur.execute("INSERT INTO category (name) VALUES (?)",
                            (self.var_name.get(),))
                con.commit()
                messagebox.showinfo("Success", "Category Added", parent=self.root)
                self.clear()
                self.show()

        except Exception as ex:
            messagebox.showerror("Error", str(ex))

        finally:
            con.close()

    # ================= SHOW =================
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()

            self.CategoryTable.delete(*self.CategoryTable.get_children())

            for row in rows:
                self.CategoryTable.insert("", END, values=row)

        except Exception as ex:
            messagebox.showerror("Error", str(ex))

        finally:
            con.close()

    # ================= SELECT DATA =================
    def get_data(self, ev):
        focus = self.CategoryTable.focus()
        data = self.CategoryTable.item(focus)

        row = data.get("values")
        if not row:
            return

        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    # ================= DELETE =================
    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Error", "Select category first", parent=self.root)
                return

            cur.execute("SELECT * FROM category WHERE cid=?",
                        (self.var_cat_id.get(),))
            row = cur.fetchone()

            if not row:
                messagebox.showerror("Error", "Invalid category", parent=self.root)
            else:
                confirm = messagebox.askyesno("Confirm", "Delete this category?", parent=self.root)

                if confirm:
                    cur.execute("DELETE FROM category WHERE cid=?",
                                (self.var_cat_id.get(),))
                    con.commit()
                    messagebox.showinfo("Success", "Category Deleted", parent=self.root)
                    self.clear()

        except Exception as ex:
            messagebox.showerror("Error", str(ex))

        finally:
            con.close()

    # ================= CLEAR =================
    def clear(self):
        self.var_cat_id.set("")
        self.var_name.set("")
        self.show()


# ================= RUN =================
if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()