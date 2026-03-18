
USER_ROLE_MAP = {1:"superadmin", 2:"admin", 3:"readonly"}

def get_user_role(role_id):
    if role_id not in USER_ROLE_MAP:
        raise ValueError(f"Invalid role id:{role_id}")
    return USER_ROLE_MAP[role_id]