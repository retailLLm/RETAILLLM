import React from 'react';

import SearchBar from './SearchComponent';
import './UserDashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard-container">
   
      <main className="main-content">
        <SearchBar />
        <div className="additional-content">
          {/* Additional content and components */}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
