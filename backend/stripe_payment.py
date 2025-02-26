import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Set your Stripe secret key
stripe.api_key = "sk_test_your_secret_key_here"  # Replace with your actual key

class PaymentRequest(BaseModel):
    amount: int  # in cents
    currency: str = "usd"
    description: str
    receipt_email: str

@router.post("/create-payment-intent")
def create_payment_intent(payment: PaymentRequest):
    try:
        intent = stripe.PaymentIntent.create(
            amount=payment.amount,
            currency=payment.currency,
            description=payment.description,
            receipt_email=payment.receipt_email,
        )
        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
