from flask import Flask,render_template,url_for,redirect,request,flash,make_response,session
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail,Message
from email_validator import validate_email,EmailNotValidError
import logging
import os

app = Flask(__name__)

#SECRET_KEY追加
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
#ログレベルを設定する
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)

#Mailクラスのコンフィグ
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

def send_email(to, subject, template, **kwargs):
        msg = Message(subject, recipients = [to])
        msg.body = render_template(template + ".txt", **kwargs)
        msg.html = render_template(template + ".html", **kwargs)
        mail.send(msg)

@app.route("/")
def index():
    return "hello, Flask"

@app.route("/hello/<name>", methods=["GET","POST"], endpoint="hello-endpoint")
def hello(name):
    return f"hello, {name}"

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name = name)

@app.route("/contact")
def contact():
    response = make_response(render_template("contact.html"))
    #クッキーを設定する
    response.set_cookie("flask_tutorial key", "flask_tutorial value")
    #セッションを設定する
    session["username"] = "ichiro"
    
    return response

@app.route("/contact/complete", methods=["GET","POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("ユーザ名は必須です")
            is_valid = False
    
        if not email:
            flash("メールアドレスは必須です")
            is_valid = False
        
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスを正しい形式で表示してください")
            is_valid = False
        

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False
        
        if not is_valid:
            return redirect(url_for("contact"))
        
        #メールを送る
        send_email(
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username = username,
            description = description,
        )

        #リダイレクト
        flash("問い合わせありがとうございました")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")