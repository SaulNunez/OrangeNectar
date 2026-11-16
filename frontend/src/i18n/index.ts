import { i18n } from '@lingui/core'

export const locales = {
  en: 'English',
  es: 'Español',
} as const

export type Locale = keyof typeof locales

export const defaultLocale: Locale = 'en'

const STORAGE_KEY = 'orangenectar.locale'

function isLocale(value: unknown): value is Locale {
  return typeof value === 'string' && value in locales
}

/**
 * Picks the initial locale: a previously chosen one, then the browser's
 * preferred languages, then the default.
 */
export function detectLocale(): Locale {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (isLocale(stored)) return stored
  } catch {
    // Storage can be unavailable (private mode, blocked site data).
  }

  for (const language of navigator.languages ?? [navigator.language]) {
    const base = language.toLowerCase().split('-')[0]
    if (isLocale(base)) return base
  }

  return defaultLocale
}

/**
 * Loads the catalog for `locale` on demand and makes it the active one.
 * The .po file is compiled by @lingui/vite-plugin when imported.
 */
export async function activateLocale(locale: Locale) {
  const { messages } = await import(`../locales/${locale}/messages.po`)
  i18n.loadAndActivate({ locale, messages })
  document.documentElement.lang = locale

  try {
    localStorage.setItem(STORAGE_KEY, locale)
  } catch {
    // Not persisting the choice is fine.
  }
}

export { i18n }
