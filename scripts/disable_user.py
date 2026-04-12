import argparse
import sys

from keycloak.exceptions import KeycloakPutError

from keycloak_admin_client import get_keycloak_admin, get_user_id_by_username


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Disable a Keycloak user.")
    parser.add_argument("--username", required=True, help="Username to disable")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    admin = get_keycloak_admin()

    try:
        user_id = get_user_id_by_username(admin, args.username)
        admin.update_user(user_id=user_id, payload={"enabled": False})
    except (ValueError, KeycloakPutError) as exc:
        print(f"Failed to disable user '{args.username}': {exc}", file=sys.stderr)
        return 1

    print(f"Disabled user '{args.username}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())