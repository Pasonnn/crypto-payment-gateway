   // src/App.jsx
   import React from 'react';
   import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Use Routes instead of Switch
   import Help from './components/Help';
   import NotFound from './components/NotFound';
   import LoginForm from './components/Auth/LoginForm';
   import RegisterForm from './components/Auth/RegisterForm';
   import Dashboard from './components/Dashboard/Dashboard';
   import AdminDashboard from './components/Admin/AdminDashboard';
   import LandingPage from './components/LandingPage/LandingPage';

   function App() {
     return (
       <Router>
         <Routes> {/* Use Routes here */}
           <Route path="/" element={<LandingPage />} />
           <Route path="/login" element={<LoginForm />} />
           <Route path="/register" element={<RegisterForm />} />
           <Route path="/dashboard" element={<Dashboard />} />
           <Route path="/admin" element={<AdminDashboard />} />
           <Route path="/help" element={<Help />} />

           <Route path="*" element={<NotFound />} /> {/* Fallback for 404 */}
         </Routes>
       </Router>
     );
   }

   export default App;