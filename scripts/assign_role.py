import argparse
import sys
from typing import Any

from keycloak.exceptions import KeycloakGetError, KeycloakPostError

from keycloak_admin_client import (
    get_keycloak_admin,
    get_most_recent_user,
    get_user_id_by_username,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assign a realm role to a Keycloak user. "
                    "Defaults to the most recently created user if no username is provided."
    )
    parser.add_argument("--role", required=True, help="Realm role to assign")
    parser.add_argument(
        "--username",
        help="Username to assign the role to. If omitted, uses the most recently created user.",
    )
    return parser.parse_args()


def get_role_representation(admin, role_name: str) -> dict[str, Any]:
    role = admin.get_realm_role(role_name)
    if not role:
        raise ValueError(f"Realm role not found: {role_name}")
    return role


def main() -> int:
    args = parse_args()
    admin = get_keycloak_admin()

    try:
        if args.username:
            username = args.username
            user_id = get_user_id_by_username(admin, username)
        else:
            user = get_most_recent_user(admin)
            username = user["username"]
            user_id = user["id"]

        role = get_role_representation(admin, args.role)
        admin.assign_realm_roles(user_id=user_id, roles=[role])

    except (ValueError, KeycloakGetError, KeycloakPostError, RuntimeError) as exc:
        print(f"Failed to assign role: {exc}", file=sys.stderr)
        return 1

    print(f"Assigned role '{args.role}' to user '{username}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())