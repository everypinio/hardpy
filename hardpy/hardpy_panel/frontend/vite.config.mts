import react from "@vitejs/plugin-react";
import type { UserConfig } from "vite";
import glsl from "vite-plugin-glsl";

export default {
  plugins: [react(), glsl()],
  publicDir: 'public',
  server: {
    port: 3000,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        secure: false,
        ws: false,
        configure: (proxy, _options) => {
          proxy.on("error", (err, _req, _res) => {
            console.log("proxy error", err);
          });
          proxy.on("proxyReq", (proxyReq, req, _res) => {
            console.log("PROXY: >>", req.method, req.url);
          });
          proxy.on("proxyRes", (proxyRes, req, _res) => {
            console.log("PROXY: <<", proxyRes.statusCode, req.url);
          });
        },
      },
    },
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