<script setup lang="ts">
import { computed } from "vue";
import type { DomainInfo } from "@/types/domain";

interface Props {
	domains?: DomainInfo[];
	items?: DomainInfo[];
}

const props = defineProps<Props>();

const _domains = computed(() => props.domains ?? props.items ?? []);

function _getSubdomains(domain: DomainInfo): string[] {
	return domain.subdomains?.subdomains ?? [];
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
          <th>Domain</th>
          <th>IP</th>
          <th>Country</th>
          <th>City</th>
          <th>Network Owner</th>
          <th>Anycast</th>
          <th>Active</th>
          <th>Subdomains</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="d in domains" :key="d.domain_name">
          <td>{{ d.domain_name }}</td>
          <td>{{ d.ip_address ?? "—" }}</td>
          <td>{{ d.geo_country ?? "—" }}</td>
          <td>{{ d.geo_city ?? "—" }}</td>
          <td>{{ d.network_owner_name ?? "—" }}</td>
          <td>{{ d.is_anycast_node ? "Yes" : "No" }}</td>
          <td>{{ d.is_active ? "Yes" : "No" }}</td>
          <td>
            <div v-if="getSubdomains(d).length > 0" class="subdomains-container">
              <ul class="subdomains-list">
                <li v-for="(subdomain, idx) in getSubdomains(d)" :key="idx">
                  {{ subdomain }}
                </li>
              </ul>
            </div>
            <span v-else>—</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.table-wrapper {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
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
  text-align: left;
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
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  color: #374151;
  vertical-align: top;
}

.subdomains-container {
  height: 140px;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 4px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  background-color: #fafafa;
}

.subdomains-list {
  list-style: disc;
  list-style-position: inside;
  margin: 0;
  padding: 0;
}

.subdomains-list li {
  padding: 2px 0;
  font-size: 0.875rem;
  line-height: 1.4;
  color: #4b5563;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .table-wrapper {
    border-color: #374151;
  }

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

  .subdomains-container {
    border-color: #374151;
    background-color: #111827;
  }

  .subdomains-list li {
    color: #d1d5db;
  }
}
</style>
