(function(window) {
  window.CryptoPay = {
    init: function(config) {
      // Store configuration
      this.config = config;
      
      // Inject necessary styles
      const style = document.createElement('style');
      style.textContent = `
        .cryptopay-button {
          /* Default button styles */
        }
        /* Add other necessary styles */
      `;
      document.head.appendChild(style);
    },

    createButton: function(elementId, options = {}) {
      const element = document.getElementById(elementId);
      if (!element) return;

      const button = document.createElement('button');
      button.className = 'cryptopay-button';
      button.innerHTML = `
        <img src="${options.iconUrl || 'https://ibb.co/W4yRZM6b'}" alt="CryptoPay">
        ${options.text || 'Pay with CryptoPay'}
      `;

      button.onclick = () => this.handlePayment(options);
      element.appendChild(button);
    },

    handlePayment: function(options) {
      // Create and show payment modal
      const modal = document.createElement('div');
      // Add payment modal implementation
    }
  };
})(window); 