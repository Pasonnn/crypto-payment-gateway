# 🚀 Crypto Payment Gateway

## 📌 Project Overview

This project is a **Crypto Payment Gateway** that enables users to make payments using cryptocurrencies like **Bitcoin, Ethereum, and USDT**. It provides a secure and decentralized way for merchants to accept crypto transactions.

## 📂 Project Structure

```
crypto-payment-gateway/
│── backend/                    # Flask Backend
│   ├── app.py                  # Main Flask app
│   ├── config.py               # Configuration settings
│   ├── blockchain/             # Blockchain payment handling
│   │   ├── web3_utils.py       # Ethereum payment processing
│   │   ├── bitcoin_utils.py    # Bitcoin payment processing
│   ├── database/               # Database models and storage
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── db_init.py          # Database initialization
│   ├── routes/                 # API Endpoints
│   │   ├── payment_routes.py   # Payment processing API
│   │   ├── user_routes.py      # User-related API
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│
│── frontend/                    # React Frontend
│   ├── src/                      # React source code
│   │   ├── components/           # UI components
│   │   │   ├── PaymentForm.js    # Crypto payment form
│   │   │   ├── SuccessPage.js    # Payment success page
│   │   │   ├── Transactions.js   # Transaction history
│   │   ├── pages/                # Page components
│   │   │   ├── Home.js           # Home page
│   │   │   ├── Checkout.js       # Crypto checkout
│   │   ├── utils/                # Utility functions
│   │   │   ├── api.js            # API calls to Flask backend
│   │   │   ├── cryptoUtils.js    # Crypto conversion functions
│   │   ├── App.js                # Main React app
│   │   ├── index.js              # React entry point
│   ├── package.json              # React dependencies
│   ├── .env                      # Environment variables
│
│── database/                     # Database files
│   ├── payments.db                # SQLite database
│   ├── migrations/                 # Database migrations
│
│── scripts/                       # Deployment Scripts
│   ├── deploy.sh                   # Deployment script
│   ├── start_server.sh              # Start server script
│
│── .gitignore                      # Git ignore settings
│── README.md                        # Project Documentation
│── docker-compose.yml               # Docker configuration
│── LICENSE                          # License
```

## 🛠️ Technologies Used

### 🔹 Backend:

- **Flask (Python)** – API handling
- **Web3.py** – Ethereum blockchain integration
- **BlockCypher API** – Bitcoin transactions
- **PostgreSQL/SQLite** – Database for storing transactions
- **SQLAlchemy** – ORM for database interaction

### 🔹 Frontend:

- **React.js** – UI development
- **Axios** – API communication
- **Bootstrap/Tailwind CSS** – UI styling

### 🔹 Deployment & DevOps:

- **Docker** – Containerized deployment
- **Gunicorn** – Production WSGI server for Flask
- **Nginx** – Reverse proxy

## 📌 Features

✔️ Accepts **Bitcoin & Ethereum** payments
✔️ **Generates unique wallet addresses** for transactions
✔️ Monitors **blockchain confirmations**
✔️ Sends payment **notifications** to merchants
✔️ **React-based checkout UI**
✔️ **Flask REST API** for payment processing
✔️ Database stores **transaction history**
✔️ **Secure environment variables** for private keys
✔️ **Deployable using Docker & Nginx**

## 🔧 Installation Guide

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/your-username/crypto-payment-gateway.git
cd crypto-payment-gateway
```

### 2️⃣ Backend Setup (Flask API)

```sh
cd backend
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
python app.py
```

📌 The API should run on **http://127.0.0.1:5000/**

### 3️⃣ Frontend Setup (React UI)

```sh
cd frontend
npm install
npm start
```

📌 The UI should run on **http://localhost:3000/**

## 🚀 API Endpoints

### 📌 Payment Processing

| Method | Endpoint               | Description                  |
| ------ | ---------------------- | ---------------------------- |
| `POST` | `/api/payment/init`    | Initialize a crypto payment  |
| `GET`  | `/api/payment/status`  | Check transaction status     |
| `POST` | `/api/payment/webhook` | Listen for blockchain events |

## 📜 License

This project is licensed under the **MIT License**.

## 🤝 Contributing

Feel free to contribute! Create a pull request or open an issue.

## 📧 Contact

If you have any questions, reach out at **pason.dev@gmail.com**.
