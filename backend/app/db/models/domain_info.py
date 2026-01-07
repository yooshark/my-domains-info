from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from app.db.models.base import Base


class DomainInfo(Base):
    __tablename__ = "domain_info"

    domain_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    subdomains: Mapped[JSON | None] = mapped_column(type_=JSON, nullable=True)

    ip_address: Mapped[str | None] = mapped_column(nullable=True)

    geo_city: Mapped[str | None] = mapped_column(nullable=True)
    geo_country: Mapped[str | None] = mapped_column(nullable=True)

    network_owner_name: Mapped[str | None] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(server_default="false", nullable=False)
    is_anycast_node: Mapped[bool] = mapped_column(
        server_default="false", nullable=False
    )
