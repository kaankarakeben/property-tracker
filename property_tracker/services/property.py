from property_tracker.models.property import (
    Property,
    PropertyType,
    PurchaseCurrency,
    Status,
)
from property_tracker.repositories import PropertyRepository


class PropertyService:
    """
    Service class for Property model
    """

    def __init__(self, property_repository: PropertyRepository):
        self.property_repository = property_repository

    def create_property(
        self,
        investor_id: int,
        address: str,
        purchase_date: str,
        purchase_price: float,
        purchase_currency: PurchaseCurrency,
        property_type: PropertyType,
        status: Status,
    ):
        """
        Create a property
        :param investor_id: int
        :param address: str
        :param purchase_date: str
        :param purchase_price: float
        :param purchase_currency: Enum (PurchaseCurrency)
        :param property_type: Enum (PropertyType)
        :param status: str
        :return: Property
        """
        inv_property = Property(
            owner_id=investor_id,
            address=address,
            purchase_date=purchase_date,
            purchase_price=purchase_price,
            purchase_currency=purchase_currency,
            type=property_type,
            status=status,
        )
        return self.property_repository.add_property(inv_property)

    def get_property(self, property_id: int):
        """
        Get a property by id
        :param property_id: int
        :return: Property
        """

        return self.property_repository.get_property(property_id)

    def get_all_properties(self):
        """
        Get all properties
        :return: List[Property]
        """

        return self.property_repository.get_all_properties()

    def update_property(
        self,
        property_id: int,
        address: str,
        purchase_date: str,
        purchase_price: float,
        purchase_currency: PurchaseCurrency,
        property_type: PropertyType,
        status: Status,
    ):
        """
        Update a property
        :param property_id: int
        :param address: str
        :param purchase_date: str
        :param purchase_price: float
        :param purchase_currency: Enum (PurchaseCurrency)
        :param property_type: Enum (PropertyType)
        :param status: str
        :return: Property
        """

        inv_property = Property(
            id=property_id,
            address=address,
            purchase_date=purchase_date,
            purchase_price=purchase_price,
            purchase_currency=purchase_currency,
            type=property_type,
            status=status,
        )

        return self.property_repository.update_property(inv_property)
