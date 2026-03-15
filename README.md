# emi-calculator-for-finance-
🚲 Bike Finance App

A Python GUI application built with Tkinter that helps finance companies calculate bike loan EMIs, generate repayment schedules, and export customer loan reports.

The application includes user authentication, EMI calculation, penalty handling, secured loan logic, and Excel report generation.

📌 Features
🔐 User Authentication

Login system

New user registration

Forgot password recovery

Users stored in a simple text file (users.txt)

📊 EMI Calculator

Calculate monthly EMI

Supports:

Normal loans

Secured loans

Adjustable interest rates

Late EMI penalty calculation

👤 Customer Details

Stores important information:

Customer name

Profession

Salary

CIBIL score

Loan type

📅 EMI Schedule Generator

Automatically creates a month-by-month repayment schedule including:

EMI amount

Penalty for late payments

Total payable amount

Remaining balance

📄 Excel Report Export

Exports a complete loan report including:

Customer information

EMI schedule

Payment details

Report is saved as .xlsx Excel file.

🔎 CIBIL Check

Direct link to check CIBIL score from:

https://www.equifax.co.in/

🧾 Risk Analysis

Based on CIBIL score, the system determines risk level:

CIBIL Score	Risk Level
> 750	Excellent
650 – 750	Good
550 – 649	Fair
< 550	Low / Risk
🖥️ Application Screens

The app includes the following pages:

1️⃣ Splash Screen
2️⃣ Login Page
3️⃣ Register Page
4️⃣ Forgot Password Page
5️⃣ Dashboard
6️⃣ EMI Calculator
7️⃣ EMI Schedule & Report Export

🧮 EMI Calculation Logic

For Normal Loans

𝐼
𝑛
𝑡
𝑒
𝑟
𝑒
𝑠
𝑡
=
𝑃
×
𝑅
×
𝑀
12
×
100
Interest=
12×100
P×R×M
	​


Where:

P = Loan Amount

R = Interest Rate

M = Number of Months

𝐸
𝑀
𝐼
=
𝑃
+
𝐼
𝑛
𝑡
𝑒
𝑟
𝑒
𝑠
𝑡
𝑀
EMI=
M
P+Interest
	​


For Secured Loans

Interest is calculated using 1.25% per 15 day block:

blocks = ceil(days_past / 15)
interest = loan_amount * 0.0125 * blocks
⚠️ Late Payment Penalty

Penalty rules:

• First 2 missed EMIs → 5% penalty on EMI
• After that → 5% penalty on accumulated late due

🛠️ Technologies Used

Python 3

Tkinter (GUI)

Pillow (PIL) – Image support

OpenPyXL – Excel report generation

Math module

Webbrowser module

📦 Required Libraries

Install dependencies before running:

pip install pillow openpyxl
▶️ How to Run

1️⃣ Clone the repository

git clone https://github.com/yourusername/bike-finance-app.git

2️⃣ Navigate to the project folder

cd bike-finance-app

3️⃣ Run the program

python app.py
📂 Project Structure
bike-finance-app
│
├── app.py
├── users.txt
├── README.md
└── reports/
📤 Exported Report Example

The Excel report contains:

Customer Info

Field	Value
Name	Example
Profession	Engineer
Salary	50000
CIBIL	720
Loan Type	Normal

EMI Schedule

Month	EMI	Penalty	Total	Balance
🚀 Future Improvements

Possible upgrades:

Database integration (SQLite / MySQL)

Secure password hashing

Email report sending

Graphical EMI charts

Admin panel

Customer management system

Loan approval system

👩‍💻 Author

Jyotsna Tiwari

B.Tech CSE Student
Python Developer

⭐ Contributing

Pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

📜 License

This project is licensed under the MIT License.
