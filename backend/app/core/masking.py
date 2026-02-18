def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return email
    try:
        user_part, domain_part = email.split("@")
        if len(user_part) > 3:
            return f"{user_part[:2]}***{user_part[-1]}@{domain_part}"
        elif len(user_part) > 0:
            return f"{user_part[0]}***@{domain_part}"
        else:
            return f"***@{domain_part}"
    except Exception:
        return "****"

def mask_phone(phone: str) -> str:
    if not phone or len(phone) < 5:
        return "****"
    return f"{phone[:3]}***{phone[-4:]}"

def mask_national_id(nid: str) -> str:
    # Assuming format 784-1234-5678901-1
    if not nid or len(nid) < 15:
        return "***********"
    return f"{nid[:4]}*******{nid[-1]}"
