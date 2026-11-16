import { useState } from 'react'
import {
  Box,
  Button,
  Container,
  Group,
  Radio,
  Stack,
  Text,
  Title,
} from '@mantine/core'
import { msg } from '@lingui/core/macro'
import type { MessageDescriptor } from '@lingui/core'
import { Trans, useLingui } from '@lingui/react/macro'
import LanguageSwitcher from './LanguageSwitcher'

type ExportFormat = 'csv' | 'html' | 'xlsx'

const formatOptions: {
  value: ExportFormat
  label: string
  description: MessageDescriptor
}[] = [
  {
    value: 'csv',
    label: 'CSV',
    description: msg`A plain spreadsheet file — opens in Excel, Sheets, or Numbers.`,
  },
  {
    value: 'html',
    label: 'HTML',
    description: msg`A single browsable page you can open straight in your browser.`,
  },
  {
    value: 'xlsx',
    label: 'XLSX',
    description: msg`An Excel workbook, formatted and ready to filter or sort.`,
  },
]

function ExportFormatPage() {
  const { i18n } = useLingui()
  const [format, setFormat] = useState<ExportFormat>('csv')
  const formatLabel = format.toUpperCase()

  // TODO: call the backend /export endpoint with the selected format
  // once the Reddit OAuth flow supplies the user's saved posts.
  const handleExport = () => {
    console.log('TODO: export saved posts as', format)
  }

  return (
    <Box style={{ minHeight: '100svh', display: 'flex', flexDirection: 'column' }}>
      <Box
        component="header"
        style={(theme) => ({
          borderBottom: `1px solid ${theme.colors.gray[2]}`,
        })}
      >
        <Container size="lg" py="md">
          <Group justify="space-between">
            <Text size="xl" fw={700}>
              🍊 OrangeNectar
            </Text>
            <LanguageSwitcher />
          </Group>
        </Container>
      </Box>

      <Box component="main" style={{ flexGrow: 1 }}>
        <Container size="xs" py={80}>
          <Stack gap="xl">
            <Stack gap={4}>
              <Title order={2}>
                <Trans>Choose an export format</Trans>
              </Title>
              <Text c="dimmed">
                <Trans>
                  Pick how you&apos;d like your saved posts and comments
                  packaged up.
                </Trans>
              </Text>
            </Stack>

            <Radio.Group
              value={format}
              onChange={(value) => setFormat(value as ExportFormat)}
            >
              <Stack gap="sm">
                {formatOptions.map((option) => (
                  <Radio.Card key={option.value} value={option.value} p="md" radius="md">
                    <Group wrap="nowrap" align="flex-start">
                      <Radio.Indicator />
                      <div>
                        <Text fw={600}>{option.label}</Text>
                        <Text size="sm" c="dimmed">
                          {i18n._(option.description)}
                        </Text>
                      </div>
                    </Group>
                  </Radio.Card>
                ))}
              </Stack>
            </Radio.Group>

            <Button color="orange" radius="xl" onClick={handleExport}>
              <Trans>Export as {formatLabel}</Trans>
            </Button>
          </Stack>
        </Container>
      </Box>
    </Box>
  )
}

export default ExportFormatPage
