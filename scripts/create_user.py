import argparse
import sys

from keycloak.exceptions import KeycloakPostError

from keycloak_admin_client import get_keycloak_admin, find_user_by_username


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Keycloak user. Password is required."
    )
    parser.add_argument("--username", required=True, help="Username to create")
    parser.add_argument("--password", required=True, help="Initial password")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--first-name", dest="first_name", help="First name")
    parser.add_argument("--last-name", dest="last_name", help="Last name")
    parser.add_argument(
        "--temporary-password",
        action="store_true",
        help="Require the user to change password at next login",
    )
    parser.add_argument(
        "--disabled",
        action="store_true",
        help="Create the user as disabled",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    admin = get_keycloak_admin()

    existing = find_user_by_username(admin, args.username)
    if existing:
        print(f"User already exists: {args.username}", file=sys.stderr)
        return 1

    payload = {
        "username": args.username,
        "enabled": not args.disabled,
        "emailVerified": False,
        "credentials": [
            {
                "type": "password",
                "value": args.password,
                "temporary": args.temporary_password,
            }
        ],
    }

    if args.email:
        payload["email"] = args.email
    if args.first_name:
        payload["firstName"] = args.first_name
    if args.last_name:
        payload["lastName"] = args.last_name

    try:
        user_id = admin.create_user(payload=payload, exist_ok=False)
    except KeycloakPostError as exc:
        print(f"Failed to create user: {exc}", file=sys.stderr)
        return 1

    print(f"Created user '{args.username}' with id: {user_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())