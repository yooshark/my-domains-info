import type { DomainInfo } from "@/types/domain";

// Normalize API URL: ensure it ends with /api but no trailing slash
function getApiUrl(): string {
	const envUrl = import.meta.env.VITE_API_URL;
	if (envUrl) {
		// Remove trailing slash if present, then ensure /api is at the end
		const clean = envUrl.replace(/\/+$/, "");
		return clean.endsWith("/api") ? clean : `${clean}/api`;
	}
	return "http://localhost:8000/api";
}

const API_URL = getApiUrl();

// Debug: log the API URL in development
if (import.meta.env.DEV) {
	console.log("[API] Base URL:", API_URL);
	console.log("[API] Full endpoints:", {
		fetch: `${API_URL}/domain-info/`,
		add: `${API_URL}/domain-info/`,
		refresh: `${API_URL}/domain-info/refresh`,
	});
}

export async function fetchDomains(): Promise<DomainInfo[]> {
	const res = await fetch(`${API_URL}/domain-info/`);
	if (!res.ok) {
		let errorMessage = "Failed to load domains";
		try {
			const err = await res.json();
			errorMessage = err.detail ?? errorMessage;
		} catch {
			// If response is not JSON, use status text
			errorMessage = res.statusText || errorMessage;
		}
		throw new Error(errorMessage);
	}
	return res.json();
}

export async function addDomain(domain: string): Promise<DomainInfo> {
	const res = await fetch(`${API_URL}/domain-info/`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ domain_name: domain }),
	});

	if (!res.ok) {
		let errorMessage = "Failed to add domain";
		try {
			const err = await res.json();
			errorMessage = err.detail ?? errorMessage;
		} catch {
			// If response is not JSON, use status text
			errorMessage = res.statusText || errorMessage;
		}
		const error = new Error(errorMessage) as Error & { detail?: string };
		error.detail = errorMessage;
		throw error;
	}

	return res.json();
}

export async function refreshDomains(): Promise<void> {
	const res = await fetch(`${API_URL}/domain-info/refresh`, {
		method: "POST",
	});

	if (!res.ok) {
		let errorMessage = "Failed to refresh domains";
		try {
			const err = await res.json();
			errorMessage = err.detail ?? errorMessage;
		} catch {
			errorMessage = res.statusText || errorMessage;
		}
		const error = new Error(errorMessage) as Error & { detail?: string };
		error.detail = errorMessage;
		throw error;
	}
}
