# Crypto Payment Service Backend

This backend service provides a RESTful API for managing cryptocurrency payments and user accounts. It is built using Flask and integrates with a blockchain network to facilitate transactions.

## Table of Contents

- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [Payment Service Endpoints](#payment-service-endpoints)
  - [User Service Endpoints](#user-service-endpoints)
- [Health Check](#health-check)
- [Contributing](#contributing)
- [License](#license)

## Features

- Create and manage cryptocurrency payment requests.
- Update payment statuses and handle fund distribution.
- User registration, authentication, and profile management.
- Admin functionalities for user management.

## Technologies

- Python 3.x
- Flask
- Flask-RESTful
- Web3.py (for Ethereum interactions)
- MongoDB (or any other database for user and payment data)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/crypto-payment-service.git
   cd crypto-payment-service/backend
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables (e.g., database connection, API keys):
   ```bash
   export DATABASE_URL='your_database_url'
   export ADMIN_WALLET_ADDRESS='your_admin_wallet_address'
   export ADMIN_PRIVATE_KEY='your_admin_private_key'
   ```

## Usage

1. Start the Flask application:

   ```bash
   flask run
   ```

2. The application will be available at `http://localhost:5000`.

## API Endpoints

### Payment Service Endpoints

- **Health Check**

  - `GET /api/payments/health`
  - Returns the status of the payment service.

- **Create Payment**

  - `POST /api/payments/create_payment`
  - Input: `{ "api_key": "string", "amount": float, "currency": "string" }`
  - Output: `{ "eth_amount": float, "payment_address": "string" }`

- **Update Payment Status**

  - `PUT /api/payments/update_payment_status`
  - Input: `{ "payment_address": "string", "api_key": "string" }`
  - Output: `{ "status": "string" }`

- **Get Payment Status**

  - `GET /api/payments/payment_status`
  - Input: Query parameter `payment_address`
  - Output: `{ "status": "string" }`

- **Get Timeout for Payment**
  - `PUT /api/payments/timeout`
  - Input: `{ "payment_address": "string", "api_key": "string" }`
  - Output: `{ "status": "string" }`

### User Service Endpoints

- **Health Check**

  - `GET /api/users/health`
  - Returns the status of the user service.

- **User Registration**

  - `POST /api/users/register`
  - Input: `{ "username": "string", "email": "string", "password": "string" }`
  - Output: `{ "message": "string" }`

- **User Login**

  - `POST /api/users/login`
  - Input: `{ "email": "string", "password": "string" }`
  - Output: `{ "status": "string", "token": "string" }`

- **Get User Profile**

  - `GET /api/users/profile`
  - Output: User profile details.

- **Get Current User API Key**

  - `GET /api/users/api_key`
  - Output: `{ "api_key": "string" }`

- **Regenerate API Key**

  - `POST /api/users/regenerate_api_key`
  - Output: `{ "message": "string", "api_key": "string" }`

- **Edit User Profile**

  - `PUT /api/users/edit`
  - Input: `{ "username": "string", "password": "string" }`
  - Output: `{ "message": "string" }`

- **Delete User**

  - `DELETE /api/users/delete`
  - Output: `{ "message": "string" }`

- **Update Wallet Address**

  - `PUT /api/users/update_wallet`
  - Input: `{ "wallet_address": "string" }`
  - Output: `{ "message": "string" }`

- **Get User Dashboard**

  - `GET /api/users/dashboard`
  - Output: Dashboard data.

- **Get User Transactions**
  - `GET /api/users/transactions`
  - Output: List of transactions.

### Admin Routes

- **Get All Users**

  - `GET /api/admin/users`
  - Output: List of users.

- **Get Specific User**

  - `GET /api/admin/users/<user_id>`
  - Output: User details.

- **Delete Specific User**
  - `DELETE /api/admin/users/<user_id>`
  - Output: `{ "message": "string" }`

## Health Check

You can check the health of both the payment and user services by accessing the respective health check endpoints.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
