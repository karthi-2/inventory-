from __future__ import print_function
from flask import Flask, render_template, url_for, request, redirect, session
import sqlite3 as sql
import re
import ibm_db
conn =ibm_db.connect("DATABASE=bludb;HOSTNAME=21fecfd8-47b7-4937-840d-d791d0218660.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31864;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=jpy41264;PWD=dcC5L2PYRESPxhxh",'','')

app=Flask(__name__)
app.secret_key ='shreesathyam'
info=[]
@app.route('/')
def signin():
    return render_template('signin.html')
@app.route('/retailers')
def retailers():
    if request.method=="GET":
        query='''select *from register'''
        exec_query=ibm_db.exec_immediate(conn,query)
        row=ibm_db.fetch_both(exec_query)
        l=1
        while(row):
            print(row[0])
            info.append([l,row[0],row[2],row[3]])
            row=ibm_db.fetch_both(exec_query)
            l+=1
    print(info)
    return render_template('retailers.html',info=info)
@app.route('/products')
def product():
    return render_template('products.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/low-stock')
def lowStock():
    return render_template('low-stock.html')





'''@app.route('/user/<id>')
def user_info(id):
    with sql.connect('inventorymanagement.db') as con:
        con.row_factory=sql.Row
        cur =con.cursor()
        cur.execute(f'SELECT * FROM register WHERE email="{id}"')
        user = cur.fetchall()
    return render_template("user_info.html", user=user[0])'''

@app.route('/indexx',methods =['GET', 'POST'])
def indexx():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        un = request.form['email']
        pd = request.form['pw']
        sql = "SELECT * FROM register WHERE email =? AND pw=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,un)
        ibm_db.bind_param(stmt,2,pd)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account['EMAIL']
            userid=  account['EMAIL']
            session['email'] = account['EMAIL']
            msg = 'Logged in successfully !'
            return render_template('index.html')
        else:
            msg += '  Incorrect username or password !'
    return render_template('signin.html',msg=msg)

@app.route('/accessbackend', methods=['POST','GET'])
def accessbackend():
    msg=''
    if request.method == "POST":
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        email=request.form['email']
        pno=request.form['pno']
        pw=request.form['password']
        sql='SELECT * FROM register WHERE email =?'
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        acnt=ibm_db.fetch_assoc(stmt)
        print(acnt)
            
        if acnt:
            msg='Account already exits!!'
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg='Please enter the avalid email address'
        else:
            insert_sql='INSERT INTO register VALUES (?,?,?,?,?)'
            pstmt=ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(pstmt,1,firstname)
            ibm_db.bind_param(pstmt,2,lastname)
            ibm_db.bind_param(pstmt,3,email)
            ibm_db.bind_param(pstmt,4,pno)
            ibm_db.bind_param(pstmt,5,pw)
            ibm_db.execute(pstmt)
            info.append([len(info)+1,firstname,email,pno])
            msg='You have successfully registered click signin!!'
            return render_template("retailers.html",info=info)         
    elif request.method == 'POST':
        msg="fill out the form first!"
    return render_template("retailers.html",info=info)  
 

if __name__ == '__main__':
    app.run(debug=True)