import os
from shared.utils.token_generator import generate_token

def main():
    api_key = "a68473c2-538d-4ce2-a6df-73e336ffcc36"
    secret_key = "b3ce071200ed73d07600c2201cb529777126ca52bd7c59d6abb4f6fc9338f471"
    token = generate_token(api_key, secret_key)
    
    env_content = f"""VIDEOSDK_API_KEY={api_key}
VIDEOSDK_SECRET_KEY={secret_key}
VIDEOSDK_TOKEN={token}
OPENAI_API_KEY=
"""
    env_path = os.path.join(os.path.dirname(__file__), "../.env")
    with open(env_path, "w") as f:
        f.write(env_content)
    print("Generated .env file successfully.")

if __name__ == "__main__":
    main()
