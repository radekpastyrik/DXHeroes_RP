import asyncio
import click
import os
from dotenv import load_dotenv
from offers_sdk.client import OffersClient, Product, UUID
from offers_sdk.http_clients.requests_client import RequestsClient

load_dotenv()
refresh_token = os.environ.get("REFRESH_TOKEN")
base_url = os.environ.get("BASE_URL")

@click.group()
def cli():
    """CLI tool for Offers SDK"""
    pass

@cli.command()
@click.option('--name', required=False, help="Product name", default="Virtual product")
@click.option('--description', required=False, help="Product description", default="Some virtual product description")
@click.option('--id', required=False, help="Product ID (UUID). Optional.")
@click.option('--client', type=click.Choice(['httpx', 'aiohttp', 'requests']), default='httpx')
@click.option('--hooks_usage', required=False, default=False)
def register(name, description, id, client, hooks_usage):
    """Register a new product (optionally with custom ID)"""
    async def run():
        http_client = resolve_http_client(client)
        sdk = OffersClient(base_url=base_url, 
                           refresh_token=refresh_token, 
                           http_client=http_client, 
                           hooks_usage=hooks_usage)

        product_id = UUID(id) if id else None
        product = await sdk.register_product(name=name, description=description, id=product_id)

        click.echo(f"Registered product:\n {product}")

    asyncio.run(run())


def resolve_http_client(name: str):
    if name == "httpx":
        from offers_sdk.http_clients.httpx_client import HTTPXClient
        return HTTPXClient()
    elif name == "aiohttp":
        from offers_sdk.http_clients.aiohttp_client import AioHTTPClient
        return AioHTTPClient()
    else:
        from offers_sdk.http_clients.requests_client import RequestsClient
        return RequestsClient()


@cli.command()
@click.argument('product_id')
@click.option('--client', type=click.Choice(['httpx', 'aiohttp', 'requests']), default='httpx')
@click.option('--hooks_usage', required=False, default=False)
def offers(product_id, client, hooks_usage):
    """Get offers for a product"""
    async def run():
        http_client = resolve_http_client(client)
        sdk = OffersClient(base_url=base_url, 
                           refresh_token=refresh_token, 
                           http_client=http_client,
                           hooks_usage=hooks_usage)
        offers = await sdk.get_offers(product_id=product_id)
        for offer in offers:
            click.echo(f"Received offer: {offer}")

    asyncio.run(run())


if __name__ == '__main__':
    cli()
