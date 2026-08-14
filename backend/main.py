from config import Settings
from functools import lru_cache

@lru_cache
def get_settings():
    return Settings()

def main():
    print("Hello from orangenectar!")


if __name__ == "__main__":
    main()
