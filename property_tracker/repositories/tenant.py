from sqlalchemy.orm import Session

from property_tracker.models.tenant import Tenant


class TenantRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_tenant(self, tenant: Tenant):
        self.db.add(tenant)
        self.db.commit()
        self.db.refresh(tenant)
        return tenant

    def get_tenant(self, tenant_id: int):
        return self.db.query(Tenant).filter(Tenant.id == tenant_id).first()

    def get_all_tenants(self):
        return self.db.query(Tenant).all()

    def update_tenant(self, tenant_id: int, name: str):
        tenant = self.get_tenant(tenant_id)
        tenant.name = name
        self.db.commit()
        self.db.refresh(tenant)
        return tenant

    def delete_tenant(self, tenant_id: int):
        tenant = self.get_tenant(tenant_id)
        self.db.delete(tenant)
        self.db.commit()
        return tenant
