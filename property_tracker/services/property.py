from property_tracker.models.property import Property, PropertyType, Status
from property_tracker.repositories import PropertyRepository


class PropertyService:
    """
    Service class for Property model
    """

    def __init__(self, property_repository: PropertyRepository):
        self.property_repository = property_repository

    def create_property(
        self,
        address: str,
        postcode: str,
        city: str,
        description: str,
        no_of_bedrooms: int,
        no_of_bathrooms: int,
        sqm: float,
        floor: int,
        furnished: bool,
        property_type: PropertyType,
        status: Status,
    ):
        """
        Create a new property
        :param address: str
        :param postcode: str
        :param city: str
        :param description: str
        :param no_of_bedrooms: int
        :param no_of_bathrooms: int
        :param sqm: float
        :param floor: int
        :param furnished: bool
        :param property_type: Enum (PropertyType)
        :param status: Enum (Status)
        :return: Property
        """

        inv_property = Property(
            address=address,
            postcode=postcode,
            city=city,
            description=description,
            no_of_bedrooms=no_of_bedrooms,
            no_of_bathrooms=no_of_bathrooms,
            sqm=sqm,
            floor=floor,
            furnished=furnished,
            property_type=property_type,
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

    def delete_property(self, property_id: int):
        """
        Delete a property
        :param property_id: int
        :return: None
        """

        return self.property_repository.delete_property(property_id)
