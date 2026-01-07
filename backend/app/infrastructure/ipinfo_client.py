from app.core.settings import IpInfoClientSettings
from app.infrastructure.base import BaseRequestsClient


class IpInfoClient(BaseRequestsClient):
    def __init__(self, cfg: IpInfoClientSettings):
        self.base_url = cfg.BASE_URL
        self.timeout = cfg.TIMEOUT
