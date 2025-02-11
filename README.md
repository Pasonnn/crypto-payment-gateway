# CryptoPay - Local Development Setup

CryptoPay is a cryptocurrency payment gateway that allows you to accept cryptocurrency payments on your website. This guide will help you set up the project locally for development.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- [Node.js](https://nodejs.org/) (v14 or higher)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [MongoDB](https://www.mongodb.com/) (for the database)
- [Python](https://www.python.org/) (for the backend, if applicable)

## Getting Started

Follow these steps to set up the project locally:

### 1. Clone the Repository

Clone the CryptoPay repository to your local machine:

```bash
git clone https://github.com/Pasonnn/crypto-payment-gateway.git
cd crypto-payment-gateway
```

### 2. Set Up the Backend

#### 2.1. Navigate to the Backend Directory

```bash
cd backend
```

#### 2.2. Install Dependencies

Install the required packages:

```bash
npm install
```

#### 2.3. Create Environment Variables

Create a `.env` file in the backend directory and add the following variables:

```env
# Infura Ethereum Node API Key
INFURA_SEPOLIA_URL="https://sepolia.infura.io/v3/YOUR_INFURA_API_KEY"

# Flask Secret Key
SECRET_KEY="your_secure_random_key_here"

# Database Configuration (MongoDB)
DATABASE_URI="mongodb+srv://your_username:your_password@your_cluster.mongodb.net"
DATABASE_NAME="your_database_name"

# Admin Wallet Address
ADMIN_WALLET_ADDRESS="your_ethereum_wallet_address"
```

#### 2.4. Start the Backend Server

Run the backend server:

```bash
npm start
```

### 3. Set Up the Frontend

#### 3.1. Navigate to the Frontend Directory

Open a new terminal window and navigate to the frontend directory:

```bash
cd frontend
```

#### 3.2. Install Dependencies

Install the required packages:

```bash
npm install
```

#### 3.3. Create Environment Variables

Create `.env.development` and `.env.production` files in the frontend directory:

`.env.development`:

```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=ws://localhost:5000
```

`.env.production`:

```env
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_WS_URL=wss://your-backend-domain.com
```

#### 3.4. Start the Frontend Server

Run the frontend server:

```bash
npm start
```

### 4. Access the Application

Once both the backend and frontend servers are running, you can access the application in your web browser at:

```
http://localhost:3000
```

## Contributing

If you would like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For any issues or questions, please reach out via [GitHub Issues](https://github.com/Pasonnn/crypto-payment-gateway/issues) or email pason,dev@gmail.com.
