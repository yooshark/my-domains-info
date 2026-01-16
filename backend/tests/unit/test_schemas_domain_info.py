from socket import gaierror

import pytest
from fastapi import HTTPException

from app.schemas.domain_info import DomainInfoCreate


class TestDomainInfoCreateValidator:
    def test_valid_domain_passes(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def fake_gethostbyname(domain: str) -> str:
            assert domain == "example.com"
            return "1.2.3.4"

        monkeypatch.setattr("socket.gethostbyname", fake_gethostbyname)

        obj = DomainInfoCreate(domain_name="  https://example.com/  ")
        assert obj.domain_name == "example.com"

    def test_empty_domain_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def fake_gethostbyname(
            domain: str,
        ) -> str:  # pragma: no cover - should not be called
            raise AssertionError("gethostbyname should not be called for empty domain")

        monkeypatch.setattr("socket.gethostbyname", fake_gethostbyname)

        with pytest.raises(HTTPException) as exc:
            DomainInfoCreate(domain_name="   ")

        assert exc.value.status_code == 400
        assert "cannot be empty" in exc.value.detail.lower()

    def test_not_found_domain_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def fake_gethostbyname(domain: str) -> str:
            raise gaierror("not found")

        monkeypatch.setattr("socket.gethostbyname", fake_gethostbyname)

        with pytest.raises(HTTPException) as exc:
            DomainInfoCreate(domain_name="not-exists.invalid")

        assert exc.value.status_code == 400
        assert "not found" in exc.value.detail.lower()
