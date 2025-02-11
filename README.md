# CryptoPay - Cryptocurrency Payment Gateway

CryptoPay is a simple and secure way to accept cryptocurrency payments on your website. This guide will help you integrate CryptoPay into your website.

## Quick Start

### 1. Get Your API Key

1. Create an account at [CryptoPay Dashboard](https://cryptopay.com/register)
2. Navigate to API Key section
3. Generate your API key

### 2. Add CryptoPay to Your Website

#### Using CDN

Add the following script to your HTML:

```html
<script src="https://cdn.cryptopay.com/cryptopay.js"></script>
```

Initialize CryptoPay with your API key:

```javascript
CryptoPay.init({
  apiKey: 'YOUR_API_KEY',
  environment: 'testnet', // or 'mainnet' for production
  currency: 'USD'
});
```

### 3. Create a Payment Button

#### Simple Integration

```html
<div id="cryptopay-button"></div>

<script>
  CryptoPay.createButton('cryptopay-button', {
    amount: 99.99,
    onSuccess: function(payment) {
      console.log('Payment successful:', payment);
    },
    onError: function(error) {
      console.error('Payment failed:', error);
    }
  });
</script>
```

#### React Integration

Install the package:
```bash
npm install @cryptopay/react
```

Use in your component:
```javascript
import { CryptoPayButton } from '@cryptopay/react';

function App() {
  return (
    <CryptoPayButton
      amount={99.99}
      onSuccess={(payment) => console.log('Payment successful:', payment)}
      onError={(error) => console.error('Payment failed:', error)}
    />
  );
}
```

## Features

- Accept ETH payments
- Real-time payment tracking
- Automatic payment verification
- Customizable UI
- Webhook notifications
- Detailed transaction history
- Sepolia testnet support

## API Documentation

For detailed API documentation, visit [docs.cryptopay.com](https://docs.cryptopay.com)

## Examples

### Custom Styling

```javascript
CryptoPay.createButton('cryptopay-button', {
  amount: 99.99,
  customStyle: {
    backgroundColor: '#007bff',
    color: 'white',
    padding: '15px 30px',
    borderRadius: '8px'
  }
});
```

### With Callback URL

```javascript
CryptoPay.createButton('cryptopay-button', {
  amount: 99.99,
  callbackUrl: 'https://your-website.com/payment/callback',
  metadata: {
    orderId: '12345',
    customerEmail: 'customer@example.com'
  }
});
```

## Development

For local development and contributing to CryptoPay, see:
- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)

## Support

- Documentation: [docs.cryptopay.com](https://docs.cryptopay.com)
- Issues: [GitHub Issues](https://github.com/yourusername/cryptopay/issues)
- Email: support@cryptopay.com

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
