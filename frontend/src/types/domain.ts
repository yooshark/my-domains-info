export interface DomainInfo {
	domain_name: string;
	ip_address?: string | null;
	subdomains?: { subdomains: string[] } | null;
	geo_city?: string | null;
	geo_country?: string | null;
	network_owner_name?: string | null;
	is_anycast_node: boolean;
	is_active?: boolean | null;
}
