from flask import Flask, render_template, request
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
                flask_session['user_id'] = customer.AccountID  # Store the student's ID in the session
                flask_session['customer_id'] = customer.AccountID  # Store the student's ID in the session
                return render_template('homepage.html')
        else:
            invalid = "Invalid email or password"
            return render_template('login.html', invalid=invalid)

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def create_user():
    conn.execute(text('INSERT INTO Users (Email, full_name, acc_type, Keyword) VALUES (:email, :full_name, "Customer", :Keyword)'), request.form)
    conn.commit()
    return render_template('register.html')


@app.route('/Customer_create', methods=['GET'])
def create_request():
    return render_template('Customer_create.html')


@app.route('/Customer_create', methods=['POST'])
def create_customer():
    conn.execute(text('INSERT INTO Customers (AccountNumber, CustomerID, SSN, Address, PhoneNumber, Email, Passwords, debit_cardnumber, Card_Pin, Expire_Date) VALUES (:AccountNumber, :CustomerID, :SSN, :Address, :PhoneNumber, :Email, :Passwords, :debit_cardnumber, :Card_Pin, :Expire_Date)'), request.form)
    conn.commit()
    return render_template('Customer_create.html')


if __name__ == '__main__':
    app.run(debug=True)
