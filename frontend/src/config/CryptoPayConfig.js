class CryptoPayConfig {
  static instance = null;
  
  constructor() {
    this.apiKey = "0b35fe6dca083a8f240cab41fcd83f7706c07c52690d9909cc10e10ce3784147";
    this.environment = 'testnet'; // or 'mainnet'
    this.currency = 'USD';
    this.callbackUrl = null;
  }

  static getInstance() {
    if (!CryptoPayConfig.instance) {
      CryptoPayConfig.instance = new CryptoPayConfig();
    }
    return CryptoPayConfig.instance;
  }

  init(config) {
    this.apiKey = config.apiKey;
    this.environment = config.environment || 'testnet';
    this.currency = config.currency || 'ETH';
    this.callbackUrl = config.callbackUrl;
  }

  getConfig() {
    if (!this.apiKey) {
      throw new Error('CryptoPay not initialized. Please call CryptoPayConfig.init() first');
    }
    return {
      apiKey: this.apiKey,
      environment: this.environment,
      currency: this.currency,
      callbackUrl: this.callbackUrl
    };
  }
}

export default CryptoPayConfig.getInstance(); 