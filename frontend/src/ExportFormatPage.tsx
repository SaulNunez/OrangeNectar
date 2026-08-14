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

type ExportFormat = 'csv' | 'html'

const formatOptions: { value: ExportFormat; label: string; description: string }[] = [
  {
    value: 'csv',
    label: 'CSV',
    description: 'A plain spreadsheet file — opens in Excel, Sheets, or Numbers.',
  },
  {
    value: 'html',
    label: 'HTML',
    description: 'A single browsable page you can open straight in your browser.',
  },
]

function ExportFormatPage() {
  const [format, setFormat] = useState<ExportFormat>('csv')

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
          <Text size="xl" fw={700}>
            🍊 OrangeNectar
          </Text>
        </Container>
      </Box>

      <Box component="main" style={{ flexGrow: 1 }}>
        <Container size="xs" py={80}>
          <Stack gap="xl">
            <Stack gap={4}>
              <Title order={2}>Choose an export format</Title>
              <Text c="dimmed">
                Pick how you&apos;d like your saved posts and comments packaged up.
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
                          {option.description}
                        </Text>
                      </div>
                    </Group>
                  </Radio.Card>
                ))}
              </Stack>
            </Radio.Group>

            <Button color="orange" radius="xl" onClick={handleExport}>
              Export as {format.toUpperCase()}
            </Button>
          </Stack>
        </Container>
      </Box>
    </Box>
  )
}

export default ExportFormatPage
