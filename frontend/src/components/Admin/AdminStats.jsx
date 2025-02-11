import React from 'react';
import { Line } from 'react-chartjs-2';

const AdminStats = ({ users }) => {
  // Convert users object to array for calculations
  const usersArray = Object.values(users);
  
  // Calculate statistics
  const totalUsers = usersArray.length;
  const activeUsers = usersArray.filter(user => user.wallet_address).length;
  
  // Group registrations by month
  const registrationsByMonth = usersArray.reduce((acc, user) => {
    const month = new Date(user.created_at).toLocaleString('default', { month: 'long' });
    acc[month] = (acc[month] || 0) + 1;
    return acc;
  }, {});

  const chartData = {
    labels: Object.keys(registrationsByMonth),
    datasets: [{
      label: 'User Registrations',
      data: Object.values(registrationsByMonth),
      fill: false,
      borderColor: 'rgb(0, 255, 149)',
      tension: 0.1
    }]
  };

  return (
    <div className="admin-stats">
      <h2>System Statistics</h2>
      
      <div className="stats-overview">
        <div className="stat-card">
          <h3>Total Users</h3>
          <p>{totalUsers}</p>
        </div>
        <div className="stat-card">
          <h3>Active Users</h3>
          <p>{activeUsers}</p>
        </div>
        <div className="stat-card">
          <h3>Wallet Connection Rate</h3>
          <p>{((activeUsers / totalUsers) * 100).toFixed(1)}%</p>
        </div>
      </div>

      <div className="stats-chart">
        <h3>User Registration Trend</h3>
        <div className="chart-container">
          <Line data={chartData} options={{
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }} />
        </div>
      </div>
    </div>
  );
};

export default AdminStats; 