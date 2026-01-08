<script setup lang="ts">
import { computed } from "vue"
import { useDomains, useRefreshDomains } from "@/composables/useDomainInfo"

const { data, isLoading, error } = useDomains()
const refresh = useRefreshDomains()

const _isRefreshDisabled = computed(() => {
  return refresh.isPending.value
})
</script>

<template>
  <div class="p-6 space-y-4">
    <div class="flex gap-2">
      <AddDomainModal/>
      <button
          class="btn"
          :disabled="isRefreshDisabled"
          @click="refresh.mutate()"
      >
        🔄 Обновить
      </button>
    </div>

    <DomainTable
        v-if="data"
        :items="data"
    />

    <p v-if="isLoading">Загрузка…</p>
    <p v-if="error" class="text-red-500">Ошибка загрузки</p>
  </div>
</template>
