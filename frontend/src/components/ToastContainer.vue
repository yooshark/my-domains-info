<script setup lang="ts">
import { useToast } from "@/composables/useToast";

const { toasts, removeToast } = useToast();
</script>

<template>
  <div class="toast-container">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      class="toast"
      @click="removeToast(toast.id)"
    >
      <div class="toast-content">
        <p class="toast-message">{{ toast.message }}</p>
        <button
          @click.stop="removeToast(toast.id)"
          class="toast-close"
          type="button"
          aria-label="Close"
        >
          ×
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 12px;
  pointer-events: none;
}

.toast {
  background-color: #dc2626;
  color: white;
  padding: 14px 18px;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  min-width: 300px;
  max-width: 500px;
  pointer-events: auto;
  animation: slide-in 0.3s ease-out;
  cursor: pointer;
}

.toast:hover {
  background-color: #b91c1c;
}

.toast-content {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.toast-message {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  margin: 0;
  flex: 1;
}

.toast-close {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  margin: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.9;
  transition: opacity 0.2s;
}

.toast-close:hover {
  opacity: 1;
}

@keyframes slide-in {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style>
