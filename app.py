from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key"          # เปลี่ยนก่อนใช้งานจริง
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ridebox.db"
db = SQLAlchemy(app)


# ---------- Database models ----------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    capacity_wh = db.Column(db.Integer)        # ความจุแบตเตอรี่ (Wh)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(200), default="picture/product.png")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)   # ตัวอย่างเท่านั้น: งานจริงต้องเข้ารหัส (hash)


def seed_data():
    """ใส่ข้อมูลตัวอย่างครั้งแรก ถ้าฐานข้อมูลยังว่าง"""
    if Product.query.count() == 0:
        db.session.add_all([
            Product(name="Ridebox Mini", description="ชุดกักเก็บพลังงานจากการปั่นจักรยาน สำหรับห้องพักหรือหอพัก",
                    capacity_wh=500, price=12900),
            Product(name="Ridebox Home", description="สำหรับบ้าน ใช้แบตเตอรี่ LiFePO4 ปลอดภัย ติดตั้งง่าย",
                    capacity_wh=1500, price=29900),
            Product(name="Ridebox Pro", description="สำหรับธุรกิจขนาดเล็ก ขยายความจุเพิ่มได้",
                    capacity_wh=3000, price=54900),
        ])
    if User.query.count() == 0:
        db.session.add(User(username="admin", password="admin123"))
    db.session.commit()


# ---------- Routes ----------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/product")
def product():
    products = Product.query.all()
    return render_template("product.html", products=products)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username"),
            password=request.form.get("password"),
        ).first()
        if user:
            session["user"] = user.username
            return redirect(url_for("dashboard"))
        flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    products = Product.query.all()
    return render_template("dashboard.html", products=products)


@app.route("/dashboard/add", methods=["POST"])
def add_product():
    if "user" not in session:
        return redirect(url_for("login"))
    db.session.add(Product(
        name=request.form["name"],
        description=request.form.get("description", ""),
        capacity_wh=int(request.form.get("capacity_wh") or 0),
        price=int(request.form["price"]),
    ))
    db.session.commit()
    flash("เพิ่มสินค้าแล้ว")
    return redirect(url_for("dashboard"))


@app.route("/dashboard/delete/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    if "user" not in session:
        return redirect(url_for("login"))
    item = db.session.get(Product, product_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("ลบสินค้าแล้ว")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host="0.0.0.0", port=5000, debug=True)
