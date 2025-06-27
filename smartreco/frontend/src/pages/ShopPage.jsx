import React from 'react';
import './ShopPage.css';
import { useNavigate } from 'react-router-dom';

const ShopPage = () => {
  const navigate = useNavigate();

  const handleSubmit = () => {
    navigate('/model-response');
  };

  return (
    <div className="shop-container">
      <header className="shop-header">
        <h1>DermaBot Store</h1>
        <input type="text" placeholder="Search skincare needs..." />
        <button onClick={handleSubmit}>Submit</button>
      </header>

      <div className="product-grid">
        <div className="product-card">
          <img src="https://source.unsplash.com/featured/?moisturizer" alt="Moisturizer" />
          <h3>GlowMoist Cream</h3>
          <p>₹599</p>
        </div>
        <div className="product-card">
          <img src="https://source.unsplash.com/featured/?facewash" alt="Facewash" />
          <h3>PureClean Wash</h3>
          <p>₹399</p>
        </div>
      </div>
    </div>
  );
};

export default ShopPage;
