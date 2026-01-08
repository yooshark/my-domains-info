<script setup lang="ts">
import { computed } from "vue"
import { useDomains, useRefreshDomains } from "@/composables/useDomainInfo"
import { useToast } from "@/composables/useToast"
import AddDomainModal from "@/components/AddDomainModal.vue"
import DomainTable from "@/components/DomainTable.vue"

const { data: domains, isLoading, error } = useDomains()
const refreshMutation = useRefreshDomains()
const { showToast } = useToast()


const isRefreshDisabled = computed(() => {
  return refreshMutation.isPending.value
})

const refreshButtonText = computed(() => {
  return refreshMutation.isPending.value ? "Refreshing..." : "Refresh Info"
})

function handleRefresh() {
  refreshMutation.mutate(undefined, {
    onSuccess: () => {
      // Query will automatically refetch due to invalidation
    },
    onError: (error) => {
      const errorMessage =
        (error as Error & { detail?: string })?.detail ||
        error.message ||
        "Failed to refresh domains"
      showToast(errorMessage, "error")
    },
  })
}
</script>

<template>
  <div class="container">
    <h1>Domain Information</h1>

    <div class="actions">
      <AddDomainModal/>
      <button
          @click="handleRefresh"
          :disabled="isRefreshDisabled"
          class="refresh-btn"
          type="button"
      >
        {{ refreshButtonText }}
      </button>
    </div>

    <div v-if="isLoading" class="status">Loading...</div>
    <div v-if="error" class="error">Error: {{ error.message }}</div>

    <DomainTable
        v-if="domains !== undefined"
        :domains="domains"
    />
  </div>
</template>

<style scoped>
.container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

h1 {
  margin-bottom: 24px;
}

.actions {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  align-items: flex-start;
}

.refresh-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #42b883;
  color: white;
  cursor: pointer;
  white-space: nowrap;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.status {
  padding: 12px;
  text-align: center;
  color: #666;
}

.error {
  padding: 12px;
  background-color: #fee;
  color: #c33;
  border-radius: 4px;
  margin-bottom: 16px;
}
</style>
