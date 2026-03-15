import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import openpyxl
import os
import math
import webbrowser

USER_FILE = "users.txt"

# ---------------- USER FUNCTIONS ----------------
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                if "," in line:
                    u, p = line.strip().split(",", 1)
                    users[u] = p
    return users

def save_user(u, p):
    with open(USER_FILE, "a") as f:
        f.write(f"{u},{p}\n")

# ---------------- SPLASH ----------------
def show_splash(root, delay=1200):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    w, h = 420, 420
    sw, sh = splash.winfo_screenwidth(), splash.winfo_screenheight()
    splash.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    tk.Label(splash, text="🚲 Bike Finance", font=("Arial", 28, "bold")).pack(expand=True)
    splash.after(delay, splash.destroy)
    root.wait_window(splash)

# ---------------- MAIN APP ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bike Finance App")
        self.geometry("1000x720")
        self.schedule_data = []
        self.customer_data = {}

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginPage, RegisterPage, ForgotPage,
                  DashboardPage, CalculatorPage, SchedulePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, page):
        self.frames[page].tkraise()

# ---------------- LOGIN ----------------
class LoginPage(tk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.c = c
        tk.Label(self, text="🔐 Login", font=("Arial", 26, "bold")).pack(pady=20)

        box = tk.Frame(self)
        box.pack()
        tk.Label(box, text="Username").grid(row=0, column=0)
        self.u = ttk.Entry(box, width=30)
        self.u.grid(row=0, column=1)

        tk.Label(box, text="Password").grid(row=1, column=0)
        self.p = ttk.Entry(box, width=30, show="*")
        self.p.grid(row=1, column=1)

        ttk.Button(self, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self, text="Register", command=lambda: c.show_frame(RegisterPage)).pack()
        ttk.Button(self, text="Forgot Password", command=lambda: c.show_frame(ForgotPage)).pack(pady=5)

    def login(self):
        users = load_users()
        if self.u.get() in users and users[self.u.get()] == self.p.get():
            messagebox.showinfo("Success", "Login Successful")
            self.c.show_frame(DashboardPage)
        else:
            messagebox.showerror("Error", "Invalid Login")

# ---------------- REGISTER ----------------
class RegisterPage(tk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.c = c
        tk.Label(self, text="📝 Register", font=("Arial", 26, "bold")).pack(pady=20)

        box = tk.Frame(self)
        box.pack()
        tk.Label(box, text="Username").grid(row=0, column=0)
        self.u = ttk.Entry(box, width=30)
        self.u.grid(row=0, column=1)

        tk.Label(box, text="Password").grid(row=1, column=0)
        self.p = ttk.Entry(box, width=30, show="*")
        self.p.grid(row=1, column=1)

        ttk.Button(self, text="Create Account", command=self.register).pack(pady=10)
        ttk.Button(self, text="← Back", command=lambda: c.show_frame(LoginPage)).pack()

    def register(self):
        users = load_users()
        if not self.u.get() or not self.p.get():
            messagebox.showerror("Error", "All fields required")
            return
        if self.u.get() in users:
            messagebox.showerror("Error", "User exists")
            return
        save_user(self.u.get(), self.p.get())
        messagebox.showinfo("Success", "Account Created")
        self.c.show_frame(LoginPage)

# ---------------- FORGOT ----------------
class ForgotPage(tk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        tk.Label(self, text="🔑 Forgot Password", font=("Arial", 26, "bold")).pack(pady=20)

        box = tk.Frame(self)
        box.pack()
        tk.Label(box, text="Username").grid(row=0, column=0)
        self.u = ttk.Entry(box, width=30)
        self.u.grid(row=0, column=1)

        ttk.Button(self, text="Recover", command=self.recover).pack(pady=10)
        ttk.Button(self, text="← Back", command=lambda: c.show_frame(LoginPage)).pack()

    def recover(self):
        users = load_users()
        if self.u.get() in users:
            messagebox.showinfo("Password", f"Password: {users[self.u.get()]}")
        else:
            messagebox.showerror("Error", "User not found")

# ---------------- DASHBOARD ----------------
class DashboardPage(tk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        tk.Label(self, text="🏍️ Dashboard", font=("Arial", 26, "bold")).pack(pady=20)
        ttk.Button(self, text="EMI Calculator", command=lambda: c.show_frame(CalculatorPage)).pack(pady=8)
        ttk.Button(self, text="EMI Schedule", command=lambda: c.show_frame(SchedulePage)).pack(pady=8)
        ttk.Button(self, text="Logout", command=lambda: c.show_frame(LoginPage)).pack(pady=8)

# ---------------- CALCULATOR ----------------
class CalculatorPage(tk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.c = c

        tk.Label(self, text="📘 EMI Calculator", font=("Arial", 22, "bold")).pack(pady=10)
        f = tk.Frame(self)
        f.pack()

        # Customer Details
        tk.Label(f, text="Customer Name").grid(row=0, column=0)
        self.name = ttk.Entry(f, width=30)
        self.name.grid(row=0, column=1)

        tk.Label(f, text="Profession").grid(row=1, column=0)
        self.prof = ttk.Entry(f, width=30)
        self.prof.grid(row=1, column=1)

        tk.Label(f, text="Salary").grid(row=2, column=0)
        self.salary = ttk.Entry(f, width=30)
        self.salary.grid(row=2, column=1)

        tk.Label(f, text="CIBIL Score").grid(row=3, column=0)
        self.cibil = ttk.Entry(f, width=30)
        self.cibil.grid(row=3, column=1)

        ttk.Button(f, text="Check CIBIL",
                   command=lambda: webbrowser.open("https://www.equifax.co.in/")).grid(row=3, column=2, padx=5)

        # Loan Details
        tk.Label(f, text="Loan Amount").grid(row=4, column=0)
        self.p = ttk.Entry(f, width=25)
        self.p.grid(row=4, column=1)

        tk.Label(f, text="Months").grid(row=5, column=0)
        self.m = ttk.Entry(f, width=25)
        self.m.grid(row=5, column=1)

        tk.Label(f, text="Loan Type").grid(row=6, column=0)
        self.loan_type = ttk.Combobox(f, values=["Normal", "Secured"], state="readonly", width=23)
        self.loan_type.current(0)
        self.loan_type.grid(row=6, column=1)
        self.loan_type.bind("<<ComboboxSelected>>", self.toggle)

        tk.Label(f, text="Interest %").grid(row=7, column=0)
        self.r = ttk.Entry(f, width=25)
        self.r.insert(0, "15")
        self.r.grid(row=7, column=1)

        tk.Label(f, text="Late EMIs").grid(row=8, column=0)
        self.l = ttk.Entry(f, width=25)
        self.l.insert(0, "0")
        self.l.grid(row=8, column=1)

        tk.Label(f, text="Days Past (Secured)").grid(row=9, column=0)
        self.days = ttk.Entry(f, width=25)
        self.days.insert(0, "0")
        self.days.grid(row=9, column=1)
        self.days.config(state="disabled")

        ttk.Button(self, text="Calculate & Generate Schedule", command=self.calculate).pack(pady=10)
        ttk.Button(self, text="← Back", command=lambda: c.show_frame(DashboardPage)).pack()

    def toggle(self, e):
        if self.loan_type.get() == "Secured":
            self.r.delete(0, tk.END)
            self.r.insert(0, "1.25")
            self.r.config(state="disabled")
            self.days.config(state="normal")
        else:
            self.r.config(state="normal")
            self.r.delete(0, tk.END)
            self.r.insert(0, "15")
            self.days.delete(0, tk.END)
            self.days.insert(0, "0")
            self.days.config(state="disabled")

    def calculate(self):
        try:
            # Store customer data
            self.c.customer_data = {
                "name": self.name.get(),
                "profession": self.prof.get(),
                "salary": self.salary.get(),
                "cibil": self.cibil.get(),
                "loan_type": self.loan_type.get()
            }

            P = float(self.p.get())
            M = int(self.m.get())
            L = int(self.l.get())
            loan_type = self.loan_type.get()

            if loan_type == "Secured":
                days = int(self.days.get())
                blocks = math.ceil(days / 15)
                interest = P * 0.0125 * blocks
            else:
                R = float(self.r.get())
                interest = (P * R * M) / (12 * 100)

            emi = (P + interest) / M
            balance = P
            late_due = 0
            schedule = []

            for i in range(1, M + 1):
                penalty = 0
                if i <= L:
                    if i <= 2:
                        penalty = emi * 0.05
                        late_due += emi + penalty
                    else:
                        penalty = late_due * 0.05
                        late_due += emi + penalty
                else:
                    late_due = 0

                balance -= P / M
                schedule.append({
                    "month": i,
                    "emi": round(emi, 2),
                    "penalty": round(penalty, 2),
                    "total": round(emi + penalty, 2),
                    "balance": round(balance if balance > 0 else 0, 2)
                })

            self.c.schedule_data = schedule
            self.c.show_frame(SchedulePage)
            self.c.frames[SchedulePage].refresh()

        except:
            messagebox.showerror("Error", "Invalid Input")

# ---------------- SCHEDULE ----------------
class SchedulePage(tk.Frame):
    def __init__(self, parent, c):
        super().__init__(parent)
        self.c = c

        tk.Label(self, text="📄 EMI Schedule", font=("Arial", 22, "bold")).pack()

        cols = ("Month", "EMI", "Penalty", "Total", "Balance")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Button(self, text="Export Report", command=self.export).pack(pady=5)
        ttk.Button(self, text="← Back", command=lambda: c.show_frame(DashboardPage)).pack()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for r in self.c.schedule_data:
            self.tree.insert("", "end", values=(r["month"], r["emi"], r["penalty"], r["total"], r["balance"]))

    def export(self):
        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if not file:
            return
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Customer Loan Report"

        # Customer Info
        cust = self.c.customer_data
        ws.append(["Customer Name", cust.get("name","")])
        ws.append(["Profession", cust.get("profession","")])
        ws.append(["Salary", cust.get("salary","")])
        ws.append(["CIBIL Score", cust.get("cibil","")])
        ws.append(["Loan Type", cust.get("loan_type","")])
        ws.append([])
        ws.append(["Month", "EMI", "Penalty", "Total", "Balance"])
        for r in self.c.schedule_data:
            ws.append([r["month"], r["emi"], r["penalty"], r["total"], r["balance"]])
        wb.save(file)

        # CIBIL Risk Level
        try:
            cibil_score = int(cust.get("cibil",0))
            if cibil_score > 750:
                level = "Excellent"
            elif cibil_score >= 650:
                level = "Good"
            elif cibil_score >= 550:
                level = "Fair"
            else:
                level = "Low / Risk"
        except:
            level = "Unknown"

        messagebox.showinfo("Report Sent", f"Your CIBIL risk level is: {level}\nYour report has been sent to the company.")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app = App()
    app.withdraw()
    show_splash(app)
    app.deiconify()
    app.mainloop()
