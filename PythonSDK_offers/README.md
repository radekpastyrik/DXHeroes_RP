# Offers SDK

An async-first Python SDK for interacting with the Offers API.  
Provides an easy and Pythonic way to obtain&refresh access tokens, register products and manage offers.

---

## Key Features

- **Async/await native** – all API calls are asynchronous.
- **Automatic access token management** – the SDK automatically refreshes short-lived access tokens.
- **Single refresh token usage** – your refresh token is tied to your email and never expires.
- **Full type hints** – for better IDE support and code quality.
- **Comprehensive error handling** – meaningful exceptions for clear error diagnosis.
- **Complete test coverage** – tests written using `pytest` and mocks (unit and integration tests).

---

## Bonus Features
- **Multiple HTTP client support** - supports usage of aiohttp, httpx and requests.
- **Dotenv configuration file support** - uses .env file to load refresh token and base url of API.
- **Packaged SDK for distribution** - generated distribution files via poetry in dist folder (.whl file).
- **TestPyPI** - SDK is published on TestP507yPI, at the moment as pending.

## Installation
Configuration file pyproject.toml in PythonSDK_offers folder, from here you can start all installation.

This SDK requires [Poetry](https://python-poetry.org/) for dependency management.

1. Install Poetry if you haven't already:
pip install poetry

2. Install the project dependencies:
poetry install
- using poetry, SDK is initialized

If still not working, some tips for VS Code:

CTRL+SHIFT+P

Python: Select Interpreter  # insert path to poetry env

You can find path to your env by inserting

poetry env info --path


Example output:
- C:\Users\<user>\AppData\Local\pypoetry\Cache\virtualenvs\offers-riMDfWzY-py3.13

## Distribution 
Distribution files created in dist folder in PythonSDK_offers folder. 

Installing by:

pip install dist/offers-0.1.0-py3-none-any.whl


## Usage
- Initialize AuthManager with auth_url and refresh_token. 
- Call get_access_token() asynchronously to obtain a valid access token. 
- The SDK handles token caching and automatic refresh behind the scenes. 
- By calling client.py methods you can register a new product or get all offers for a specific product defined by UUID. 
- While calling register_product(), offers of the product are automatically created via wrapped Offers API. 
- Example file for SDK usage: PythonSDK_offers/examples/main.py


## Tests
Run tests with:

poetry run pytest

## Requirements
Python with the newest version. Programmed with Python 3.13.2.

Use atleast 3.9.

While working with main.py - update REFRESH_TOKEN in .env file. Kept in here mine for a testing usage - but highly not recommended to share your tokens!
