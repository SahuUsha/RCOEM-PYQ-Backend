from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    message: str

@router.post("/send-request")
async def send_contact_email(form_data: ContactForm):
    html = f"""
    <p><strong>Name:</strong> {form_data.name}</p>
    <p><strong>Email:</strong> {form_data.email}</p>
    <p><strong>Message:</strong><br>{form_data.message}</p>
    """

    # Create config dynamically to set the Sender Name correctly
    conf = ConnectionConfig(
        MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'default@gmail.com'),
        MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'xney flnm rlnj kxha'),
        # We MUST use the authenticated email here to prevent Google from stripping our custom name
        MAIL_FROM = os.getenv('MAIL_USERNAME', 'default@gmail.com'),
        # This will set the display name to "riya" (from the form)
        MAIL_FROM_NAME = form_data.name,
        MAIL_PORT = int(os.getenv('MAIL_PORT', 587)),
        MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
        MAIL_STARTTLS = True,
        MAIL_SSL_TLS = False,
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )

    message = MessageSchema(
        subject=f"New Contact Request from {form_data.name}",
        recipients=[os.getenv('MAIL_USERNAME', 'default@gmail.com')], # We revert this back to your inbox!
        body=html,
        subtype=MessageType.html,
        headers={"Reply-To": form_data.email}
    )

    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return {"message": "Email has been sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
