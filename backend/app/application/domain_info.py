import asyncio
import logging
import socket
from typing import Any

import dns.resolver
import httpx
from fastapi import HTTPException

from app.db.models import DomainInfo
from app.db.repositories.domain_info import DomainInfoRepository
from app.infrastructure.crt_sh_client import CrtShClient
from app.infrastructure.ipinfo_client import IpInfoClient
from app.infrastructure.ipwhois_client import IpWhoIsClient

logger = logging.getLogger("app")


class DomainInfoService:
    DNS_RECORD_TYPES = ["A", "AAAA", "MX", "NS", "CNAME", "SOA", "TXT"]

    def __init__(
        self,
        repo: DomainInfoRepository,
        crt_sh_cl: CrtShClient,
        ip_who_is_cl: IpWhoIsClient,
        ip_info_cl: IpInfoClient,
    ):
        self.repo = repo
        self.crt_sh_cl = crt_sh_cl
        self.ip_who_is_cl = ip_who_is_cl
        self.ip_info_cl = ip_info_cl

    @staticmethod
    async def resolve_ip(host: str) -> str:
        return await asyncio.to_thread(socket.gethostbyname, host)

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
            name = item["name_value"]
            for sub in name.split("\n"):
                if sub.endswith(domain):
                    subs.add(sub.lower())
        subs.add(domain)
        return list(subs)

    async def collect_domain_info(self, data: dict[str, Any]) -> dict[str, Any]:
        ip_address = await self.resolve_ip(data["domain_name"])

        ip_info_data, ip_who_is_data, dns_settings = await asyncio.gather(
            self.ip_info_cl.get_ip_info(ip_address),
            self.ip_who_is_cl.get_ip_info(ip_address),
            self.get_dns_settings(data["domain_name"]),
        )

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

        valid_results = []

        for domain, result in zip(domains, results, strict=True):
            if isinstance(result, Exception):
                logger.warning(
                    "Failed to collect",
                    extra={"domain": domain, "result": repr(result)},
                )
                continue
            valid_results.append(result)
        return await self.repo.bulk_insert(valid_results)

    async def add_domain(self, domain_name: str) -> list[DomainInfo]:
        existing = await self.repo.get_by_domain_name(domain_name)
        if existing is not None:
            raise HTTPException(status_code=400, detail="Domain name already exists")
        try:
            return await self.handle_domain_name(domain_name)
        except socket.gaierror:
            message = (
                f"Failed to determine IP for the address: {domain_name}\n\n"
                "Possible reasons:\n"
                "• the domain does not exist\n"
                "• the domain is entered incorrectly\n"
                "• the DNS server did not respond"
            )
            raise HTTPException(status_code=400, detail=message)
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=400, detail=exc.response.json())

    async def get_domains_info(
        self,
        limit: int,
        offset: int,
    ) -> tuple[int, list[DomainInfo]]:
        return await self.repo.get_domains_info(limit=limit, offset=offset)

    async def refresh_domains_info(self) -> None:
        domain_names = await self.repo.get_domain_names()
        if not domain_names:
            return
        tasks = [
            self.collect_domain_info({"id": idx, "domain_name": name})
            for idx, name in domain_names
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = []

        for domain, result in zip(domain_names, results, strict=True):
            if isinstance(result, Exception):
                logger.warning(
                    "Failed to refresh domain",
                    extra={"domain": domain, "result": repr(result)},
                )
                continue
            valid_results.append(result)

        if not valid_results:
            return
        await self.repo.update_domains_info(data=valid_results)
