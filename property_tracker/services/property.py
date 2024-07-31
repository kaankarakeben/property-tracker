from property_tracker.models.property import Property
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
        purchase_price: float,
        current_value: float,
        rent: float,
    ):
        """
        Create a new property
        :param investor_id: int
        :param address: str
        :param purchase_price: float
        :param current_value: float
        :param rent: float
        :return: Property
        """

        new_property = Property(
            investor_id=investor_id,
            address=address,
            purchase_price=purchase_price,
            current_value=current_value,
            rent=rent,
        )
        return self.property_repository.add_property(new_property)

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
        purchase_price: float,
        current_value: float,
        rent: float,
    ):
        """
        Update a property
        :param property_id: int
        :param address: str
        :param purchase_price: float
        :param current_value: float
        :param rent: float
        :return: Property
        """

        property = self.get_property(property_id)
        property.address = address
        property.purchase_price = purchase_price
        property.current_value = current_value
        property.rent = rent
        return self.property_repository.update_property(property)

    def delete_property(self, property_id: int):
        """
        Delete a property
        :param property_id: int
        :return: None
        """

        property = self.get_property(property_id)
        self.property_repository.delete_property(property)
