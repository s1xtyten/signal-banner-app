import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

export default defineConfig({
    plugins: [svelte()],
    server: {
        host: true,  // Changed from '127.0.0.1' to true to allow all network access
        port: 5173,
        strictPort: true
    },
    css: {
        postcss: './postcss.config.cjs'
    }
})