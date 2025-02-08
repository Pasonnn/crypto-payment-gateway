# Crypto Payment Service

This project is a cryptocurrency payment service that includes a backend API for managing payments and user accounts. The application is designed to facilitate cryptocurrency transactions and user management.

## Project Structure

```
crypto-payment-service/
│
├── backend/                # Backend service (Flask API)
│   ├── payment_service/    # Payment service module
│   ├── user_service/       # User service module
│   ├── requirements.txt     # Python dependencies
│   └── ...                 # Other backend files
│
├── frontend/               # Frontend application (TBD)
│   └── ...                 # Frontend files and structure
│
└── README.md               # Project overview and setup instructions
```

## Backend

The backend service is built using Flask and provides a RESTful API for managing cryptocurrency payments and user accounts.

### Features

- Create and manage cryptocurrency payment requests.
- User registration, authentication, and profile management.
- Admin functionalities for user management.

### Installation

1. Navigate to the backend directory:

   ```bash
   cd backend
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

5. Start the Flask application:
   ```bash
   flask run
   ```

### API Documentation

Refer to the `backend/README.md` for detailed API endpoints and usage instructions.

## Frontend

The frontend application is currently under development. It will provide a user interface for interacting with the backend services.

### Setup Instructions

(TBD - Add instructions for setting up the frontend once it's developed)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
