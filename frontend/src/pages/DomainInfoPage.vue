<script setup lang="ts">
import { computed } from "vue"
import { useDomains, useRefreshDomains } from "@/composables/useDomainInfo"
import { useToast } from "@/composables/useToast"
import AddDomainModal from "@/components/AddDomainModal.vue"
import DomainTable from "@/components/DomainTable.vue"

const { data, isLoading, error } = useDomains()
const refresh = useRefreshDomains()
const { showToast } = useToast()

const isRefreshDisabled = computed(() => {
  return refresh.isPending.value
})

function handleRefresh() {
  refresh.mutate(undefined, {
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
  <div class="p-6 space-y-4">
    <div class="flex gap-2">
      <AddDomainModal/>
      <button
          class="btn"
          :disabled="isRefreshDisabled"
          @click="handleRefresh"
      >
        🔄 Обновить
      </button>
    </div>

    <DomainTable
        v-if="data"
        :domains="data"
    />

    <p v-if="isLoading">Загрузка…</p>
    <p v-if="error" class="text-red-500">Ошибка загрузки</p>
  </div>
</template>
