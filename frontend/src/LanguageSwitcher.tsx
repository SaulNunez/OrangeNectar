import { SegmentedControl } from '@mantine/core'
import { useLingui } from '@lingui/react/macro'
import { activateLocale, locales, type Locale } from './i18n'

function LanguageSwitcher() {
  const { i18n, t } = useLingui()

  return (
    <SegmentedControl
      size="xs"
      radius="xl"
      aria-label={t`Language`}
      value={i18n.locale}
      onChange={(value) => void activateLocale(value as Locale)}
      data={Object.entries(locales).map(([value, label]) => ({ value, label }))}
    />
  )
}

export default LanguageSwitcher
