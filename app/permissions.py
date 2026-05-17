def parse_roles(role_string: str):
    return [r.strip() for r in role_string.split(",") if r.strip()]

def is_allowed(user_role: str, allowed_roles: str) -> bool:
    return user_role in parse_roles(allowed_roles)

def filter_authorized_chunks(user_role: str, chunks: list):
    return [c for c in chunks if is_allowed(user_role, c["allowed_roles"])]