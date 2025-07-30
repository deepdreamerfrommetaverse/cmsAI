// frontend/vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),   // <-- pozwala na "@/lib/api" itp.
    },
  },
  define: {
    // dzięki temu każde `process.env.*` w kodzie nie wywróci bundla
    "process.env": {},
  },
  server: {
    port: 3000,
  },
});
