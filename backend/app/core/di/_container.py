import aioinject
from aioinject.ext.fastapi import FastAPIExtension

from app.application.domain_info import DomainInfoService
from app.core import settings
from app.core.server import new_server
from app.db.providers import (
    create_engine,
    create_session,
    make_async_sessionmaker,
    sa_session_uow,
)
from app.db.repositories.domain_info import DomainInfoRepository
from app.infrastructure.crt_sh_client import CrtShClient
from app.infrastructure.ipinfo_client import IpInfoClient
from app.infrastructure.ipwhois_client import IpWhoIsClient


def new_container() -> aioinject.Container:
    container = aioinject.Container(extensions=[FastAPIExtension()])
    container.register(
        aioinject.Singleton(settings.AppSettings.new),
        aioinject.Singleton(settings.DatabaseSettings.new),
        aioinject.Singleton(settings.CrtShClientSettings.new),
        aioinject.Singleton(settings.IpWhoIsClientSettings.new),
        aioinject.Singleton(settings.IpInfoClientSettings.new),
        aioinject.Singleton(CrtShClient),
        aioinject.Singleton(IpWhoIsClient),
        aioinject.Singleton(IpInfoClient),
        aioinject.Singleton(DomainInfoService),
        aioinject.Singleton(DomainInfoRepository),
        aioinject.Singleton(create_engine),
        aioinject.Singleton(make_async_sessionmaker),
        aioinject.Singleton(new_server),
        aioinject.Scoped(create_session),
        aioinject.Scoped(sa_session_uow),
    )

    return container


container: aioinject.Container = new_container()
