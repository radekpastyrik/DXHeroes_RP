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
- **Retry logic** - Retry logic implemented for a network failures using exponential backoff.
- **CLI tool** - tool for testing the SDK from command line.
- **Automatic generation of SDK** - using OpenAPI and given .json file there are generated methods to work with API.
- **Synchronous wrapper** - included synchronous wrapper for an asynchronous implementation, running request until completed.
- **TestPyPI** - SDK is published on TestPyPI, at the moment as pending.

## Installation
Configuration file pyproject.toml in PythonSDK_offers folder, from here you can start all installation.

This SDK requires [Poetry](https://python-poetry.org/) for dependency management.

1. Install Poetry if you haven't already:
`pip install poetry`

2. Install the project dependencies:
`poetry install`
- using poetry, SDK is initialized

If still not working, some tips for VS Code:

`CTRL+SHIFT+P`

Python: Select Interpreter  # insert path to poetry env

You can find path to your env by inserting

`poetry env info --path`

Example output:
`C:\Users\<user>\AppData\Local\pypoetry\Cache\virtualenvs\offers-riMDfWzY-py3.13`

3. Set up your .env file:

`REFRESH_TOKEN=your_refresh_token_here`

4. Check example files 

PythonSDK_offers/examples/

and you can run it.

## Distribution - TestPyPI
Published package: [TestPyPI](https://test.pypi.org/project/python_offers_sdk/).

Distribution files created in dist folder in `PythonSDK_offers` folder. 

Publishing by:

`poetry publish -r testpypi --username __token__ --password pypi-<token>`

Note: `poetry version patch` and `poetry build` required before publishing!

Installing by:

`pip install -i https://test.pypi.org/simple/ offers`

Notes: There could happen error with older version of dependencies on TestPyPI. You can call `extra-index-url` to download up-to-date versions from pypi if this error exists

`pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple python_offers_sdk`


## Usage
- Initialize `OffersClient` which automatically initialize `AuthManager` with given `auth_url` and `refresh_token`. 
- Authentication is called automatically when any defined method is called for `OffersClient`.
- The SDK handles token caching and automatic refresh behind the scenes. 
- By calling `OffersClient` methods in `client.py` you can register a new product or get all offers for a specific product defined by UUID. 
- While calling `register_product()`, offers of the product are automatically created via wrapped Offers API. 
- See more example SDK usage: `PythonSDK_offers/examples/main.py`

## CLI usage:
You can easily start a command window in folder `PythonSDK_offers`. 

Installation of poetry (`poetry install`) is firstly required!

From here you can run command line commands e.g.:

- **Register product** - name, description http_client and ID are optional, if not inserted, everything is automatically defined, defaultly used client is httpx.

`poetry run offers register --name "Virtual product" --description "Some virtual product description" --client httpx`

or with id manual specification (ID could be already created, use your own or leave empty!!!):

`poetry run offers register --id 0d7c7424-449a-4531-b33f-d3c2b57e9a23`


- **Get offers from ID** - By the given ID of product, return all offers. Parameter ID is required.

`poetry run offers offers 065464bb-4b72-4583-96d5-74a23ff451d4 --client httpx`

## Automatic SDK generation
There is also included automatic generation of SDK by given OpenAPI generator - `openapi-python-client` is included into pyproject.toml, by poetry installation you can freely generate it yourself.

Go to command line into folder: `./DXHeroes_RP/PythonSDK_offers`. If you did not installed dependencies of the project yet, run:

`poetry install`

then you can generate SDK by:

`poetry run openapi-python-client generate --path openapi.json`

Note: You have to remove old generated SDK (whole folder named as `python-exercise-client`).

If there is needed to use config.yaml file, there is attached one in the `./DXHeroes_RP/PythonSDK_offers` folder.

Example of used automatic SDK located in `examples/automatic_sdk.py`.

## Tests
Run tests with:

`poetry run pytest`

## Requirements
Python with the newest version. Programmed with Python 3.13.2.

Use atleast 3.10.

## Notes
While working with this SDK - update REFRESH_TOKEN in `.env` file. Kept in here mine for a testing usage - but highly not recommended to share your tokens!
