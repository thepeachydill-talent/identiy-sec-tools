from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os

load_dotenv()

app = Flask(__name__)
app.secret_key ="97ea37f57a24e1109390f6f3716f80b4209eb244113b393820ab0a7d73b60ac8"

oauth = OAuth(app)

keycloak = oauth.register(
    name="keycloak",
    client_id="identity-sec-lab",
    client_secret=("AdHJuZDfQN0rxQNczxWaHWZgU8UAxEnp"),
    server_metadata_url="http://localhost:8080/realms/master/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

@app.route("/")
def home():
    if "user" in session:
        return f"<pre>{session['user']}</pre>"
    return '<a href="/login">Login</a>'

@app.route("/debug/session")
def debug_session():
    return {
        "has_claims": "claims" in session,
        "claims": session.get("claims"),
        "session_keys": list(session.keys()),
    }
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