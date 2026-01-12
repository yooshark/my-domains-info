import type { DomainInfo, PaginatedDomainsResponse } from "@/types/domain"

interface ErrorResponse {
  detail?: string
}

// Normalize API URL: ensure it ends with /api but no trailing slash
function getApiUrl(): string {
  const envUrl = import.meta.env.VITE_API_URL
  if (envUrl && typeof envUrl === "string") {
    // Remove trailing slash if present, then ensure /api is at the end
    const clean = envUrl.replace(/\/+$/, "")
    return clean.endsWith("/api") ? clean : `${clean}/api`
  }
  return "http://localhost:8000/api"
}

const API_URL = getApiUrl()

export async function fetchDomains(
  page = 1,
  limit = 25,
): Promise<PaginatedDomainsResponse> {
  const offset = (page - 1) * limit
  const url = new URL(`${API_URL}/domain-info/`)
  url.searchParams.set("limit", limit.toString())
  url.searchParams.set("offset", offset.toString())

  if (import.meta.env.DEV) {
    console.log("🌐 fetchDomains: Calling API at", url.toString())
  }

  try {
    const res = await fetch(url.toString())
    if (!res.ok) {
      let errorMessage = "Failed to load domains"
      try {
        const err = (await res.json()) as ErrorResponse
        errorMessage = err.detail ?? errorMessage
      } catch {
        // If response is not JSON, use status text
        errorMessage = res.statusText || errorMessage
      }
      throw new Error(errorMessage)
    }
    return (await res.json()) as PaginatedDomainsResponse
  } catch (error) {
    if (error instanceof Error) {
      throw error
    }
    throw new Error("Failed to load domains")
  }
}

export async function addDomain(domain: string): Promise<DomainInfo> {
  try {
    const res = await fetch(`${API_URL}/domain-info/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ domain_name: domain }),
    })

    if (!res.ok) {
      let errorMessage = "Failed to add domain"
      try {
        const err = (await res.json()) as ErrorResponse
        errorMessage = err.detail ?? errorMessage
      } catch {
        // If response is not JSON, use status text
        errorMessage = res.statusText || errorMessage
      }
      const error = new Error(errorMessage) as Error & { detail?: string }
      error.detail = errorMessage
      throw error
    }

    return (await res.json()) as DomainInfo
  } catch (error) {
    if (error instanceof Error) {
      throw error
    }
    throw new Error("Failed to add domain")
  }
}

export async function refreshDomains(): Promise<void> {
  try {
    const res = await fetch(`${API_URL}/domain-info/refresh`, {
      method: "POST",
    })

    if (!res.ok) {
      let errorMessage = "Failed to refresh domains"
      try {
        const err = (await res.json()) as ErrorResponse
        errorMessage = err.detail ?? errorMessage
      } catch {
        errorMessage = res.statusText || errorMessage
      }
      const error = new Error(errorMessage) as Error & { detail?: string }
      error.detail = errorMessage
      throw error
    }
  } catch (error) {
    if (error instanceof Error) {
      throw error
    }
    throw new Error("Failed to refresh domains")
  }
}
