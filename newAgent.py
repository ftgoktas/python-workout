"""

Name:Furkan T Goktas
Date: 9/17/2021
Assignment:#3 Flask Website
Due Date: 9/19/2021
About this project: Developing a frontend application that interacts with a database
for a small scale real-world applications using third-party Python libraries discussed in the course.
Assumptions:The AgentName, the AgentAlias and the LoginPassword are not empty and does not only contain spaces,
the SecurityLevel is a numeric value between 1 and 10 inclusive.
All work below was performed by Furkan T Goktas

"""

from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


# default routing
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def new_student():
    return render_template('agent.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        # form fields
        try:
            nm = request.form['Name']
            als = request.form['Alias']
            slvl = request.form['SecLvl']
            pwd = request.form['Password']

            msg = ""
            isValid = True

            # Check if name is not empty and does not only contain spaces
            if len(nm) < 1 or nm.isspace():
                msg += "You cannot enter in an empty name\n"
                isValid = False

            # Check if alias is not empty and does not only contain spaces
            if len(als) < 1 or als.isspace():
                msg += "You cannot enter in an alias\n"
                isValid = False

            # Check if password is not empty and does not only contain spaces
            if len(pwd) < 1 or pwd.isspace():
                msg += "You cannot enter in an empty password\n"
                isValid = False

            # Check if the SecurityLevel is a numeric value between 1 and 10 inclusive
            if len(slvl) < 1 or slvl.isspace() or not slvl.isnumeric() or int(slvl) >= 10 or int(slvl) <= 0:
                msg += "The security level must be a numeric value between 1 and 10."
                isValid = False

            if isValid:
                try:
                    with sql.connect("AgentDB.db") as con:
                        cur = con.cursor()

                    cur.execute("INSERT INTO AGENTS (Name,Alias,SecLvl,Password) VALUES (?,?,?,?)",
                                (nm, als, slvl, pwd))
                    con.commit()
                    msg += "Record successfully added"

                except:
                    con.rollback()
                    msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("AgentDB.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from AGENTS")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
