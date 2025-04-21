from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_string(string_to_hash):
    return password_context.hash(string_to_hash)


def verify(password_in_db, entered_password):
    return password_context.verify(entered_password, password_in_db)
