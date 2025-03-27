import react from "@vitejs/plugin-react";
import type { UserConfig } from "vite";
import glsl from "vite-plugin-glsl";

export default {
  plugins: [react(), glsl()],
  publicDir: 'public',
  server: {
    port: 3000,
  },
} satisfies UserConfig;