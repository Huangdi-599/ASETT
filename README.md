use virtual env 
then install all package in requirements.txt

Sure, here are the request bodies for each view:

Create Portfolio View:

Request Method: POST

Endpoint: /portfolios/

Request Body:

json
Copy code
{
  "name": "My Portfolio",
  "description": "A portfolio of my favorite cryptocurrencies",
  "cryptos": []
}
Notes:

The name and description fields are required.
The cryptos field is optional and can be left empty.
If you want to add Crypto objects to the Portfolio, you will need to use the Add Crypto View after creating the Portfolio.
Add Crypto View:

Request Method: PUT

Endpoint: /portfolios/<portfolio_id>/

Request Body:

json
Copy code
{
  "name": "My Portfolio",
  "description": "A portfolio of my favorite cryptocurrencies",
  "cryptos": [
    {
      "id": 1,
      "name": "Bitcoin",
      "symbol": "BTC",
      "price": 55000,
      "quantity": 1.5
    },
    {
      "id": 2,
      "name": "Ethereum",
      "symbol": "ETH",
      "price": 2000,
      "quantity": 3.2
    }
  ]
}
Notes:

The id field for each Crypto object is required and must correspond to an existing Crypto object in the database.
The name, symbol, price, and quantity fields are read-only and should not be included in the request body. They will be populated automatically based on the id field.
You can add or remove Crypto objects from the Portfolio by including or excluding them from the cryptos list.
Crypto View:

Request Method: GET

Endpoint: /cryptos/

Request Body: N/A

Notes: