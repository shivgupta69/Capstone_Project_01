from werkzeug.security import check_password_hash, generate_password_hash

try:
    import bcrypt
except ImportError:  # pragma: no cover - runtime environment fallback
    bcrypt = None


BCRYPT_PREFIX = "$2"


def hash_password(plain_password):
    """Hash passwords using bcrypt when available."""
    password = (plain_password or "").encode("utf-8")

    if bcrypt is not None:
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")

    return generate_password_hash(plain_password)


def verify_password(stored_hash, plain_password):
    """Verify bcrypt hashes and support legacy Werkzeug hashes."""
    stored_hash = stored_hash or ""
    plain_password = plain_password or ""

    if stored_hash.startswith(BCRYPT_PREFIX) and bcrypt is not None:
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), stored_hash.encode("utf-8")
            )
        except ValueError:
            return False

    if stored_hash.startswith(BCRYPT_PREFIX) and bcrypt is None:
        return False

    return check_password_hash(stored_hash, plain_password)
