   // src/App.jsx
   import React from 'react';
   import { BrowserRouter, Routes, Route } from 'react-router-dom';
   import Help from './components/Help';
   import NotFound from './components/NotFound';
   import LoginForm from './components/Auth/LoginForm';
   import RegisterForm from './components/Auth/RegisterForm';
   import Dashboard from './components/Dashboard/Dashboard';
   import AdminDashboard from './components/Admin/AdminDashboard';
   import LandingPage from './components/LandingPage/LandingPage';
   import ProtectedRoute from './components/Common/ProtectedRoute';

   function App() {
     return (
       <BrowserRouter>
         <Routes>
           <Route path="/" element={<LandingPage />} />
           <Route path="/login" element={<LoginForm />} />
           <Route path="/register" element={<RegisterForm />} />
           <Route path="/dashboard" element={<Dashboard />} />
           <Route
             path="/admin"
             element={
               <ProtectedRoute requiredRole="admin">
                 <AdminDashboard />
               </ProtectedRoute>
             }
           />
           <Route path="/help" element={<Help />} />
           <Route path="*" element={<NotFound />} />
         </Routes>
       </BrowserRouter>
     );
   }

   export default App;