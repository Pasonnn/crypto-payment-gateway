class CryptoPayConfig {
  static instance = null;
  
  constructor() {
    this.apiKey = '3803d823d5f6aed8b534f775b5e471231784099ff3b0932ec51e8793cede2c92';
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