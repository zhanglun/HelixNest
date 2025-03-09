import path from "path";

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  resolve: {
    alias: {
      "framer-motion": path.resolve(__dirname, "node_modules/framer-motion"),
      "tailwindcss/plugin.js": path.resolve(
        __dirname,
        "node_modules/tailwindcss/plugin.js",
      ),
    },
  },
  build: {
    rollupOptions: {
      external: ["framer-motion", "tailwindcss/plugin.js"],
    },
  },
});
