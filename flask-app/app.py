from flask import Flask, session, redirect, url_for, abort
from dotenv import load_dotenv
from functools import wraps
from authlib.integrations.flask_client import OAuth
import os

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "4d1885187200923621dfb9ff04dcef5ae0a9ef423bb3d98b942acfbeef7c5766"

oauth = OAuth(app)

keycloak = oauth.register(
    name="keycloak",
    client_id="identity-sec-lab",
    client_secret="4SKCOQY36xEDvzW36drIoEzIUIALlqRC",
    server_metadata_url="http://localhost:8080/realms/master/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)

def get_claims() -> dict:
    return session.get("claims", {})

def get_roles() -> set[str]:
    claims = get_claims()
    return set(claims.get("realm_access", {}).get("roles", []))

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "claims" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped_view

def roles_required(*required_roles):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if "claims" not in session:
                return redirect(url_for("login"))

            user_roles = get_roles()

            if not any(role in user_roles for role in required_roles):
                abort(403)

            return view(*args, **kwargs)
        return wrapped_view
    return decorator

@app.route("/")
def home():
    claims = session.get("claims")
    if claims:
        return f"<pre>{claims}</pre>"
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
    userinfo = token.get("userinfo") or keycloak.parse_id_token(token)
    session["claims"] = userinfo
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/developer")
@login_required
@roles_required("developer")
def developer():
    return "Developer Access Granted"

@app.route("/support")
@login_required
@roles_required("helpdesk_admin")
def support():
    return "Support Access Granted"

@app.route("/admin")
@login_required
@roles_required("security-admin")
def admin():
    return "Admin Access Granted"

@app.route("/whoami")
@login_required
def whoami():
    claims = get_claims()
    return {
        "username": claims.get("preferred_username"),
        "email": claims.get("email"),
        "roles": list(get_roles())
    }

@app.errorhandler(403)
def forbidden(_):
    return "403 Forbidden - You don't have access", 403

if __name__ == "__main__":
    app.run(debug=True)