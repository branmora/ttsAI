# %%
import os
from dotenv import load_dotenv
import yaml
from pathlib import Path

# %% Config function
def load_config():
    # Load environment variables from .env
    base_path = Path(__file__).resolve().parent.parent  # This gets the parent directory of the current script
    env_path = base_path / '.env'

    # Load environment variables from .env
    load_dotenv(dotenv_path=env_path)

    # Specify the path to the config file relative to the script
    config_path = base_path / 'config.yaml'  # Assumes config.yaml is one level up from the script directory

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Replace placeholders in config with environment variables
    for key, value in config.items():
        if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
            env_var_name = value[2:-1]  # Extract the environment variable name
            config[key] = os.getenv(env_var_name, f'NOT FOUND: {env_var_name}')  # Use the environment variable, fallback to the placeholder

    return config

