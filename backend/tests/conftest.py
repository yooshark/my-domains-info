import inspect
import typing
from collections.abc import AsyncIterator, Callable
from typing import Annotated, TypeVar

import aioinject
import pytest
import pytest_asyncio
from _pytest.fixtures import SubRequest
from aioinject import Inject
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.core import di
from app.core.server import new_server
from app.core.settings import AppSettings
from app.db.models.base import Base

T = TypeVar("T")


engine: AsyncEngine = create_async_engine(
    "sqlite+aiosqlite:///:memory:", echo=False, poolclass=StaticPool
)


@pytest.fixture
def app_settings() -> AppSettings:
    return AppSettings(
        DEBUG=True,
        DEVELOP=True,
        PROJECT_NAME="TestApp",
        VERSION="0.1",
        ALLOW_ORIGINS=["*"],
        ALLOW_ORIGIN_REGEX=None,
    )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db() -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    async with engine.connect() as conn:
        trans = await conn.begin()

        session = AsyncSession(
            bind=conn,
            expire_on_commit=False,
            autoflush=False,
        )

        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()


def make_fixture[T](
    context: aioinject.Context, typ: type[T]
) -> Callable[[], AsyncIterator[T]]:
    async def inner() -> AsyncIterator[T]:
        value = await context.resolve(typ)
        yield value

    return inner


@pytest.fixture
def aioinject_container() -> aioinject.Container:
    container = di.new_container()
    return container


@pytest.fixture
async def aioinject_context(
    aioinject_container: aioinject.Container,
) -> AsyncIterator[aioinject.Context]:
    async with aioinject_container.context() as ctx:
        yield ctx


@pytest.fixture(autouse=True)
def add_fixture_dynamically(
    request: SubRequest, aioinject_context: aioinject.Context
) -> None:
    signature = inspect.signature(request.function)
    for parameter in signature.parameters.values():
        if typing.get_origin(parameter.annotation) is not Annotated:
            continue
        args = typing.get_args(parameter.annotation)
        has_inject = Inject in args
        if not has_inject:
            continue

        injected_type = args[0]

        # Wire pytest fixture for this parameter name
        request._fixturemanager._arg2fixturedefs[parameter.name] = [
            pytest.FixtureDef(
                argname=parameter.name,
                func=make_fixture(aioinject_context, injected_type),
                scope="function",
                baseid=None,
                params=None,
                config=request.config,
            )
        ]


@pytest.fixture
async def test_app(
    aioinject_container: aioinject.Container, app_settings: AppSettings
) -> AsyncIterator[FastAPI]:
    async with aioinject_container.context():
        aioinject_container.register(
            aioinject.Object(app_settings, AppSettings),
        )

        app = new_server(app_settings)
        yield app


@pytest.fixture
async def api_client(test_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=test_app),
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
