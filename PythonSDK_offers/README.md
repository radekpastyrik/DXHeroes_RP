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
- **Complete test coverage** – tests written using `pytest` and mocks.

---

## Installation
Configuration file pyproject.toml in PythonSDK_offers folder, from here you can start all installation.

This SDK requires [Poetry](https://python-poetry.org/) for dependency management.

1. Install Poetry if you haven't already:
pip install poetry

2. Install the project dependencies:
poetry install
- using poetry, SDK is initialized

If still not working, some tips for VS Code:

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

## Tests
Run tests with:

pytest 

or 

poetry run pytest
