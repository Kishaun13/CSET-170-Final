from random import random, randint

from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'password123'
connect = "mysql://root:Applepine13.!@localhost/banking"
engine = create_engine(connect, echo=True)
conn = engine.connect()


@app.route('/base')
def add():
    return render_template('base.html')


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


from flask import session as flask_session


# @app.route('/login', methods=['POST'])
# def login_post():
#     with app.app_context():
#         engine = create_engine(connect)
#         Session = sessionmaker(bind=engine)
#         session = Session()
#         conn = engine.connect()
#
#         user = session.execute(text('SELECT email, acc_type FROM USERS WHERE email = :email AND Keyword = :Keyword'),
#                                request.form).fetchone()
#         session.commit()
#         conn.commit()
#
#         if user:
#             if user.acc_type == 'Admin':
#                 admin = session.execute(text('SELECT * FROM admins WHERE email = :email'),
#                                         {'email': user.email}).fetchone()
#                 flask_session['user_id'] = admin.AdminID  # Store the admins id in the session
#                 return render_template('admin.html')
#             elif user.acc_type == 'Customer':
#                 customer = session.execute(text('SELECT * FROM customers WHERE email = :email'),
#                                            {'email': user.email}).fetchone()
#                 if customer is not None:
#                     flask_session['user_id'] = customer.CustomerID  # Store the customer's ID in the session
#                     flask_session['customer_id'] = customer.CustomerID  # Store the customer's ID in the session
#                     return render_template('homepage.html')
#                 else:
#                     invalid = "Invalid email or password"
#                     return render_template('login.html', invalid=invalid)
#         else:
#             invalid = "Invalid email or password"
#             return render_template('login.html', invalid=invalid)
@app.route('/login', methods=['POST'])
def login_post():
    with app.app_context():
        engine = create_engine(connect)
        Session = sessionmaker(bind=engine)
        session = Session()
        conn = engine.connect()

        user = session.execute(text('SELECT email, acc_type FROM USERS WHERE email = :email AND Keyword = :Keyword'),
                               request.form).fetchone()
        session.commit()
        conn.commit()

        if user:
            if user.acc_type == 'Admin':
                admin = session.execute(text('SELECT * FROM admins WHERE email = :email'),
                                        {'email': user.email}).fetchone()
                flask_session['user_id'] = admin.AdminID  # Store the admins id in the session
                return render_template('admin.html')
            elif user.acc_type == 'Customer':
                customer = session.execute(text('SELECT * FROM customers WHERE email = :email'),
                                           {'email': user.email}).fetchone()
                flask_session['user_id'] = customer.CustomerID  # Store the student's ID in the session
                flask_session['customer_id'] = customer.CustomerID  # Store the student's ID in the session
                return render_template('homepage.html')
        else:
            invalid = "Invalid email or password"
            return render_template('login.html', invalid=invalid)


@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def create_user():
    conn.execute(text(
        'INSERT INTO Users (Username, Email, full_name, acc_type, Keyword) VALUES (:username, :email, :full_name, "Customer", :Keyword)'),
        request.form)
    conn.commit()
    return render_template('Customer_create.html')


@app.route('/Customer_create', methods=['GET'])
def create_request():
    return render_template('Customer_create.html')


@app.route('/Customer_create', methods=['POST'])
def create_request_post():
    form_data = request.form.copy()
    phone_number = form_data.get('phone')
    if phone_number is not None:
        form_data['phone_number'] = form_data.pop('phone')
    conn.execute(text(
        'INSERT INTO Customers (OpenDate, SSN, Address, PhoneNumber, Email, Passwords) VALUES (CURRENT_DATE, :ssn, :address, :phone_number, :email, :passwords)'),
        form_data)
    conn.commit()
    return render_template('login.html')


@app.route('/my_account', methods=['GET'])
def my_account():
    return render_template('my_account.html')


@app.route('/admin_accounts', methods=['GET'])
def view_accounts():
    return render_template('admin_accounts.html')


@app.route('/admin_accounts', methods=['POST'])
def view_accounts_post():
    # Check if the user is logged in as admin
    if 'user_id' not in flask_session or flask_session['user_id'] != 1:
        return render_template('login.html')

    # Fetch all user accounts that are not approved
    accounts = conn.execute(text('SELECT * FROM Customers WHERE acc_status = "Pending"')).fetchall()

    return render_template('admin_accounts.html', accounts=accounts)

# @app.route('/admin_approve/<int:customer_id>', methods=['POST'])
# def approve(customer_id):
#     # Check if the user is logged in as admin
#     if 'user_id' not in flask_session or flask_session['user_id'] != 1:
#         return render_template('login.html')
#
#     # Update the account status to "Approved"
#     conn.execute(text('UPDATE Customers SET acc_status = "Approved" WHERE CustomerID = :customer_id'),
#                  {'customer_id': customer_id})
#     conn.commit()
#
#     # Generate a unique bank account number for the approved user
#     account_number = generate_account_number()
#
#     # Insert the new bank account into the BankAccounts table
#     conn.execute(text('INSERT INTO BankAccounts (AccountNumber, CustomerID) VALUES (:account_number, :customer_id)'),
#                  {'account_number': account_number, 'customer_id': customer_id})
#     conn.commit()
#
#     return redirect('/admin/accounts')


@app.route('/admin_approve/<int:customer_id>', methods=['POST'])
def approve_account(customer_id):
    # Check if the user is logged in as admin
    if 'user_id' not in flask_session or flask_session['user_id'] != 1:
        return render_template('login.html')

    # Update the account status to "Approved"
    conn.execute(text('UPDATE Customers SET acc_status = "Approved" WHERE CustomerID = :customer_id'),
                 {'customer_id': customer_id})
    conn.commit()

    # Generate a unique bank account number for the approved user
    account_number = generate_account_number()

    # Insert the new bank account into the BankAccounts table
    conn.execute(text('INSERT INTO BankAccounts (AccountNumber, CustomerID) VALUES (:account_number, :customer_id)'),
                 {'account_number': account_number, 'customer_id': customer_id})
    conn.commit()

    return redirect('/admin_accounts')


@app.route('/admin_approve/<int:customer_id>', methods=['GET'])
def approve_account_page(customer_id):
    return render_template('admin_approve.html', customer_id=customer_id)


@app.route('/add_or_send_money', methods=['GET'])
def add_or_send_money():
    return render_template('add_or_send_money.html')


@app.route('/add_or_send_money', methods=['POST'])
def add_to_balance():
    form_data = request.form.copy()
    amount = form_data.get('amount')
    if amount is not None:
        form_data['amount'] = form_data.pop('amount')
    conn.execute(text(
        'INSERT INTO BankAccounts (Balance) VALUES (:amount)'),
                 form_data)
    conn.commit()
    return render_template('homepage.html')
def generate_account_number():

    account_number = random.randint(100000, 999999)

    # Check if the generated account number already exists in the BankAccounts table
    existing_account = conn.execute(text('SELECT * FROM BankAccounts WHERE AccountNumber = :account_number'),
                                    {'account_number': account_number}).fetchone()

    # If the account number already exists, generate a new one recursively
    if existing_account:
        return generate_account_number()

    return account_number


if __name__ == '__main__':
    app.run(debug=True)
