import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { MantineProvider, createTheme } from '@mantine/core'
import { I18nProvider } from '@lingui/react'
import '@mantine/core/styles.css'
import './index.css'
import App from './App.tsx'
import ExportFormatPage from './ExportFormatPage.tsx'
import { activateLocale, detectLocale, i18n } from './i18n'

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

// Load the user's catalog before the first render so the page never flashes
// untranslated text.
await activateLocale(detectLocale())

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <I18nProvider i18n={i18n}>
      <MantineProvider theme={theme} defaultColorScheme="auto">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<App />} />
            {/* Not yet linked from the UI — will be reachable after Reddit login is wired up. */}
            <Route path="/export" element={<ExportFormatPage />} />
          </Routes>
        </BrowserRouter>
      </MantineProvider>
    </I18nProvider>
  </StrictMode>,
)
