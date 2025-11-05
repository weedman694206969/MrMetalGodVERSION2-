from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from datetime import timedelta
import random
import mysql.connector

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "the-greatest-key-ever-made-69420"

app.permanent_session_lifetime = timedelta(minutes=10)

testing_db_credentials = {
    "host": "198.251.89.164",
    "user": "mrmetalg_test",
    "password": "ThePassword69!",
    "database": "mrmetalg_test"
}

final_db_credentials = {
    "host": "localhost", 
    "user": "mrmetalg_test", 
    "password": "ThePassword69!",
    "database": "mrmetalg_test"
}


def establish_db_connection():
     return mysql.connector.connect(
        host=testing_db_credentials["host"],
        user=testing_db_credentials["user"],
        password=testing_db_credentials["password"],
        database=testing_db_credentials["database"]
     )

def execute_sql_query(query, parameters=None, data_to_fetch=None):
    # Nothing is required to return directly from query execution, only results, so.... 
    # We're just returning result!

    acceptable_fetch_parameters = ["one", "all"]
    conn = establish_db_connection()
    cursor = conn.cursor()

    if parameters is not None:
        cursor.execute(query, parameters)
    else:
        cursor.execute(query)

    result = None
    if data_to_fetch is not None:
        if data_to_fetch == "one":
            result = cursor.fetchone()
        elif data_to_fetch == "all":
            result = cursor.fetchall()
        else:
            raise ValueError(f"{str(data_to_fetch)} is not a valid parameter for Query: {query}")
    
    conn.commit()
    cursor.close()
    conn.close()

    
    return result
        

def get_comments():
    comments = execute_sql_query(query="SELECT user, messagecontent FROM messages", data_to_fetch="all")
    return comments


@app.route('/get_comments', methods=['GET'])
def get_comments_json():
     comments = get_comments()
     return jsonify(comments)
@app.route('/add_comment', methods=['POST'])
def add_comment():
        

        user = request.form.get('user', f"Guest {random.randint(1, 10000)}")  # Default to a random guest name if not provided

        """^ The front end handles this part now, it's still generating the same random guest name, but only for that session"""

        message = request.form['message']
        execute_sql_query(query="INSERT INTO messages (user, messagecontent) VALUES (%s, %s)", parameters=(user, message))
    
        return jsonify({'status': 'success'})  # Redirect back to the home page to see the new message

@app.route("/purge_chat", methods=["POST"])
def purge_chat():
    execute_sql_query(query="DELETE from messages")
    print(f"Chat purge complete! Reloading page....")
    return redirect(url_for('home'))
    

@app.route('/')
def home():
    comments = get_comments()
    admin_logged_in = session.get('admin', False) # Check: is Admin logged in?
    return render_template('index.html', comments=comments, admin_logged_in=admin_logged_in)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/report")
def report():
    return render_template("report.html")



def is_admin_credentials(user, password):
        
    conn = establish_db_connection()
    cursor = conn.cursor()

    actual_user, actual_password = execute_sql_query(query="SELECT adminusername, adminpassword FROM admininfo", data_to_fetch="one")

    if user == actual_user and password == actual_password:
        print(f"Admin credentials valid!")
        return True 
    else:
        print(f"ERROR: Invalid admin credentials!")
        return False
    
    conn.commit()
    cursor.close()
    conn.close()
     #with establish_db_connection() as conn:
        #with conn.cursor() as cursor:
            #cursor.execute("SELECT adminusername, adminpassword FROM admininfo")
            #actual_user, actual_password = cursor.fetchone()

            #if user == actual_user and password == actual_password:
                #print(f"Valid admin credentials detected!")
                #return True
            #else:
                #return False


        

@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method == 'POST':
        username = request.form.get('username')  
        password = request.form.get('password')

        if is_admin_credentials(username, password):
            print(f"Admin login test successful!")
            session.permanent = True
            session['admin'] = True
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials", 401 #This will help us handle errors better.

        
     return  ''' <h2>Login</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    '''


@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

