import httpx
from aioinject import Injected
from aioinject.ext.fastapi import inject
from fastapi import APIRouter, HTTPException, Query

from app.application.domain_info import DomainInfoService
from app.schemas.domain_info import (
    DomainInfoCreate,
    DomainInfoRead,
    DomainInfoResponse,
    RefreshResponse,
)

router = APIRouter(
    prefix="/domain-info",
    tags=["Domain Info"],
)


@router.get("/", response_model=DomainInfoResponse)
@inject
async def get_domains_info(
    service: Injected[DomainInfoService],
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    total, items = await service.get_domains_info(limit=limit, offset=offset)
    return {"total": total, "items": items}


@router.post("/", response_model=list[DomainInfoRead])
@inject
async def add_domain(data: DomainInfoCreate, service: Injected[DomainInfoService]):
    try:
        return await service.add_domain(data.domain_name)
    except HTTPException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=400, detail=exc.response.json())


@router.post("/refresh", response_model=RefreshResponse)
@inject
async def refresh_domains_info(service: Injected[DomainInfoService]):
    return await service.refresh_domains_info()
