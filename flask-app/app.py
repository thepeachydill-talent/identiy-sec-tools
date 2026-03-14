from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os

load_dotenv()

app = Flask(__name__)
app.secret_key ="7edd3903bad8068f3ae62e3e9f31a294d2e479817faf1d95c087b55599c30f5a"

oauth = OAuth(app)

keycloak = oauth.register(
    name="keycloak",
    client_id="identity-sec-lab",
    client_secret=("EsmGHDNspx1kx8RGjloQsw13KMgjPc8T"),
    server_metadata_url="http://localhost:8080/realms/master/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

@app.route("/")
def home():
    if "user" in session:
        return f"<pre>{session['user']}</pre>"
    return '<a href="/login">Login</a>'


@app.route("/login")
def login():
    return keycloak.authorize_redirect(
        redirect_uri=url_for("auth", _external=True)
    )


@app.route("/auth")
def auth():
    token = keycloak.authorize_access_token()
    session["user"] = token["userinfo"]
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)