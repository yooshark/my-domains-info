import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { addDomain, fetchDomains, refreshDomains } from "@/api/domain"
import type { PaginatedDomainsResponse } from "@/types/domain"
import { ref } from "vue"

export function useDomains(page = ref(1)) {
  if (import.meta.env.DEV) {
    console.log("📡 useDomains: Setting up query...")
  }
  return useQuery<PaginatedDomainsResponse>({
    queryKey: ["domains", page],
    queryFn: async () => {
      if (import.meta.env.DEV) {
        console.log("📡 useDomains: Fetching domains page", page.value)
      }
      try {
        const result = await fetchDomains(page.value, 25)
        if (import.meta.env.DEV) {
          console.log(
            "✅ useDomains: Fetched",
            result.items.length,
            "domains (total:",
            result.total,
            ")",
          )
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

  return useMutation({
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
