<script setup lang="ts">
import { computed } from "vue"
import type { DomainInfo } from "@/types/domain"

interface Props {
  domains: DomainInfo[]
  currentPage: number
  totalPages: number
}

const props = defineProps<Props>()

const emit = defineEmits<{
  pageChange: [page: number]
}>()

const domains = computed(() => props.domains ?? [])

function getDnsRecordHelp(recordType: string): string {
  const helpMap: Record<string, string> = {
    A: "IPv4 address of the host",
    AAAA: "IPv6 address of the host",
    CNAME: "Creates an alias pointing to another domain",
    MX: "Mail exchange server for the domain",
    NS: "Name server for the domain",
    TXT: "Text record for various purposes",
    SRV: "Service location record",
    PTR: "Pointer record for reverse DNS",
    SOA: "Start of Authority record",
    CAA: "Certificate Authority Authorization",
  }
  return helpMap[recordType] || ""
}

function hasHelpText(recordType: string): boolean {
  return getDnsRecordHelp(recordType) !== ""
}

function goToPage(page: number) {
  if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
    emit("pageChange", page)
  }
}
</script>

<template>
  <div v-if="domains.length === 0" class="text-center py-8 text-gray-500">
    No domains found
  </div>
  <div v-else class="table-wrapper">
    <table class="domain-table">
      <thead>
        <tr>
          <th class="center-cell">Domain</th>
          <th class="center-cell">IP</th>
          <th class="center-cell">Country</th>
          <th class="center-cell">City</th>
          <th class="center-cell">Network Owner</th>
          <th class="center-cell">Anycast</th>
          <th class="center-cell">Active</th>
          <th class="center-cell">DNS Settings</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="d in domains" :key="d.domain_name">
          <td class="center-cell">{{ d.domain_name }}</td>
          <td class="center-cell">{{ d.ip_address ?? "—" }}</td>
          <td class="center-cell">{{ d.geo_country ?? "—" }}</td>
          <td class="center-cell">{{ d.geo_city ?? "—" }}</td>
          <td class="center-cell">{{ d.network_owner_name ?? "—" }}</td>
          <td class="center-cell">{{ d.is_anycast_node ? "Yes" : "No" }}</td>
          <td class="center-cell">
            <span
              class="status-dot"
              :class="d.is_active ? 'active' : 'inactive'"
              :title="d.is_active ? 'Active' : 'Inactive'"
            />
          </td>
          <td class="dns-column">
            <div
              v-if="d.dns_settings && Object.keys(d.dns_settings).length > 0"
              class="dns-container"
            >
              <div
                v-for="(values, recordType) in d.dns_settings"
                :key="recordType"
                class="dns-record"
                :title="hasHelpText(recordType) ? getDnsRecordHelp(recordType) : undefined"
              >
                <span class="dns-record-type">
                  {{ recordType }}<span v-if="hasHelpText(recordType)" class="dns-star">*</span>:
                </span>
                <span class="dns-record-values">{{ values.join(", ") }}</span>
              </div>
            </div>
            <span v-else class="dns-empty">—</span>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="totalPages > 0" class="pagination">
      <button
        class="pagination-btn"
        :disabled="currentPage === 1"
        @click="goToPage(currentPage - 1)"
        type="button"
        aria-label="Previous page"
      >
        ← Prev
      </button>
      <span class="pagination-info">
        Page {{ currentPage }} of {{ totalPages }}
      </span>
      <button
        class="pagination-btn"
        :disabled="currentPage === totalPages || totalPages === 0"
        @click="goToPage(currentPage + 1)"
        type="button"
        aria-label="Next page"
      >
        Next →
      </button>
    </div>
  </div>
</template>

<style scoped>
.table-wrapper {
  overflow-x: auto;
}

.domain-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
}

.domain-table thead {
  background-color: #f3f4f6;
}

.domain-table th {
  padding: 12px 16px;
  text-align: center;
  vertical-align: middle;
  font-weight: 600;
  color: #1f2937;
  border: 1px solid #e5e7eb;
  border-bottom: 2px solid #d1d5db;
  background-color: #f9fafb;
}

.domain-table tbody tr {
  border-bottom: 1px solid #e5e7eb;
}

.domain-table tbody tr:hover {
  background-color: #f9fafb;
}

.domain-table tbody tr:last-child {
  border-bottom: none;
}

.domain-table td {
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  color: #374151;
}

.center-cell {
  text-align: center;
  vertical-align: middle;
}

.dns-column {
  white-space: normal;
  max-width: 320px;
  padding: 8px 10px;
  vertical-align: top;
}

.dns-container {
  max-height: 90px;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 6px;
}

.dns-container::-webkit-scrollbar {
  width: 6px;
}

.dns-container::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 4px;
}

.dns-container::-webkit-scrollbar-thumb:hover {
  background-color: #9ca3af;
}


.dns-empty {
  text-align: center;
  color: #9ca3af;
}

.dns-star {
  color: #dc2626;
  font-size: 11px;
  margin-left: 2px;
  vertical-align: super;
}

.dns-record {
  margin-bottom: 6px;
  cursor: help;
  font-size: 0.875rem;
  line-height: 1.4;
  color: #374151;
}

.dns-record:last-child {
  margin-bottom: 0;
}

.dns-record-type {
  font-weight: 500;
  color: #111827;
}

.dns-record-values {
  color: #4b5563;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 20px;
  padding: 12px 0;
}

.pagination-btn {
  padding: 6px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background-color: white;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.active {
  background-color: #22c55e;
}

.status-dot.inactive {
  background-color: #ef4444;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .domain-table {
    background-color: #1f2937;
  }

  .domain-table thead {
    background-color: #111827;
  }

  .domain-table th {
    color: #f9fafb;
    border-color: #374151;
    background-color: #111827;
    border-bottom-color: #4b5563;
  }

  .domain-table tbody tr {
    border-bottom-color: #374151;
  }

  .domain-table tbody tr:hover {
    background-color: #1f2937;
  }

  .domain-table td {
    border-color: #374151;
    color: #e5e7eb;
  }

  .dns-record {
    color: #e5e7eb;
  }

  .dns-record-type {
    color: #f9fafb;
  }

  .dns-record-values {
    color: #d1d5db;
  }

  .pagination-btn {
    background-color: #1f2937;
    border-color: #374151;
    color: #e5e7eb;
  }

  .pagination-btn:hover:not(:disabled) {
    background-color: #374151;
  }

  .pagination-info {
    color: #9ca3af;
  }

  .dns-container::-webkit-scrollbar-thumb {
    background-color: #4b5563;
  }

  .dns-container::-webkit-scrollbar-thumb:hover {
    background-color: #6b7280;
  }
}
</style>
