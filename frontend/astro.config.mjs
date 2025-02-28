import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

// https://astro.build/config
export default defineConfig({
  integrations: [
    react(),
    tailwind({
      // Configuración de Tailwind
      config: { path: './tailwind.config.mjs' }
    })
  ],
  output: 'static',
  build: {
    assets: 'assets'
  }
});
