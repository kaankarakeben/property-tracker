from property_tracker.models.payment import Payment
from property_tracker.repositories import PaymentRepository


class PaymentService:
    """
    Service class for Payment Service
    """

    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def create_payment(
        self, property_id: int, payment_date: str, amount: float, is_rent: bool
    ):
        """
        Create a new payment
        :param property_id: int
        :param payment_date: str
        :param amount: float
        :param is_rent: bool
        :return: Payment
        """

        new_payment = Payment(
            property_id=property_id,
            payment_date=payment_date,
            amount=amount,
            is_rent=is_rent,
        )
        return self.payment_repository.add_payment(new_payment)

    def get_payment(self, payment_id: int):
        """
        Get a payment by id
        :param payment_id: int
        :return: Payment
        """

        return self.payment_repository.get_payment(payment_id)

    def get_all_payments(self):
        """
        Get all payments
        :return: List[Payment]
        """

        return self.payment_repository.get_all_payments()

    def update_payment(
        self, payment_id: int, payment_date: str, amount: float, is_rent: bool
    ):
        """
        Update a payment
        :param payment_id: int
        :param payment_date: str
        :param amount: float
        :param is_rent: bool
        :return: Payment
        """

        payment = self.get_payment(payment_id)
        payment.payment_date = payment_date
        payment.amount = amount
        payment.is_rent = is_rent
        return self.payment_repository.update_payment(payment)

    def delete_payment(self, payment_id: int):
        """
        Delete a payment
        :param payment_id: int
        :return: None
        """

        payment = self.get_payment(payment_id)
        self.payment_repository.delete_payment(payment)
