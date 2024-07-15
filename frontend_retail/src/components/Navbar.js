import React from 'react';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="nav-container">
      <div className="nav-left">
        <a href="/" className="logo-link">
         
          <span className="explore-text">Explore</span>
        </a>
        <a href="/" className="logo-link">
         
          <span className="explore-text">Explore</span>
        </a>
        <a href="/" className="logo-link">
        
          <span className="explore-text">Explore</span>
        </a>

      </div>
     <div className="nav-right">
       
        <button className="sign-up-btn">LOGOUT</button>
        
      </div>
    </nav>
  );
};

export default Navbar;
