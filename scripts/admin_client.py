import os
from typing import Any

from dotenv import load_dotenv
from keycloak import KeycloakAdmin


load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_keycloak_admin() -> KeycloakAdmin:
    server_url = _require_env("127.0.0.1:8080/admin)
    realm_name = _require_env("master")
    username = _require_env("admin")
    password = _require_env("020102Acela!")
    verify_tls_raw = os.getenv("KEYCLOAK_VERIFY_TLS", "true").strip().lower()
    verify_tls = verify_tls_raw not in {"0", "false", "no"}

    return KeycloakAdmin(
        server_url=server_url,
        username=username,
        password=password,
        realm_name=realm_name,
        verify=verify_tls,
    )


def find_user_by_username(admin: KeycloakAdmin, username: str) -> dict[str, Any] | None:
   users = admin.get_users({"username": username})
    for user in users:
        if user.get("username") == username:
            return user
    return None


def get_user_id_by_username(admin: KeycloakAdmin, username: str) -> str:
    user = find_user_by_username(admin, username)
    if not user:
        raise ValueError(f"User not found: {username}")
    user_id = user.get("id")
    if not user_id:
        raise RuntimeError(f"User record for {username} is missing an id")
    return user_id


def get_most_recent_user(admin: KeycloakAdmin) -> dict[str, Any]:
   users = admin.get_users({})

    filtered = [
        u for u in users
        if u.get("username") and not u.get("serviceAccountClientId")
    ]
    if not filtered:
        raise RuntimeError("No eligible users found in the realm")

    def sort_key(user: dict[str, Any]) -> int:
        return int(user.get("createdTimestamp") or 0)

    return max(filtered, key=sort_key)