import { QueryClient, VueQueryPlugin } from "@tanstack/vue-query"
import { createApp } from "vue"
import "./style.css"
import App from "./App.vue"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

console.log("🚀 Initializing Vue app...")

const app = createApp(App)
app.use(VueQueryPlugin, { queryClient })
app.mount("#app")

console.log("✅ App mounted successfully")
