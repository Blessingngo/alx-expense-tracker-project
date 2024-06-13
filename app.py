# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request, redirect, session 
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager


app = Flask(__name__)

app.secret_key = 'a'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'blessing'
app.config['MYSQL_PASSWORD'] = 'blessingem.01'
app.config['MYSQL_DB'] = 'bblexpense'

mysql = MySQL(app)

# setup_Flask_login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)


#HOME--PAGE
@app.route("/home")
def home():
    if 'loggedin' in session:
        return render_template("homepage.html", username=session['username'])
    return redirect('/login')

@app.route("/")
def add():
    return render_template("home.html")


#SIGN--UP--OR--REGISTER


@app.route("/signup")
def signup():
    return render_template("signup.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE username = %s', (username,))
        account = cursor.fetchone()
        #print(account)

        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
          #  cursor.execute('INSERT INTO register VALUES (NULL, % s, % s, % s)', (username, email,password))
#            cursor.execute('INSERT INTO register (id, username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            cursor.execute('INSERT INTO register (username, email, password) VALUES (%s, %s, %s)', (username, email, hashed_password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('signup.html', msg=msg)

        return render_template('signup.html', msg=msg)
        
        
        
 #LOGIN--PAGE
    
@app.route("/signin")
def signin():
    return render_template("login.html")
        
@app.route('/login', methods=['GET', 'POST'])
def loggin():
    global userid
    msg = ''
   
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
#        cursor.execute('SELECT * FROM register WHERE username = % s AND password = % s', (username,))
        cursor.execute('SELECT * FROM register WHERE username = %s', (username,))
        account = cursor.fetchone()
       # print (account)
        
        if account and check_password_hash(account[3], password):
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['username'] = account[1]
           
            return redirect('/home')
        else:
            msg = 'Incorrect username or password !'

    return render_template('login.html', msg=msg)

# ABOUT PAGE

@app.route("/about")
def about():
    return render_template("about.html")

#ADDING----DATA


@app.route("/add")
def adding():
    return render_template('add.html')


@app.route('/addexpense',methods=['GET', 'POST'])
def addexpense():

    if request.method == 'POST':
        date = request.form['date']
        expensename = request.form['expensename']
        amount = request.form['amount']
        paymode = request.form['paymode']
        category = request.form['category']
    
        cursor = mysql.connection.cursor()
        # cursor.execute('INSERT INTO expenses VALUES (NULL,  % s, % s, % s, % s, % s, % s)', (session['id'] ,date, expensename, amount, paymode, category))
        cursor.execute('INSERT INTO expenses (userid, date, expensename, amount, paymode, category) VALUES (%s, %s, %s, %s, %s, %s)', (session['id'], date, expensename, amount, paymode, category))
        mysql.connection.commit()
        print(date + " " + expensename + " " + amount + " " + paymode + " " + category)
    
    return redirect("/display")



#DISPLAY---graph 

@app.route("/display")
def display():
    print(session["username"], session['id'])
    
    cursor = mysql.connection.cursor()
    # cursor.execute('SELECT * FROM expenses WHERE userid = %s AND date ORDER BY DESC', (str(session['id']),))
    cursor.execute('SELECT * FROM expenses WHERE userid = %s ORDER BY date DESC', (str(session['id']),))
    expense = cursor.fetchall()
  
       
    return render_template('display.html' ,expense=expense)
                          



#delete---the--data

@app.route('/delete/<string:id>', methods=['POST', 'GET' ])
def delete(id):
     cursor = mysql.connection.cursor()
     cursor.execute('DELETE FROM expenses WHERE  id = %s', (id,))
     mysql.connection.commit()
     print('deleted successfully')    
     return redirect("/display")
 
    
#UPDATE---DATA

@app.route('/edit/<id>', methods=['POST', 'GET' ])
def edit(id):

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM expenses WHERE  id = %s', (id,))
    row = cursor.fetchall()
    if row:
        return render_template('edit.html', expenses=row[0])
    else:
        return "Expense not found", 404
   
#   print(row[0])
#    return render_template('edit.html', expenses = row[0])


@app.route('/update/<id>', methods=['POST'])
def update(id):

  if request.method == 'POST' :
   
      date = request.form['date']
      expensename = request.form['expensename']
      amount = request.form['amount']
      paymode = request.form['paymode']
      category = request.form['category']
    
      cursor = mysql.connection.cursor()
       
      # cursor.execute("UPDATE `expenses` SET `date` = % s , `expensename` = % s , `amount` = % s, `paymode` = % s, `category` = % s WHERE `expenses`.`id` = % s ",(date, expensename, amount, str(paymode), str(category),id))
      cursor.execute("UPDATE expenses SET date = %s, expensename = %s, amount = %s, paymode = %s, category = %s WHERE id = %s", (date, expensename, amount, paymode, category, id))
      mysql.connection.commit()
      print('successfully updated')
      return redirect("/display")
      
            
 #limit
@app.route("/limit" )
def limit():
       return redirect('/limitn')

@app.route("/limitnum" , methods=['POST' ])
def limitnum():
     if request.method == "POST":
         number= request.form['number']
         cursor = mysql.connection.cursor()
         # cursor.execute('INSERT INTO limits VALUES (NULL, % s, % s) ',(session['id'], number))
         cursor.execute('INSERT INTO limits (userid, limitss) VALUES (%s, %s)', (session['id'], number))
         mysql.connection.commit()
         return redirect('/limitn')
     
         
@app.route("/limitn") 
def limitn():
    cursor = mysql.connection.cursor()
    # cursor.execute('SELECT limitss FROM `limits` ORDER BY `limits`.`id` DESC LIMIT 1')
    cursor.execute('SELECT limitss FROM limits ORDER BY id DESC LIMIT 1')
    x = cursor.fetchone()
    s = x[0] if x else 0 # Handle the case where no limit is set
    
    
    return render_template("limit.html" , y=s)

#REPORT

@app.route("/today")
def today():
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT TIME(date)   , amount FROM expenses  WHERE userid = %s AND DATE(date) = DATE(NOW()) ',(str(session['id'])))
      texpense = cursor.fetchall()
      print(texpense)
      
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM expenses WHERE userid = % s AND DATE(date) = DATE(NOW()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
      expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
     

@app.route("/month")
def month():
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT DATE(date), SUM(amount) FROM expenses WHERE userid= %s AND MONTH(DATE(date))= MONTH(now()) GROUP BY DATE(date) ORDER BY DATE(date) ',(str(session['id'])))
      texpense = cursor.fetchall()
      print(texpense)
      
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM expenses WHERE userid = % s AND MONTH(DATE(date))= MONTH(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
      expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )
         
@app.route("/year")
def year():
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT MONTH(date), SUM(amount) FROM expenses WHERE userid= %s AND YEAR(DATE(date))= YEAR(now()) GROUP BY MONTH(date) ORDER BY MONTH(date) ',(str(session['id'])))
      texpense = cursor.fetchall()
      print(texpense)
      
      cursor = mysql.connection.cursor()
      cursor.execute('SELECT * FROM expenses WHERE userid = % s AND YEAR(DATE(date))= YEAR(now()) AND date ORDER BY `expenses`.`date` DESC',(str(session['id'])))
      expense = cursor.fetchall()
  
      total=0
      t_food=0
      t_entertainment=0
      t_business=0
      t_rent=0
      t_EMI=0
      t_other=0
 
     
      for x in expense:
          total += x[4]
          if x[6] == "food":
              t_food += x[4]
            
          elif x[6] == "entertainment":
              t_entertainment  += x[4]
        
          elif x[6] == "business":
              t_business  += x[4]
          elif x[6] == "rent":
              t_rent  += x[4]
           
          elif x[6] == "EMI":
              t_EMI  += x[4]
         
          elif x[6] == "other":
              t_other  += x[4]
            
      print(total)
        
      print(t_food)
      print(t_entertainment)
      print(t_business)
      print(t_rent)
      print(t_EMI)
      print(t_other)


     
      return render_template("today.html", texpense = texpense, expense = expense,  total = total ,
                           t_food = t_food,t_entertainment =  t_entertainment,
                           t_business = t_business,  t_rent =  t_rent, 
                           t_EMI =  t_EMI,  t_other =  t_other )

#log-out

@app.route('/logout')

def loggout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return render_template('home.html')

             

if __name__ == "__main__":
    app.run(debug=True)
