import { ref } from "vue"

export interface Toast {
  id: number
  message: string
  type: "error" | "success" | "info"
}

const toasts = ref<Toast[]>([])
let toastId = 0

export function useToast() {
  function showToast(
    message: string,
    type: "error" | "success" | "info" = "error",
  ) {
    const id = ++toastId
    const toast: Toast = { id, message, type }
    toasts.value.push(toast)

    // Auto-hide after 4 seconds (within 3-5 second range)
    setTimeout(() => {
      removeToast(id)
    }, 4000)
  }

  function removeToast(id: number) {
    const index = toasts.value.findIndex((t) => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  return {
    toasts,
    showToast,
    removeToast,
  }
}
