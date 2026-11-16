import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { lingui } from '@lingui/vite-plugin'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // Compiles .po catalogs on import and transforms Lingui macros natively,
    // so no Babel/SWC plugin or separate `lingui compile` step is needed.
    lingui({ macroTransform: true }),
  ],
})
