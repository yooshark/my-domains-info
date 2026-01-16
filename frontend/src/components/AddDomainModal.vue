<script setup lang="ts">
import { computed, ref } from "vue"
import { useAddDomain } from "@/composables/useDomainInfo"
import { useToast } from "@/composables/useToast"

const domain = ref("")
const add = useAddDomain()
const { showToast } = useToast()

const isDisabled = computed(() => {
  return add.isPending.value
})

const buttonText = computed(() => {
  return add.isPending.value ? "Adding..." : "Add Domain"
})

function handleAdd() {
  const trimmed = domain.value.trim()
  if (!trimmed) return

  add.mutate(trimmed, {
    onSuccess: () => {
      domain.value = ""
    },
    onError: (error) => {
      const errorMessage =
        (error as Error & { detail?: string })?.detail || error.message || "Failed to add domain"
      showToast(errorMessage, "error")
    },
  })
}
</script>

<template>
  <div class="add-domain">
    <input
        v-model="domain"
        placeholder="example.com"
        class="input"
        @keyup.enter="handleAdd"
    />
    <button
        class="btn"
        :disabled="isDisabled"
        @click="handleAdd"
        type="button"
    >
      {{ buttonText }}
    </button>
  </div>
</template>

<style scoped>
.add-domain {
  display: flex;
  gap: 8px;
  align-items: center;
}

.input {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  flex: 1;
}

.btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #646cff;
  color: white;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  color: red;
  font-size: 0.875em;
  margin: 4px 0 0 0;
}
</style>
