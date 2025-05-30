from module.db import get_db_connection

def delete_invalid_tokens(invalid_tokens):
    if not invalid_tokens:
        return 0

    db = get_db_connection()
    if db:
        cursor = db.cursor()
        for bad_token in invalid_tokens:
            cursor.execute("DELETE FROM fcm_tokens WHERE token = %s", (bad_token,))
        db.commit()
        cursor.close()
        db.close()
        return len(invalid_tokens)
    return 0
