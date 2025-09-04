import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { VitePWA } from 'vite-plugin-pwa'
import svgLoader from 'vite-svg-loader'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    svgLoader(),
    VitePWA({ 
      registerType: 'autoUpdate',
      devOptions: {
        enabled: true
      },
      includeAssets: ['favicon.ico', 'apple-touch-icon.png', 'mask-icon.svg'],
      manifest: {
        name: 'VisioAgro',
        short_name: 'VisioAgro',
        description: 'Mindfulness',
        theme_color: '#FF9900',
        /**
        icons: [
          {
            src: 'android-icon-192x192.png',
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: 'android-icon-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          },
          {
            src: 'android-icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any'
          },
          {
            src: 'android-icon-512x512.png',
            sizes: '512x512',
            type: 'image/png',
            purpose: 'maskable'
          }
        ]
         */
      }
    })
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  optimizeDeps: {
    include: ["fast-deep-equal"],
  },
  server: {
    host: true,
  },
});
