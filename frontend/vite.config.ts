import { defineConfig, normalizePath, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";
import { createRequire } from "node:module";
import { viteStaticCopy } from "vite-plugin-static-copy";

const require = createRequire(import.meta.url);
const cMapDir = normalizePath(
  path.join(path.dirname(require.resolve("pdfjs-dist/package.json")), "cmaps")
);
const standardFontsDir = normalizePath(
  path.join(
    path.dirname(require.resolve("pdfjs-dist/package.json")),
    "standard_fonts"
  )
);

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env variables based on the current mode
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [
      react(),
      viteStaticCopy({
        targets: [
          { src: cMapDir, dest: "" },
          { src: standardFontsDir, dest: "" },
        ],
      }),
    ],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src')
      },
    },
    define: {
      "process.env": {
        API_URL: env.VITE_API_URL,
        API_WISEMAN_URL: env.VITE_WISEMAN_API_URL,
        AUTH_SERVICE_URL: env.VITE_AUTH_SERVICE_URL,
      },
    },
    server: {
      host: "0.0.0.0",
      port: 3000,
      open: true,
      proxy: {
        // Proxy setting for the API requests
        '/api': {
          target: env.VITE_API_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        },
        '/wise': {
          target: env.VITE_WISEMAN_API_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/wise/, '')
        },
      },
    },
  };
});