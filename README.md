# DXHeroes_RP
Required task for Applifting/DXHeroes - Offers. Python SDK for Offers API.

This project includes additional inner README.md describing installation, usage and description of the project.

At the moment, there is SDK wrapping Offer API installable by poetry. 
Client and authorization manager are defaultly using httpx (you can choose aiohttp or requests yet) for interaction with API.

Data models are imported via pydantic. 

Relations between models: Product could have multiple Offers, Offer could have only one Product.

By poetry install in PythonSDK_offers, project will be installed.

Project also published on [TestPyPI](https://test.pypi.org/project/python_offers_sdk/).

You can also test SDK by using CLI tool while running in PythonSDK_offers (poetry install required).

In the main folder, there is also file work_load.txt to see some approximately time spent on the task.

Task specification is at root folder in .html format: './DXHeros_RP/Applifting Python task.html'.

For more usage, read inner README.md.
