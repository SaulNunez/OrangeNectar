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
import { REDDIT_LOGIN_URL } from './api'

function RedditLoginButton({ size = 'md' }: { size?: 'md' | 'lg' }) {
  const handleRedditLogin = () => {
    // Full browser navigation, not a fetch: the backend responds with a
    // redirect to Reddit's authorization page that the browser must follow.
    window.location.href = REDDIT_LOGIN_URL
  }

  return (
    <Button size={size} color="orange" radius="xl" onClick={handleRedditLogin}>
      Log in with Reddit
    </Button>
  )
}

const features = [
  {
    title: 'One-click export',
    description:
      'Grab everything you’ve saved on Reddit and download it in a single request.',
  },
  {
    title: 'CSV today, more formats soon',
    description:
      'Start with a clean CSV file, with JSON and other formats on the way.',
  },
  {
    title: 'Nothing stored, nothing tracked',
    description:
      'Your saved posts pass straight through to your download — we don’t keep a copy.',
  },
]

function App() {
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
            <RedditLoginButton />
          </Group>
        </Container>
      </Box>

      <Box component="main" style={{ flexGrow: 1 }}>
        <Container size="sm" py={80}>
          <Stack align="center" gap="lg" ta="center">
            <Title order={1} fz={{ base: 36, sm: 48 }} fw={800}>
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
            </Title>
            <Text size="lg" c="dimmed" maw={520}>
              Connect your Reddit account and export everything you&apos;ve
              saved &mdash; posts and comments &mdash; into a CSV you can
              actually use.
            </Text>
            <RedditLoginButton size="lg" />
            <Text size="sm" c="dimmed">
              We only ask for read access to your saved items.
            </Text>
          </Stack>
        </Container>

        <Container size="lg" pb={80}>
          <SimpleGrid cols={{ base: 1, sm: 3 }} spacing="lg">
            {features.map((feature) => (
              <Card key={feature.title} padding="lg" radius="md" withBorder>
                <Text fw={600} mb={4}>
                  {feature.title}
                </Text>
                <Text size="sm" c="dimmed">
                  {feature.description}
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
            OrangeNectar isn&apos;t affiliated with Reddit, Inc.
          </Text>
        </Container>
      </Box>
    </Box>
  )
}

export default App
