from property_tracker.models import Tenant
from property_tracker.repositories import TenantRepository


class TenantService:
    """
    Service class for Tenant model
    """

    def __init__(self, tenant_repository: TenantRepository):
        self.tenant_repository = tenant_repository

    def create_tenant(self, property_id: int, name: str, contact_details: str):
        """
        Create a new tenant
        :param property_id: int
        :param name: str
        :param contact_details: str
        :return: Tenant
        """

        new_tenant = Tenant(
            property_id=property_id, name=name, contact_details=contact_details
        )
        return self.tenant_repository.add_tenant(new_tenant)

    def get_tenant(self, tenant_id: int):
        """
        Get a tenant by id
        :param tenant_id: int
        :return: Tenant
        """

        return self.tenant_repository.get_tenant(tenant_id)

    def get_all_tenants(self):
        """
        Get all tenants
        :return: List[Tenant]
        """

        return self.tenant_repository.get_all_tenants()

    def update_tenant(self, tenant_id: int, name: str, contact_details: str):
        """
        Update a tenant
        :param tenant_id: int
        :param name: str
        :param contact_details: str
        :return: Tenant
        """

        tenant = self.get_tenant(tenant_id)
        tenant.name = name
        tenant.contact_details = contact_details
        return self.tenant_repository.update_tenant(tenant)

    def delete_tenant(self, tenant_id: int):
        """
        Delete a tenant
        :param tenant_id: int
        :return: None
        """

        tenant = self.get_tenant(tenant_id)
        self.tenant_repository.delete_tenant(tenant)
