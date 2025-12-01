import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [tailwindcss()],
  server: {
    cors: {
      origin: "http://localhost:8000",
    },
  },
  build: {
    manifest: true,
    rollupOptions: {
      input: ["src/main.ts", "src/style.css"],
    },
  },
});
