# My Domains Info

A self-hosted domain tracking and monitoring service that provides a centralized control panel for managing domains across different registrars, hosting providers, and DNS platforms.

## 🎯 Project Goal

**My Domains Info** solves the problem of tracking domains scattered across multiple registrars and hosting providers. It provides a single source of truth for your entire domain infrastructure, independent of where domains are registered or configured.

This service becomes your **domain control panel** that helps you:
- Track all your domains in one place
- Monitor domain health and configuration
- Audit DNS settings and network information
- Discover subdomains automatically
- Get insights into domain infrastructure

## ✨ Features

- **Domain Management**: Store and track root domains and subdomains
- **Automatic Subdomain Discovery**: Discovers subdomains via certificate transparency logs
- **DNS Analysis**: Comprehensive DNS record resolution (A, AAAA, MX, NS, CNAME, SOA, TXT)
- **IP Resolution**: Automatic IP address detection and validation
- **Geographic Information**: Geo-location data (city, country) for domain IPs
- **Network Intelligence**: ASN lookup and network owner identification
- **Anycast Detection**: Identifies if domains are using anycast networking
- **Domain Health Monitoring**: Tracks domain activity and resolution status
- **Bulk Refresh**: Update all domain information with a single command
- **Web Interface**: Modern Vue.js frontend for easy management
- **REST API**: Clean API for programmatic access

## 🚀 Quick Start

**The fastest way to get started** - run the prebuilt Docker image with a single command:

```bash
docker run -d \
  -p 80:80 \
  -v my-domains-data:/app \
  --name my-domains-info \
  yoorudziankou/my-domain-info:latest
```

**Command breakdown:**
- `-p 80:80` - Maps port 80 from container to host
- `-v my-domains-data:/app` - Persists database to a Docker named volume (recommended)
- `--name my-domains-info` - Names the container for easy management

**Alternative: Persist data to a local directory**
```bash
mkdir -p ./data
docker run -d \
  -p 80:80 \
  -v $(pwd)/data:/app \
  --name my-domains-info \
  yoorudziankou/my-domain-info:latest
```

> **Note:** The database file is stored in the `/app` directory inside the container. Mounting `/app` will persist your database data. Using a named volume is recommended for production use.

That's it! The application will automatically run database migrations and start serving.

**Access the application:**
- Web UI: http://localhost
- API Documentation: http://localhost/api/docs

### Using the Web Interface

1. **Add a Domain:**
   - Click the "Add Domain" button
   - Enter the domain name (e.g., `example.com`)
   - The system will automatically discover and add all subdomains

2. **View Domains:**
   - Browse the domain table with pagination
   - View detailed information including IP address, geolocation, DNS settings, network owner, and domain health

3. **Refresh Domains:**
   - Click the "Refresh" button to update all domain information

### Using the API

**Add a domain:**
```bash
curl -X POST "http://localhost/api/domain-info/" \
  -H "Content-Type: application/json" \
  -d '{"domain_name": "example.com"}'
```

**Get all domains:**
```bash
curl "http://localhost/api/domain-info/?limit=25&offset=0"
```

**Refresh all domains:**
```bash
curl -X POST "http://localhost/api/domain-info/refresh"
```

## 📖 What Information is Collected?

For each domain, the service automatically collects:

- ✅ Domain name and type (root or subdomain)
- ✅ IP address
- ✅ DNS records (A, AAAA, MX, NS, CNAME, SOA, TXT)
- ✅ Geographic location (city, country)
- ✅ Network owner information
- ✅ Anycast detection
- ✅ Domain health status

## 🔧 Configuration

The application works out of the box with default settings. For advanced configuration, create a `.env` file in the project root. See [backend/README.md](backend/README.md) for detailed configuration options.

## 📚 Documentation

- **Technical Documentation**: See [backend/README.md](backend/README.md) for architecture, development setup, API details, and deployment guides

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgments

- [crt.sh](https://crt.sh) for certificate transparency logs
- [IPWhois](http://ipwho.is/) for IP geolocation
- [IPInfo](https://ipinfo.io) for IP information services

---

**Made with ❤️ for domain administrators who need a single source of truth**
