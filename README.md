# DXHeroes_RP
Required task for Applifting/DXHeroes - Offers. Python SDK for Offers API.

This project includes additional inner README.md describing installation, usage and description of the project.

At the moment, there is SDK wrapping Offer API installable by poetry, client and authorization manager are using httpx for interaction with API.

Data models are imported via pydantic. 
Relations between models: Product could have multiple Offers, Offer could have only one Product.


By poetry install in PythonSDK_offers, project will be installed.
