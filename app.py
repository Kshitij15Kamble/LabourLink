from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# -------------------------
# MySQL Database Connection
# -------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",              # or your created user
    password="King@2201",     # your MySQL password
    database="laborlink"
)

cursor = db.cursor()

# -------------------------
# Home Page
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# Labor Registration Page
# -------------------------
@app.route("/register-labor", methods=["GET", "POST"])
def register_labor():
    if request.method == "POST":
        full_name = request.form["full_name"]
        age = request.form["age"]
        gender = request.form["gender"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]

        sql = """
        INSERT INTO labor_register 
        (full_name, age, gender, email, phone, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (full_name, age, gender, email, phone, password)

        cursor.execute(sql, values)
        db.commit()

        return render_template("labor_register.html", success=True)

    return render_template("labor_register.html")


# -------------------------
# Search Labor Page
# -------------------------
@app.route("/search-labor", methods=["GET", "POST"])
def search_labor():
    if request.method == "POST":
        location = request.form.get("location")
        cursor.execute(
            "SELECT * FROM labor WHERE location LIKE %s",
            ("%" + location + "%",)
        )
    else:
        cursor.execute("SELECT * FROM labor")

    labors = cursor.fetchall()
    return render_template("search_labor.html", labors=labors)

# -------------------------
# Run Flask App
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
