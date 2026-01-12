from fastapi import HTTPException
from pydantic import BaseModel, field_validator

from app.core.utils import normalize_domain


class DomainInfoCreate(BaseModel):
    domain_name: str

    @field_validator("domain_name", mode="before")
    @classmethod
    def normalize_and_validate_domain(cls, v: str) -> str:
        domain = normalize_domain(v)
        if not domain:
            raise HTTPException(status_code=400, detail="Domain name cannot be empty")
        return domain


class DomainInfoRead(BaseModel):
    domain_name: str
    ip_address: str | None = None

    geo_city: str | None = None
    geo_country: str | None = None
    network_owner_name: str | None = None
    is_anycast_node: bool
    is_active: bool | None = None

    dns_settings: dict[str, list[str]] | None = None


class DomainInfoResponse(BaseModel):
    items: list[DomainInfoRead]
    total: int
