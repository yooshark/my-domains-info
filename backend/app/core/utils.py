from urllib.parse import urlparse


def normalize_domain(value: str) -> str:
    value = value.strip().lower().strip(" '\"")

    if not value:
        return ""

    if not value.startswith(("http://", "https://")):
        value = "http://" + value

    parsed = urlparse(value)

    host = parsed.netloc or parsed.path

    host = host.split("@")[-1]
    host = host.split(":")[0]

    return host
