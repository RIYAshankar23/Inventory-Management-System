from tkinter import *
from tkinter import messagebox
import os


class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        self.bill_list = []
        self.var_invoice = StringVar()

        # ================= TITLE =================
        Label(self.root, text="View Customer Bills",
              font=("goudy old style", 30),
              bg="#184a45", fg="white").pack(side=TOP, fill=X, padx=10, pady=20)

        # ================= SEARCH =================
        Label(self.root, text="Invoice No.",
              font=("times new roman", 15), bg="white").place(x=50, y=100)

        Entry(self.root, textvariable=self.var_invoice,
              font=("times new roman", 15),
              bg="lightyellow").place(x=160, y=100, width=180, height=28)

        Button(self.root, text="Search", command=self.search,
               font=("times new roman", 15, "bold"),
               bg="#2196f3", fg="white").place(x=360, y=100, width=120, height=28)

        Button(self.root, text="Clear", command=self.clear,
               font=("times new roman", 15, "bold"),
               bg="lightgray").place(x=490, y=100, width=120, height=28)

        # ================= BILL LIST =================
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scroll = Scrollbar(sales_Frame, orient=VERTICAL)

        self.Sales_List = Listbox(sales_Frame,
                                  font=("goudy old style", 15),
                                  bg="white",
                                  yscrollcommand=scroll.set)

        scroll.pack(side=RIGHT, fill=Y)
        scroll.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH, expand=1)

        self.Sales_List.bind("<ButtonRelease-1>", self.get_data)

        # ================= BILL AREA =================
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        Label(bill_Frame, text="Customer Bill Area",
              font=("goudy old style", 20),
              bg="orange").pack(side=TOP, fill=X)

        scroll2 = Scrollbar(bill_Frame, orient=VERTICAL)

        self.bill_area = Text(bill_Frame,
                              bg="lightyellow",
                              yscrollcommand=scroll2.set)

        scroll2.pack(side=RIGHT, fill=Y)
        scroll2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # ================= LOAD DATA =================
        self.show()

    # ================= LOAD BILLS =================
    def show(self):
        self.bill_list.clear()
        self.Sales_List.delete(0, END)

        folder = "bill"

        if not os.path.exists(folder):
            os.makedirs(folder)

        for file in os.listdir(folder):
            if file.endswith(".txt"):
                self.Sales_List.insert(END, file)
                self.bill_list.append(file[:-4])  # remove .txt safely

    # ================= GET FROM LIST =================
    def get_data(self, ev):
        try:
            index = self.Sales_List.curselection()
            if not index:
                return

            file_name = self.Sales_List.get(index)

            self.bill_area.delete("1.0", END)

            with open(f"bill/{file_name}", "r") as fp:
                self.bill_area.insert(END, fp.read())

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= SEARCH BILL =================
    def search(self):
        invoice = self.var_invoice.get().strip()

        if invoice == "":
            messagebox.showerror("Error", "Enter Invoice No.")
            return

        # ensure string match
        if invoice in self.bill_list:
            try:
                self.bill_area.delete("1.0", END)

                with open(f"bill/{invoice}.txt", "r") as fp:
                    self.bill_area.insert(END, fp.read())

            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Invalid Invoice No.")

    # ================= CLEAR =================
    def clear(self):
        self.var_invoice.set("")
        self.bill_area.delete("1.0", END)
        self.show()


# ================= RUN =================
if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()