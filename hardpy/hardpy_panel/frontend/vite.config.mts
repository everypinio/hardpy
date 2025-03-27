import react from "@vitejs/plugin-react";
import type { UserConfig } from "vite";
import glsl from "vite-plugin-glsl";

export default {
  plugins: [react(), glsl()],
  publicDir: 'public',
  server: {
    port: 3000,
  },
  define: {
    // By default, Vite doesn't include shims for NodeJS/
    // necessary for segment analytics lib to work
    global: {},
  },
  build: {
    target: 'esnext' //browsers can handle the latest ES features
  }
} satisfies UserConfig;