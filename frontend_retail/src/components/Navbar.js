import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="nav-container">
      <div className="nav-left">
        <a href="/" className="logo-link">
         
          <span className="explore-text">Home</span>
        </a>
        <a href="/search" className="logo-link">
         
          <span className="explore-text">Search</span>
        </a>
        <a href="/productAvailability" className="logo-link">
        
          <span className="explore-text">Product Availability</span>
        </a>

      </div>
     <div className="nav-right">
       
        <button className="sign-up-btn">LOGOUT</button>
        
      </div>
    </nav>
  );
};

export default Navbar;
