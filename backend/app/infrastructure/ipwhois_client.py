from app.core.settings import IpWhoIsClientSettings
from app.infrastructure.base import BaseRequestsClient


class IpWhoIsClient(BaseRequestsClient):
    def __init__(self, cfg: IpWhoIsClientSettings):
        self.base_url = cfg.BASE_URL
        self.timeout = cfg.TIMEOUT
