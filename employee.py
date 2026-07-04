from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Employee")
        self.root.config(bg="white")
        self.root.focus_force()

        # ================= VARIABLES =================
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        # ================= SEARCH =================
        SearchFrame = LabelFrame(self.root, text="Search Employee",
                                 font=("goudy old style", 12, "bold"),
                                 bg="white")
        SearchFrame.place(x=250, y=20, width=600, height=70)

        cmb_search = ttk.Combobox(SearchFrame,
                                  textvariable=self.var_searchby,
                                  values=("Email", "Name", "Contact"),
                                  state='readonly')
        cmb_search.place(x=10, y=10, width=180)

        Entry(SearchFrame, textvariable=self.var_searchtxt,
              bg="lightyellow").place(x=200, y=10, width=180)

        Button(SearchFrame, text="Search", command=self.search,
               bg="#4caf50", fg="white").place(x=410, y=9, width=150, height=30)

        # ================= FORM =================
        Label(self.root, text="Emp ID").place(x=50, y=150)
        Entry(self.root, textvariable=self.var_emp_id, bg="lightyellow").place(x=150, y=150, width=180)

        Label(self.root, text="Name").place(x=50, y=190)
        Entry(self.root, textvariable=self.var_name, bg="lightyellow").place(x=150, y=190, width=180)

        Label(self.root, text="Email").place(x=50, y=230)
        Entry(self.root, textvariable=self.var_email, bg="lightyellow").place(x=150, y=230, width=180)

        Label(self.root, text="Gender").place(x=350, y=150)
        ttk.Combobox(self.root, textvariable=self.var_gender,
                     values=("Male", "Female", "Other"),
                     state='readonly').place(x=450, y=150, width=150)

        Label(self.root, text="Contact").place(x=350, y=190)
        Entry(self.root, textvariable=self.var_contact, bg="lightyellow").place(x=450, y=190, width=150)

        Label(self.root, text="Password").place(x=350, y=230)
        Entry(self.root, textvariable=self.var_pass, bg="lightyellow").place(x=450, y=230, width=150)

        Label(self.root, text="User Type").place(x=650, y=150)
        ttk.Combobox(self.root, textvariable=self.var_utype,
                     values=("Admin", "Employee"),
                     state='readonly').place(x=750, y=150, width=150)

        Label(self.root, text="Salary").place(x=650, y=190)
        Entry(self.root, textvariable=self.var_salary, bg="lightyellow").place(x=750, y=190, width=150)

        Label(self.root, text="DOB").place(x=650, y=230)
        Entry(self.root, textvariable=self.var_dob, bg="lightyellow").place(x=750, y=230, width=150)

        # ================= BUTTONS =================
        Button(self.root, text="Save", command=self.add, bg="blue", fg="white").place(x=400, y=300, width=100)
        Button(self.root, text="Update", command=self.update, bg="green", fg="white").place(x=510, y=300, width=100)
        Button(self.root, text="Delete", command=self.delete, bg="red", fg="white").place(x=620, y=300, width=100)
        Button(self.root, text="Clear", command=self.clear, bg="gray", fg="white").place(x=730, y=300, width=100)

        # ================= TABLE =================
        self.emp_table = ttk.Treeview(self.root,
                                      columns=("id", "name", "email", "gender", "contact", "dob", "pass", "utype", "salary"),
                                      show="headings")

        for col in self.emp_table["columns"]:
            self.emp_table.heading(col, text=col)

        self.emp_table.place(x=0, y=350, relwidth=1, height=150)
        self.emp_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # ================= DATABASE =================
    def add(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID required")
                return

            cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
            row = cur.fetchone()

            if row:
                messagebox.showerror("Error", "Employee already exists")
            else:
                cur.execute("""INSERT INTO employee 
                (eid,name,email,gender,contact,dob,password,utype,salary)
                VALUES (?,?,?,?,?,?,?,?,?)""",
                            (
                                self.var_emp_id.get(),
                                self.var_name.get(),
                                self.var_email.get(),
                                self.var_gender.get(),
                                self.var_contact.get(),
                                self.var_dob.get(),
                                self.var_pass.get(),
                                self.var_utype.get(),
                                self.var_salary.get()
                            ))

                con.commit()
                messagebox.showinfo("Success", "Employee Added")
                self.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        cur.execute("SELECT eid,name,email,gender,contact,dob,password,utype,salary FROM employee")
        rows = cur.fetchall()

        self.emp_table.delete(*self.emp_table.get_children())

        for row in rows:
            self.emp_table.insert("", END, values=row)

    def get_data(self, ev):
        row = self.emp_table.item(self.emp_table.focus())["values"]

        self.var_emp_id.set(row[0])
        self.var_name.set(row[1])
        self.var_email.set(row[2])
        self.var_gender.set(row[3])
        self.var_contact.set(row[4])
        self.var_dob.set(row[5])
        self.var_pass.set(row[6])
        self.var_utype.set(row[7])
        self.var_salary.set(row[8])

    def update(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        cur.execute("""UPDATE employee SET
        name=?, email=?, gender=?, contact=?, dob=?, password=?, utype=?, salary=?
        WHERE eid=?""",
                    (
                        self.var_name.get(),
                        self.var_email.get(),
                        self.var_gender.get(),
                        self.var_contact.get(),
                        self.var_dob.get(),
                        self.var_pass.get(),
                        self.var_utype.get(),
                        self.var_salary.get(),
                        self.var_emp_id.get()
                    ))

        con.commit()
        messagebox.showinfo("Updated", "Employee Updated")
        self.show()

    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        cur.execute("DELETE FROM employee WHERE eid=?", (self.var_emp_id.get(),))
        con.commit()

        messagebox.showinfo("Deleted", "Employee Deleted")
        self.show()

    def clear(self):
        self.var_emp_id.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("")
        self.var_contact.set("")
        self.var_dob.set("")
        self.var_pass.set("")
        self.var_utype.set("")
        self.var_salary.set("")

    def search(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        query = f"SELECT * FROM employee WHERE {self.var_searchby.get()} LIKE ?"
        cur.execute(query, ('%' + self.var_searchtxt.get() + '%',))

        rows = cur.fetchall()

        self.emp_table.delete(*self.emp_table.get_children())

        for row in rows:
            self.emp_table.insert("", END, values=row)


if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()