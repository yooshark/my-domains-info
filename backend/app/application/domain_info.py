import asyncio
import logging
import socket
from typing import Any

import dns.resolver
import tldextract
from fastapi import HTTPException

from app.core.enums import DomainTypes
from app.core.uow import SaSessionUnitOfWork
from app.db.models.domain_info import DomainInfo
from app.infrastructure.crt_sh_client import CrtShClient
from app.infrastructure.ipinfo_client import IpInfoClient
from app.infrastructure.ipwhois_client import IpWhoIsClient

logger = logging.getLogger("app")


class DomainInfoService:
    DNS_RECORD_TYPES = ["A", "AAAA", "MX", "NS", "CNAME", "SOA", "TXT"]

    def __init__(
        self,
        uow: SaSessionUnitOfWork,
        crt_sh_cl: CrtShClient,
        ip_who_is_cl: IpWhoIsClient,
        ip_info_cl: IpInfoClient,
    ):
        self.uow = uow
        self.crt_sh_cl = crt_sh_cl
        self.ip_who_is_cl = ip_who_is_cl
        self.ip_info_cl = ip_info_cl

    @staticmethod
    async def resolve_ip(host: str) -> str:
        return await asyncio.to_thread(socket.gethostbyname, host)

    @staticmethod
    async def get_domain_type(domain: str) -> DomainTypes:
        ext = await asyncio.to_thread(tldextract.extract, domain)
        if ext.subdomain:
            return DomainTypes.SUBDOMAIN
        return DomainTypes.ROOT

    async def get_dns_settings(self, domain: str) -> dict[str, Any]:
        result = {}

        for record in self.DNS_RECORD_TYPES:
            try:
                answers = await asyncio.to_thread(dns.resolver.resolve, domain, record)
                r = [r.to_text() for r in answers]
                if r:
                    result[record] = r
            except Exception as exc:
                logger.error(f"Failed to resolve {record}: {exc}")
                continue

        return result

    async def get_target_domains(self, domain: str) -> list[str]:
        data = await self.crt_sh_cl.get_subdomains(domain)
        subs = set()
        for item in data:
            name: str = item["name_value"]
            for sub in name.split("\n"):
                if sub.endswith(domain):
                    subs.add(sub.lower())
        subs.add(domain)
        return list(subs)

    async def collect_domain_info(self, data: dict[str, Any]) -> dict[str, Any]:
        ip_address = await self.resolve_ip(data["domain_name"])

        ip_info_data, ip_who_is_data, dns_settings, domain_type = await asyncio.gather(
            self.ip_info_cl.get_ip_info(ip_address),
            self.ip_who_is_cl.get_ip_info(ip_address),
            self.get_dns_settings(data["domain_name"]),
            self.get_domain_type(data["domain_name"]),
        )

        data["domain_type"] = domain_type
        data["ip_address"] = ip_address
        data["geo_city"] = ip_who_is_data.get("city", "")
        data["geo_country"] = ip_who_is_data.get("country", "")
        data["network_owner_name"] = ip_who_is_data.get("connection", {}).get("org", "")
        data["is_active"] = ip_who_is_data.get("success", False)
        data["is_anycast_node"] = ip_info_data.get("anycast", False)
        data["dns_settings"] = dns_settings
        return data

    async def handle_domain_name(self, domain_name: str) -> list[DomainInfo]:
        domains = await self.get_target_domains(domain_name)
        tasks = [self.collect_domain_info({"domain_name": d}) for d in domains]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results: list[dict[str, Any]] = []

        for domain, result in zip(domains, results, strict=True):
            if isinstance(result, dict):
                valid_results.append(result)
            if isinstance(result, Exception):
                logger.warning(
                    "Failed to collect",
                    extra={"domain": domain, "result": repr(result)},
                )
        async with self.uow:
            return await self.uow.domain_info.bulk_insert(valid_results)

    async def add_domain(self, domain_name: str) -> list[DomainInfo]:
        async with self.uow:
            existing = await self.uow.domain_info.get_by_domain_name(domain_name)
            if existing is not None:
                raise HTTPException(
                    status_code=400, detail="Domain name already exists"
                )
        return await self.handle_domain_name(domain_name)

    async def get_domains_info(
        self,
        limit: int,
        offset: int,
    ) -> tuple[int | None, list[DomainInfo]]:
        async with self.uow:
            return await self.uow.domain_info.get_domains_info(
                limit=limit, offset=offset
            )

    async def refresh_domains_info(self) -> dict[str, str]:
        async with self.uow:
            root_domains = await self.uow.domain_info.get_root_domain_names()
            if not root_domains:
                return {"status": "ok"}
        root_domains_results = await asyncio.gather(
            *(self.get_target_domains(d) for d in root_domains),
            return_exceptions=True,
        )

        domains_to_update: set[str] = set()

        for res in root_domains_results:
            if isinstance(res, list):
                domains_to_update.update(res)

        if not domains_to_update:
            return {"status": "ok"}

        async with self.uow:
            rows = await self.uow.domain_info.get_domain_names()
        domains: dict[str, int] = {domain: id_ for id_, domain in rows}
        tasks = [
            self.collect_domain_info({"domain_name": d, "id": domains.get(d)})
            for d in domains_to_update
        ]

        results: list[dict[str, Any] | BaseException] = await asyncio.gather(
            *tasks, return_exceptions=True
        )

        valid_results: list[dict[str, Any]] = []

        for domain, result in zip(domains_to_update, results, strict=True):
            if isinstance(result, dict):
                valid_results.append(result)
            if isinstance(result, Exception):
                logger.warning(
                    "Failed to refresh domain",
                    extra={"domain": domain, "result": repr(result)},
                )

        if valid_results:
            async with self.uow:
                await self.uow.domain_info.update_domains_info(data=valid_results)
        return {"status": "ok"}
