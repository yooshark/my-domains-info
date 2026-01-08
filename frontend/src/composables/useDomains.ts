import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query"
import { addDomain, fetchDomains, refreshDomains } from "@/api/domain"

export function useDomains() {
  const queryClient = useQueryClient()

  const domainsQuery = useQuery({
    queryKey: ["domains"],
    queryFn: fetchDomains,
  })

  const addDomainMutation = useMutation({
    mutationFn: addDomain,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["domains"] })
    },
  })

  const refreshMutation = useMutation({
    mutationFn: refreshDomains,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["domains"] })
    },
  })

  return {
    domainsQuery,
    addDomainMutation,
    refreshMutation,
  }
}
