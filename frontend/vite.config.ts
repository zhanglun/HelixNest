import path from "path";
import dns from "node:dns";

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

dns.setDefaultResultOrder("verbatim");

// https://vitejs.dev/config/
export default defineConfig({
  // server: {
  //   host: "127.0.0.1",
  //   port: 5173,
  // },
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
