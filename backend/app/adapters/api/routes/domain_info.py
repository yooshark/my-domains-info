from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter

from app.application.domain_info import DomainInfoService
from app.schemas.domain_info import DomainInfoCreate, DomainInfoRead

router = APIRouter(
    prefix="/domain-info",
    tags=["Domain Info"],
)


@router.get("/", response_model=list[DomainInfoRead])
@inject
async def get_domains_info(service: Injected[DomainInfoService]):
    return await service.get_domains_info()


@router.post("/", response_model=DomainInfoRead)
@inject
async def add_domain(data: DomainInfoCreate, service: Injected[DomainInfoService]):
    return await service.add_domain(data.domain_name)


@router.post("/refresh")
@inject
async def refresh_domains_info(service: Injected[DomainInfoService]):
    return await service.refresh_domains_info()
