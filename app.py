from flask import *
import os
import sqlite3
from datetime import datetime
import pandas as pd
from flask import send_file
from io import BytesIO
from xhtml2pdf import pisa
from flask import render_template_string
import calendar
from datetime import datetime


from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key="harsh1"
app.config['UPLOAD_FOLDER'] = "c:/Users/Victus/OneDrive/Desktop/SOCIETY PORTAL/static/images"



# ======================LOGIN PAGE=====================#
@app.route("/")
def index():
    return render_template("index.html")


# ======================LOGIN CHECK=====================#
@app.route("/logincheck",methods=["POST","GET"])
def logincheck():
   if request.method=="POST":
        em=request.form["email"]
        ps=request.form["password"]

        
        con=sqlite3.connect("portal.db")
        c=con.cursor()

        c.execute("SELECT * FROM login WHERE email = ? and password=? ", (em,ps))
        data=c.fetchall()
       


        if len(data)==1:
            session["username"]=em    #session start
            return render_template("dashboard.html")

        else:
            return "<script>alert('Invalid email or password'); window.location.href='/';</script>"

    
# ======================DASHBOARD=====================#


@app.route("/dashboard")
def dashboard():
    if session.get("username") is not None:
     return render_template("dashboard.html")
    else:
         return  redirect(url_for("index"))


# ======================LOGOUT=====================#


@app.route("/logout")
def logout():
    session.pop("username",None)
    return render_template("index.html")


# ======================PROFILE-UPDATE=====================#


@app.route("/profile")
def profileupdate():
        con=sqlite3.connect("portal.db")
        c=con.cursor()

        c.execute("SELECT * FROM profile ")
        data=c.fetchall()
        return render_template("profile.html",data=data)


@app.route("/profileupdate/<int:id>")
def updated(id):
        con=sqlite3.connect("portal.db")
        c=con.cursor()
        c.execute("SELECT * FROM profile where id=?",[id])
        data=c.fetchall()
        return render_template("updateprofile.html",data=data)



@app.route("/profilesave",methods=["POST"])
def profileupdated():
    if request.method=="POST":
        
        fn=request.form["fullname"]
        em=request.form["email"]
        ps=request.form["firstname"]
        cn=request.form["lastname"]
        ad=request.form["contact"]
        Id=request.form["id"]
         

        con=sqlite3.connect("portal.db")
        c=con.cursor()
        c.execute("UPDATE profile   SET fullname =? , email =?, firstname=?,lastname=?,contact=? where id=?",(fn,em,ps,cn,ad,Id))
        c.execute("UPDATE login SET email = ? WHERE id = ?", (em, Id))
        con.commit()
        return redirect(url_for("index"))
   




# ======================RESET-PASSWORD=====================#

@app.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():
    con = sqlite3.connect("portal.db")
    c = con.cursor()

    # Fetch all emails from the login table
    c.execute("SELECT email FROM login")
    emails = [row[0] for row in c.fetchall()]

    if request.method == "POST":
        email = request.form.get("email")
        new_password = request.form.get("newpassword")
        confirm_password = request.form.get("confirmPassword")

        if new_password != confirm_password:
            return "<script>alert('Passwords do not match.'); window.location.href='/resetpassword';</script>"

        c.execute("SELECT * FROM login WHERE email = ?", (email,))
        if not c.fetchone():
            return "<script>alert('Email not found.'); window.location.href='/resetpassword';</script>"

        c.execute("UPDATE login SET password = ? WHERE email = ?", (new_password, email))
        con.commit()
        con.close()

        return "<script>alert('Password updated successfully.'); window.location.href='/';</script>"

    con.close()
    return render_template("resetpassword.html", emails=emails)


   
# ======================ADD-NEW-ENTRY=====================#


@app.route("/newentry", methods=["GET", "POST"])
def newentry():
    if request.method == "POST":
        name = request.form["name"]
        flat_no = request.form["flatNo"]
        contact = request.form["contact"]
        email = request.form["email"]
        member_type = request.form["memberType"]
        photo = request.files["photo"]

        photo_filename = ""
        if photo:
            photo_filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        con = sqlite3.connect("portal.db")
        c = con.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                flat_no TEXT,
                contact TEXT,
                email TEXT,
                member_type TEXT,
                photo TEXT
            )
        """)
        c.execute("INSERT INTO entries (name, flat_no, contact, email, member_type, photo) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, flat_no, contact, email, member_type, photo_filename))
        con.commit()
        con.close()

        return redirect(url_for("viewentry"))

    return render_template("newentry.html")

   
# ======================VIEW-ENTRY=====================#

@app.route("/viewentry")
def viewentry():
    con = sqlite3.connect("portal.db")
    c = con.cursor()
    c.execute("SELECT * FROM entries")
    data = c.fetchall()
    con.close()
    return render_template("Viewentry.html", entries=data)


@app.route("/delete/<int:id>")
def delete_entry(id):
    con = sqlite3.connect("portal.db")
    c = con.cursor()
    c.execute("DELETE FROM entries WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("viewentry"))


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_entry(id):
    con = sqlite3.connect("portal.db")
    c = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        flat_no = request.form["flatNo"]
        contact = request.form["contact"]
        email = request.form["email"]
        member_type = request.form["memberType"]
        
        c.execute("UPDATE entries SET name=?, flat_no=?, contact=?, email=?, member_type=? WHERE id=?",
                  (name, flat_no, contact, email, member_type, id))
        con.commit()
        con.close()
        return redirect(url_for("viewentry"))

    c.execute("SELECT * FROM entries WHERE id=?", (id,))
    data = c.fetchone()
    con.close()
    return render_template("updateentry.html", entry=data)



# ======================MAINTAINCENCE=====================#


@app.route("/maintenence", methods=["GET", "POST"])
def maintainence():
    con = sqlite3.connect("portal.db")
    c = con.cursor()

    if request.method == "POST":
        flat = request.form["flat"]
        name = request.form["name"]
        month = request.form["month"]
        status = request.form["status"]
        amount=request.form['amount'] 
        # date = datetime.now().strftime("%Y-%m-%d")

        c.execute("SELECT * FROM maintainence WHERE flat=? AND month=? AND status='Paid'", (flat, month))
        if c.fetchone():
            flash("This flat has already paid for this month!", "danger")
        else:
            c.execute("INSERT INTO maintainence (flat, name, month, status,amount) VALUES (?, ?, ?,?,?)",
                      (flat, name, month, status,amount))
            con.commit()
            flash("Maintenance entry added successfully!", "success")

    # ✅ Fetch members for dropdown
    c.execute("SELECT flat_no, name FROM entries")
    members = c.fetchall()

    c.execute("SELECT * FROM maintainence")
    data = c.fetchall()
    con.close()
    return render_template("maintainence.html", data=data, members=members)



@app.route("/update", methods=["POST"])
def update():
    id = request.form["id"]
    status = request.form["status"]
    amount = request.form["amount"]

    con = sqlite3.connect("portal.db")
    c = con.cursor()
    date = datetime.now().strftime("%Y-%m-%d")

    c.execute("UPDATE maintainence SET status=?, amount=?, date=? WHERE id=?", (status, amount, date, id))

    con.commit()
    con.close()
    return redirect(url_for("maintainence"))



@app.route("/deletemaintainence/<int:id>")
def deleterecord(id):
    con=sqlite3.connect("portal.db")
    c=con.cursor()
    c.execute("delete from maintainence where id=?",[id])
    con.commit()
    con.close()
    return redirect(url_for("maintainence"))


# ======================EXPENSES=====================#



@app.route("/expenses")
def expenses():   
    con = sqlite3.connect("portal.db")
    c = con.cursor()

    c.execute("SELECT * FROM expenses")
    records = c.fetchall()

    # Calculate totals
    c.execute("SELECT SUM(amount) FROM expenses")
    total = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM expenses WHERE status='Paid'")
    paid = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM expenses WHERE status='Pending'")
    pending = c.fetchone()[0] or 0

    con.close()

    return render_template("expenses.html", records=records, total=total, paid=paid, pending=pending)




@app.route("/add", methods=["POST"])
def add_expense():
    category = request.form["category"]
    amount = int(request.form["amount"])
    date = request.form["date"]
    status = request.form["status"]

    con = sqlite3.connect("portal.db")
    c = con.cursor()
    c.execute("INSERT INTO expenses (category, amount, date, status) VALUES (?, ?, ?, ?)",
                   (category, amount, date, status))
    con.commit()
    con.close()

    return redirect(url_for("expenses"))




@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    conn = sqlite3.connect("portal.db")
    cursor = conn.cursor()

    if request.method == "POST":
        category = request.form["category"]
        amount = request.form["amount"]
        date = request.form["date"]
        status = request.form["status"]

        cursor.execute("UPDATE expenses SET category=?, amount=?, date=?, status=? WHERE id=?",
                       (category, amount, date, status, id))
        conn.commit()
        conn.close()
        return redirect(url_for("expenses"))


    cursor.execute("SELECT * FROM expenses WHERE id=?", (id,))
    expense = cursor.fetchone()
    conn.close()

    return render_template("edit_expense.html", expense=expense)




# ======================SEARCH-DETAILS=====================#



@app.route('/search')
def search():
    flat = request.args.get('flat')
    con = sqlite3.connect('portal.db')
    c = con.cursor()

    c.execute("SELECT * FROM entries WHERE flat_no = ?", (flat,))
    results = c.fetchall()
    con.close()

    return render_template('search.html', results=results, flat=flat)


# ======================REPORTS=====================#






def get_date_range(from_month_str, to_month_str):
    # Parse inputs like "2025-01"
    from_year, from_month_num = map(int, from_month_str.split("-"))
    to_year, to_month_num = map(int, to_month_str.split("-"))

    # Start date: first of from_month
    start_date = f"{from_year}-{from_month_num:02d}-01"

    # End date: last day of to_month
    end_day = calendar.monthrange(to_year, to_month_num)[1]
    end_date = f"{to_year}-{to_month_num:02d}-{end_day}"

    return start_date, end_date



@app.route('/reports', methods=["POST", "GET"])
def reports():
    records = []
    total_members = paid_this_month = pending_payments = total_collected = 0

    if request.method == "POST":
        from_month = request.form['fromMonth']
        to_month = request.form['toMonth']

        con = sqlite3.connect('portal.db')
        c = con.cursor()

        from_month = request.form['fromMonth']   # e.g., "2025-01"
        to_month = request.form['toMonth']       # e.g., "2025-06"

        start_date, end_date = get_date_range(from_month, to_month)

        c.execute("""
                    SELECT flat AS item, name AS category, month, amount, status, date, 'Maintenance' AS type
                    FROM maintainence
                    WHERE month BETWEEN ? AND ?
                    UNION ALL
                    SELECT category AS item, '-' AS category,
                        strftime('%m', date) AS month,
                        amount, status, date, 'Expenses' AS type
                    FROM expenses
                    WHERE date BETWEEN ? AND ?
                    ORDER BY date DESC
                """, (from_month, to_month, start_date, end_date))

        records = c.fetchall()

        # Summary calculations
        c.execute("SELECT COUNT(DISTINCT flat) FROM maintainence")
        total_members = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM maintainence WHERE month = ? AND status = 'Paid'", (to_month,))
        paid_this_month = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM maintainence WHERE month = ? AND status = 'Pending'", (to_month,))
        pending_payments = c.fetchone()[0]

        c.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM (
            SELECT amount FROM maintainence WHERE month BETWEEN ? AND ?
            UNION ALL
            SELECT amount FROM expenses
            WHERE 
                CASE strftime('%m', date)
                    WHEN '01' THEN 'Jan'
                    WHEN '02' THEN 'Feb'
                    WHEN '03' THEN 'Mar'
                    WHEN '04' THEN 'Apr'
                    WHEN '05' THEN 'May'
                    WHEN '06' THEN 'Jun'
                    WHEN '07' THEN 'Jul'
                    WHEN '08' THEN 'Aug'
                    WHEN '09' THEN 'Sep'
                    WHEN '10' THEN 'Oct'
                    WHEN '11' THEN 'Nov'
                    WHEN '12' THEN 'Dec'
                END BETWEEN ? AND ?
        )
        """, (from_month, to_month, from_month, to_month))
        total_collected = c.fetchone()[0]

        con.close()

    return render_template("report.html", records=records,
                           total_members=total_members,
                           paid_this_month=paid_this_month,
                           pending_payments=pending_payments,
                           total_collected=total_collected)

      
     

@app.route("/download_excel")
def download_excel():
    from_month = request.args.get("fromMonth", "2025-01")
    to_month = request.args.get("toMonth", "2025-12")

    start_date, end_date = get_date_range(from_month, to_month)

    con = sqlite3.connect("portal.db")
    c = con.cursor()

    query = """
    SELECT flat AS item, name AS category, month, amount, status, date, 'Maintenance' AS type
    FROM maintainence
    WHERE month BETWEEN ? AND ?
    UNION ALL
    SELECT category AS item, '-' AS category,
           strftime('%m', date) AS month,
           amount, status, date, 'Expenses' AS type
    FROM expenses
    WHERE date BETWEEN ? AND ?
    ORDER BY date DESC
    """
    c.execute(query, (from_month, to_month, start_date, end_date))
    data = c.fetchall()
    con.close()

    columns = ["Item", "Category", "Month", "Amount", "Status", "Date", "Type"]
    df = pd.DataFrame(data, columns=columns)
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)

    return send_file(output, download_name="Society_Report.xlsx", as_attachment=True)



@app.route("/download_pdf")
def download_pdf():
    from_month = request.args.get("fromMonth", "2025-01")
    to_month = request.args.get("toMonth", "2025-12")

    start_date, end_date = get_date_range(from_month, to_month)

    con = sqlite3.connect("portal.db")
    c = con.cursor()

    query = """
    SELECT flat AS item, name AS category, month, amount, status, date, 'Maintenance' AS type
    FROM maintainence
    WHERE month BETWEEN ? AND ?
    UNION ALL
    SELECT category AS item, '-' AS category,
           strftime('%m', date) AS month,
           amount, status, date, 'Expenses' AS type
    FROM expenses
    WHERE date BETWEEN ? AND ?
    ORDER BY date DESC
    """
    c.execute(query, (from_month, to_month, start_date, end_date))
    data = c.fetchall()
    con.close()

    columns = ["Item", "Category", "Month", "Amount", "Status", "Date", "Type"]

    html = render_template_string("""
    <html>
    <head>
    <style>
    table {width: 100%; border-collapse: collapse;}
    th, td {border: 1px solid black; padding: 5px; text-align: left;}
    </style>
    </head>
    <body>
    <h2>Society Report ({{ from_month }} to {{ to_month }})</h2>
    <table>
      <tr>
        {% for col in columns %}
          <th>{{ col }}</th>
        {% endfor %}
      </tr>
      {% for row in data %}
      <tr>
        {% for item in row %}
          <td>{{ item }}</td>
        {% endfor %}
      </tr>
      {% endfor %}
    </table>
    </body>
    </html>
    """, data=data, columns=columns, from_month=from_month, to_month=to_month)

    pdf = BytesIO()
    pisa.CreatePDF(html, dest=pdf)
    pdf.seek(0)

    return send_file(pdf, download_name="Society_Report.pdf", as_attachment=True)









    



if __name__=="__main__":
    app.run(debug=True)