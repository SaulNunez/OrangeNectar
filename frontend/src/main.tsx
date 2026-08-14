import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { MantineProvider, createTheme } from '@mantine/core'
import '@mantine/core/styles.css'
import './index.css'
import App from './App.tsx'
import ExportFormatPage from './ExportFormatPage.tsx'

const theme = createTheme({
  primaryColor: 'orange',
  defaultRadius: 'md',
  fontFamily:
    'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
  headings: {
    fontFamily:
      'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider theme={theme} defaultColorScheme="auto">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />} />
          {/* Not yet linked from the UI — will be reachable after Reddit login is wired up. */}
          <Route path="/export" element={<ExportFormatPage />} />
        </Routes>
      </BrowserRouter>
    </MantineProvider>
  </StrictMode>,
)
