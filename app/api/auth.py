from fastapi import APIRouter, Form
from app.database.connection import get_connection
import hashlib
import secrets

router = APIRouter()

# In-memory reset token store { token: email }
# For production use Redis/DB; fine for this app
_reset_tokens: dict = {}


# ---------- helper ----------

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


# ---------- /login ----------

@router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM doctors WHERE email = %s AND password = %s",
            (email, hash_password(password))
        )
        doctor = cursor.fetchone()
        cursor.close()
        conn.close()

        if doctor:
            return {
                "success": True,
                "message": "Login successful",
                "id": doctor["id"],
                "name": doctor["name"],
                "email": doctor["email"]
            }
        return {"success": False, "message": "Invalid email or password"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /signup ----------

@router.post("/signup")
async def signup(
    name: str = Form(...),
    license: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM doctors WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return {"success": False, "message": "Email already registered"}

        cursor.execute(
            "INSERT INTO doctors (name, license, email, password) VALUES (%s, %s, %s, %s)",
            (name, license, email, hash_password(password))
        )
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return {"success": True, "message": "Account created successfully", "id": new_id}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /fetch_profile ----------

@router.post("/fetch_profile")
async def fetch_profile(id: int = Form(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, email, phone, clinic, license FROM doctors WHERE id = %s",
            (id,)
        )
        doctor = cursor.fetchone()
        cursor.close()
        conn.close()
        if doctor:
            return {"success": True, "data": doctor}
        return {"success": False, "message": "Doctor not found"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /update_profile ----------

@router.post("/update_profile")
async def update_profile(
    id: int = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    clinic: str = Form("")
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE doctors SET name=%s, email=%s, phone=%s, clinic=%s WHERE id=%s",
            (name, email, phone, clinic, id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Profile updated"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /add_credential ----------

@router.post("/add_credential")
async def add_credential(
    doctor_id: int = Form(...),
    credential_type: str = Form(...),
    credential_number: str = Form(...),
    issue_date: str = Form(...),
    expiry_date: str = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO credentials
               (doctor_id, credential_type, credential_number, issue_date, expiry_date)
               VALUES (%s, %s, %s, %s, %s)""",
            (doctor_id, credential_type, credential_number, issue_date, expiry_date)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Credential added"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /fetch_credentials ----------

@router.post("/fetch_credentials")
async def fetch_credentials(doctor_id: int = Form(...)):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM credentials WHERE doctor_id = %s", (doctor_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"success": True, "data": rows}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /change_password ----------

@router.post("/change_password")
async def change_password(
    id: int = Form(...),
    current_password: str = Form(...),
    new_password: str = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id FROM doctors WHERE id = %s AND password = %s",
            (id, hash_password(current_password))
        )
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return {"success": False, "message": "Current password is incorrect"}

        cursor.execute(
            "UPDATE doctors SET password = %s WHERE id = %s",
            (hash_password(new_password), id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"success": True, "message": "Password changed successfully"}
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /forgot-password ----------

@router.post("/forgot-password")
async def forgot_password(email: str = Form(...)):
    """
    Check the email exists, generate a reset token, and return it.
    In production you would email the link; here we return it directly
    so the frontend can redirect the user immediately.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name FROM doctors WHERE email = %s", (email,))
        doctor = cursor.fetchone()
        cursor.close()
        conn.close()

        if not doctor:
            # Return success anyway to avoid email enumeration
            return {"success": True, "message": "If that email exists, a reset link has been sent."}

        token = secrets.token_urlsafe(32)
        _reset_tokens[token] = email

        return {
            "success": True,
            "message": "Password reset token generated.",
            "reset_token": token,   # frontend uses this to redirect to reset page
            "name": doctor["name"]
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


# ---------- /reset-password ----------

@router.post("/reset-password")
async def reset_password(
    token: str = Form(...),
    new_password: str = Form(...)
):
    """Verify the reset token and update the password."""
    email = _reset_tokens.get(token)
    if not email:
        return {"success": False, "message": "Invalid or expired reset token."}

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE doctors SET password = %s WHERE email = %s",
            (hash_password(new_password), email)
        )
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()

        if affected == 0:
            return {"success": False, "message": "Account not found."}

        # Invalidate the token after use
        del _reset_tokens[token]
        return {"success": True, "message": "Password reset successfully. You can now log in."}
    except Exception as e:
        return {"success": False, "message": str(e)}
