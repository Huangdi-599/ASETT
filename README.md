# Ayulla Crypto Portfolio Management API
This API allows users to manage their crypto-currency portfolios. It utilizes API calls to coingecko or any other cryptocurrency API to gather data that will be used to implement the necessary functionalities and additional features.

## Features
- User Authentication:
    Users can sign up, log in, and log out of the system
    Password recovery features are available
    Passwords are securely stored and hashed using Django's built-in authentication system
- Referral System:
    Users can invite other users to join the platform using a referral link
    Referral links are tracked, and the referrer receives a bonus when a new user signs up using their link
- Portfolio Management:
    A user can create wallets/portfolios
    Users can add and remove cryptocurrencies to their wallet/porfolio
    Each cryptocurrency has a name, symbol, current price, and quantity which the user can add to their portfolio
    Users can see a detail view of their portfolio, which shows the value of each cryptocurrency in their wallet and the total value of their portfolio
- Crypto Data:
    The homepage shows the 24-hour price and percentage change of the top 10 ranked cryptocurrencies
    It also includes the 24-hour price and percentage change of the currencies in the user’s portfolio
    A search bar is available where users can search for new cryptocurrencies to add to their portfolio

## Testing
This API was built using a TDD approach. Tests were written for each feature before coding began, with a goal of achieving at least 80% test coverage.

## Installation
To run this API locally, follow these steps:

- Clone the repository
- create a virtual env with `virtualenv env`
- Activate your virtual environment with `./activate`
- Install dependencies with `pip install -r requirements.txt`
- Run database migrations with `python manage.py migrate`
- Start the server with `python manage.py runserver`


## Authentication
To access the API, users must be authenticated with a valid API key, which can be obtained by registering for an account on the platform.

## Endpoint Documentation

- `POST /api/signup/`
Creates a new user account.

>Request Body:
```
{
    'username': 'testuser',
    'email': 'testuser@example.com',
    'password': 'testpassword123',
    'password2': 'testpassword123',
    'first_name': 'Test',
    'last_name': 'User'
}
```

>Response:
```
```

- `POST /api/login/`
Logs a user in to the platform.

>Request Body:
```
{
    "username":"Huangdi",
    "password":"staff123"
}
```

>Response:
token (string): A JSON Web Token (JWT) that can be used to authenticate subsequent API calls.
```
```
- `POST /api/password-reset/`
Sends a password reset email to the specified user.

>Request Body:
email (string, required): The email address of the user.
```
{
    "email": ""
}
```

>Response:
```
{
    "email": ""
}

```


- `POST /api/password-reset/confirm/`
Confirms a password reset request with a token.

>Request Body:
token (string, required): The token sent in the password reset email.
password (string, required): The user's desired new password.
```
{
    "token": "",
    "password": "",
    "password_confirm": ""
}
```

>Response:
```
{
    "detail": "Password reset successful."
}
```

POST /api/logout/
Logs the current user out of the platform.


- `POST /api/portfolios/`
    Create a portfolio for the current user.

>Request Body:
    name: the name of the portfoilio or wallet
    description : portfoilio description
```
{
    "name": "My Holdings",
    "description": "Hodl Coins"
}
```
>Response:
```
{
    "id": 2,
    "name": "My Holdings",
    "description": "Hodl Coins",
    "user": {
        "id": 1,
        "username": "admin"
    },
    "portfolio_crypto": [],
    "total_value": 0
}

```
- `POST /api/portfolios/2/add-crypto`
    Add a crypto that is to particular portfolio.
>Request Body:
    crypto_id : is the id of a crypto is already the database
    quantity: is the amount of value of that crypto a user want to add
{
    "crypto_id":4,
    "quantity": 2.666
}
>Response:
```
{
        "id": 2,
        "name": "My Holdings",
        "description": "Hodl Coins",
        "user": {
            "id": 1,
            "username": "admin"
        },
        "portfolio_crypto": [
            {
                "crypto": {
                    "id": 4,
                    "name": "Ethereum",
                    "symbol": "eth",
                    "price": "1990.8600000000",
                    "market_cap": 239484199353,
                    "percentage_change": "6.2919600000"
                },
                "quantity": "2.6660000000",
                "value": "5307.6327600000"
            }
        ],
        "total_value": 5307.63276
    }
]

```




- `GET /api/portfolios/1`
Retrieves the current user's crypto portfolio by its id.

>Request Body:
N/A

>Response:
```
[
    {
        "id": 1,
         "name": "My Holdings",
        "description": "Hodl Coins"
        "user": {
            "id": 1,
            "username": "admin"
        },
        "portfolio_crypto": [
            {
                "crypto": {
                    "id": 1,
                    "name": "TrueUSD",
                    "symbol": "tusd",
                    "price": "0.9996480000",
                    "market_cap": 2041488435,
                    "percentage_change": "-0.0176700000"
                },
                "quantity": "2.0000000000",
                "value": "1.9992960000"
            },
            {
                "crypto": {
                    "id": 2,
                    "name": "VeChain",
                    "symbol": "vet",
                    "price": "0.0248134000",
                    "market_cap": 1798517409,
                    "percentage_change": "2.5289700000"
                },
                "quantity": "2.0000000000",
                "value": "0.0496268000"
            }
        ],
        "total_value": 2.0489228
    }
]
```


`DELETE /api/portfolios/1/remove-crypto/3/`
    Removes a cryptocurrency from the user's portfolio
    it takes the portfolio id and the id of the crypto to be remove
    







