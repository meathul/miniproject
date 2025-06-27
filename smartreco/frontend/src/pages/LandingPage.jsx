import React from 'react';
import { Link } from 'react-router-dom';
import './LandingPage.css'; 

function LandingPage() {
  return (
    <div className="landing-bg">
      <div className="landing-card">
        <h1 className="brand-name">DermaBot</h1>
        <p className="tagline">
          Your personalized skincare assistant powered by AI ✨
        </p>
        <div className="landing-btn-group">
          <Link to="/login">
            <button className="start-button">Get Started</button>
          </Link>
          <Link to="/user-info">
            <button className="user-info-button">Go to User Info</button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
