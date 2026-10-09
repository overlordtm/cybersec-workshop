import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';
import { handout } from './shared/handout.js';

export default defineConfig({
  // Relative asset URLs support both project Pages and custom domains.
  base: './',
  plugins: [handout()],
  build: {
    rolldownOptions: {
      input: {
        home: fileURLToPath(new URL('./index.html', import.meta.url)),
        'cybersec-101': fileURLToPath(new URL('./cybersec-101/index.html', import.meta.url)),
        'cybersec-101-vaje': fileURLToPath(new URL('./cybersec-101/vaje/index.html', import.meta.url)),
        'cybersec-201': fileURLToPath(new URL('./cybersec-201/index.html', import.meta.url)),
      },
    },
  },
});
