 // src/index.js
 import React from 'react';
 import ReactDOM from 'react-dom';
 import App from './App'; // Import the main App component
 import './style.css'; // Optional: Import global styles

 ReactDOM.render(
   <React.StrictMode>
     <App />
   </React.StrictMode>,
   document.getElementById('root') // This should match the <div id="root"></div> in index.html
 );