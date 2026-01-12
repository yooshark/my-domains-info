import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { addDomain, fetchDomains, refreshDomains } from "@/api/domain"
import type { DomainInfo } from "@/types/domain"

export function useDomains() {
  if (import.meta.env.DEV) {
    console.log("📡 useDomains: Setting up query...")
  }
  return useQuery<DomainInfo[]>({
    queryKey: ["domains"],
    queryFn: async () => {
      if (import.meta.env.DEV) {
        console.log("📡 useDomains: Fetching domains...")
      }
      try {
        const result = await fetchDomains()
        if (import.meta.env.DEV) {
          console.log("✅ useDomains: Fetched", result.length, "domains")
        }
        return result
      } catch (error) {
        if (import.meta.env.DEV) {
          console.error("❌ useDomains: Error fetching domains", error)
        }
        throw error
      }
    },
  })
}

export function useAddDomain() {
  const qc = useQueryClient()

  return useMutation<DomainInfo, Error, string>({
    mutationFn: addDomain,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["domains"] })
    },
  })
}

export function useRefreshDomains() {
  const qc = useQueryClient()

  return useMutation<void, Error, void>({
    mutationFn: refreshDomains,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["domains"] })
    },
  })
}
