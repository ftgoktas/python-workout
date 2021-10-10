import os

from flask import Flask, render_template, request, session, flash, jsonify
import sqlite3 as sql

app = Flask(__name__)


# default routing
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', name=session['name'])


@app.route('/enternew')
def new_agent():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin') == True:
        return render_template('agent.html')
    else:
        msg = "Page not found"
        return render_template("result.html", msg=msg)


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin') == True:
        #if request.method == 'POST':
            try:
                msg = ""
                isValid = True
                nm = request.form['Name']
                als = request.form['Alias']
                slvl = request.form['SecurityLevel']
                pwd = request.form['Password']

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
                    msg = msg + "The security level must be a numeric value between 1 and 10."
                    isValid = False

                if isValid:
                    try:
                        with sql.connect("CrapsDB.db") as con:
                            cur = con.cursor()

                        cur.execute("INSERT INTO AGENTS (AgentName,Alias,SecurityLevel,Password) VALUES (?,?,?,?)",
                                        (nm, als, slvl, pwd))
                        con.commit()
                        msg = "Record successfully added"
                    except:
                        con.rollback()
                        msg = "Error in insert operation"
            except:
                con.rollback()
                msg = "Error in insert operation"

            finally:
                return render_template("result.html", msg = msg)
                con.close()
    else:
        return render_template('login.html')


@app.route('/list')
def list():
    if not session.get('logged_in'):
        return render_template('login.html')
    elif session.get('admin') == True:
        con = sql.connect("CrapsDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from AGENTS")

        rows = cur.fetchall();
        return render_template("list.html", rows=rows)

    elif session.get('admin2') == True:
        con = sql.connect("CrapsDB.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select AgentName, Alias, SecurityLevel from AGENTS")

        rows = cur.fetchall();
        return render_template("list.html", rows=rows)
    else:
        msg = "Page not found"
        return render_template("result.html", msg=msg)


@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        nm = request.form['AgentName']
        pwd = request.form['Password']

        with sql.connect("CrapsDB.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = """select * from AGENTS where AgentName = ? and Password = ?"""
            cur.execute(sql_select_query, (nm, pwd))

            row = cur.fetchone();
            if (row != None):
                session['logged_in'] = True
                session['name'] = nm
                if int(row['SecurityLevel']) == 1:
                    session['admin'] = True
                else:
                    session['admin'] = False
                if int(row['SecurityLevel']) == 2:
                    session['admin2'] = True
                else:
                    session['admin2'] = False
                if int(row['SecurityLevel']) == 3:
                    session['admin3'] = True
                else:
                    session['admin3'] = False
            else:
                session['logged_in'] = False
                flash('invalid username and/or password!')
    except:
        con.rollback()
        flash("error in insert operation")
    finally:
        con.close()
    return home()


@app.route("/logout")
def logout():
    session['name'] = ""
    session['logged_in'] = False
    session['admin'] = False
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
