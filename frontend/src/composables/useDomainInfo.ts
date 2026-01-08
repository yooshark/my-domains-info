import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";
import { addDomain, fetchDomains, refreshDomains } from "@/api/domain";
import type { DomainInfo } from "@/types/domain";

export function useDomains() {
	return useQuery<DomainInfo[]>({
		queryKey: ["domains"],
		queryFn: fetchDomains,
	});
}

export function useAddDomain() {
	const qc = useQueryClient();

	return useMutation<DomainInfo, Error, string>({
		mutationFn: addDomain,
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ["domains"] });
		},
	});
}

export function useRefreshDomains() {
	const qc = useQueryClient();

	return useMutation({
		mutationFn: refreshDomains,
		onSuccess: () => {
			qc.invalidateQueries({ queryKey: ["domains"] });
		},
	});
}
