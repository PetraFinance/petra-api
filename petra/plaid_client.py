from plaid import Client

from petra.config import config

Client.config({
    'url': 'https://tartan.plaid.com'
})

client = Client(
    client_id=config['PLAID']['CLIENT_ID'],
    secret=config['PLAID']['SECRET'],
)
