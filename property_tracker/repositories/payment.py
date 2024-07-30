from sqlalchemy.orm import Session

from property_tracker.models import Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_payment(self, payment: Payment):
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_payment(self, payment_id: int):
        return self.db.query(Payment).filter(Payment.id == payment_id).first()

    def get_all_payments(self):
        return self.db.query(Payment).all()

    def update_payment(self, payment_id: int, amount: float):
        payment = self.get_payment(payment_id)
        payment.amount = amount
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def delete_payment(self, payment_id: int):
        payment = self.get_payment(payment_id)
        self.db.delete(payment)
        self.db.commit()
        return payment
