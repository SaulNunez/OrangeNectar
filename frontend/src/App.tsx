import {
  Box,
  Button,
  Card,
  Container,
  Group,
  SimpleGrid,
  Stack,
  Text,
  Title,
} from '@mantine/core'
import { msg } from '@lingui/core/macro'
import { Trans, useLingui } from '@lingui/react/macro'
import { REDDIT_LOGIN_URL } from './api'
import LanguageSwitcher from './LanguageSwitcher'

function RedditLoginButton({ size = 'md' }: { size?: 'md' | 'lg' }) {
  const handleRedditLogin = () => {
    // Full browser navigation, not a fetch: the backend responds with a
    // redirect to Reddit's authorization page that the browser must follow.
    window.location.href = REDDIT_LOGIN_URL
  }

  return (
    <Button size={size} color="orange" radius="xl" onClick={handleRedditLogin}>
      <Trans>Log in with Reddit</Trans>
    </Button>
  )
}

// Defined with `msg` so they can live outside a component; they're translated
// at render time with `i18n._()`.
const features = [
  {
    id: 'one-click',
    title: msg`One-click export`,
    description: msg`Grab everything you’ve saved on Reddit and download it in a single request.`,
  },
  {
    id: 'formats',
    title: msg`CSV today, more formats soon`,
    description: msg`Start with a clean CSV file, with JSON and other formats on the way.`,
  },
  {
    id: 'privacy',
    title: msg`Nothing stored, nothing tracked`,
    description: msg`Your saved posts pass straight through to your download — we don’t keep a copy.`,
  },
]

function App() {
  const { i18n } = useLingui()

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
            <Group gap="xs">
              <Text size="xl" fw={700}>
                🍊 OrangeNectar
              </Text>
            </Group>
            <Group gap="sm">
              <LanguageSwitcher />
              <RedditLoginButton />
            </Group>
          </Group>
        </Container>
      </Box>

      <Box component="main" style={{ flexGrow: 1 }}>
        <Container size="sm" py={80}>
          <Stack align="center" gap="lg" ta="center">
            <Title order={1} fz={{ base: 36, sm: 48 }} fw={800}>
              <Trans>
                Take your Reddit{' '}
                <Text
                  component="span"
                  inherit
                  variant="gradient"
                  gradient={{ from: 'orange', to: 'yellow' }}
                >
                  Saved
                </Text>{' '}
                posts with you
              </Trans>
            </Title>
            <Text size="lg" c="dimmed" maw={520}>
              <Trans>
                Connect your Reddit account and export everything you&apos;ve
                saved &mdash; posts and comments &mdash; into a CSV you can
                actually use.
              </Trans>
            </Text>
            <RedditLoginButton size="lg" />
            <Text size="sm" c="dimmed">
              <Trans>We only ask for read access to your saved items.</Trans>
            </Text>
          </Stack>
        </Container>

        <Container size="lg" pb={80}>
          <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="lg">
            {features.map((feature) => (
              <Card key={feature.id} padding="lg" radius="md" withBorder>
                <Text fw={600} mb={4}>
                  {i18n._(feature.title)}
                </Text>
                <Text size="sm" c="dimmed">
                  {i18n._(feature.description)}
                </Text>
              </Card>
            ))}
          </SimpleGrid>
        </Container>
      </Box>

      <Box
        component="footer"
        style={(theme) => ({
          borderTop: `1px solid ${theme.colors.gray[2]}`,
        })}
      >
        <Container size="lg" py="md">
          <Text size="sm" c="dimmed" ta="center">
            <Trans>OrangeNectar isn&apos;t affiliated with Reddit, Inc.</Trans>
          </Text>
        </Container>
      </Box>
    </Box>
  )
}

export default App
