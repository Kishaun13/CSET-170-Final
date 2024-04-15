from flask import Flask, render_template
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = 'password123'
connect = "mysql://root:Applepine13.!@localhost/banking"
engine = create_engine(connect, echo=True)
conn = engine.connect()


@app.route('/base')
def add():
    return render_template('base.html')













if __name__ == '__main__':
    app.run(debug=True)
