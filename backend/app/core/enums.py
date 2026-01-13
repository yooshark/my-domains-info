from enum import Enum


class DomainTypes(str, Enum):
    ROOT = "root"
    SUBDOMAIN = "subdomain"
