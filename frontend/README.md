# CryptoPay Frontend

The frontend application for CryptoPay - a cryptocurrency payment gateway solution.

## Features

- User Authentication (Login/Register)
- Dashboard with Revenue Analytics
- Transaction Management
- Wallet Connection (MetaMask Integration)
- API Key Management
- User Profile Management
- Payment Processing Interface

## Prerequisites

- Node.js >=14
- npm or yarn
- MetaMask browser extension

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Pasonnn/crypto-payment-gateway.git
cd cryptopay/frontend
```

2. Install dependencies:

```bash
npm install
```

3. Create environment files:

For development (.env.development):

```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_WS_URL=ws://localhost:5000
```

For production (.env.production):

```
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_WS_URL=wss://your-backend-domain.com
```

## Development

Start the development server:

```bash
npm start
```

## Building for Production

```bash
npm run build
```

## Deployment

The project is configured for Vercel deployment:

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Deploy:

```bash
vercel
```

3. For production:

```bash
vercel --prod
```

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── assets/         # Images and static files
│   ├── components/     # React components
│   │   ├── Auth/      # Authentication components
│   │   ├── Common/    # Shared components
│   │   ├── Dashboard/ # Dashboard components
│   │   └── LandingPage/
│   ├── config/        # Configuration files
│   ├── styles/        # CSS styles
│   └── App.js         # Main application component
├── package.json
└── vercel.json        # Vercel deployment config
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
