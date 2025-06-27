import React, { useState } from 'react';
import './ProductCard.css';

function ProductCard({ product }) {
  const [imgError, setImgError] = useState(false);
  const imageUrl = `https://source.unsplash.com/featured/?${encodeURIComponent(product.name)}`;
  const fallbackUrl = '/default-product-image.png'; // Place a default image in your public folder

  return (
    <div className="product-card aesthetic-card">
      <img
        src={imgError ? fallbackUrl : imageUrl}
        alt={product.name}
        onError={() => setImgError(true)}
        className="product-img"
      />
      <h3 className="product-brand">{product.name}</h3>
    </div>
  );
}

export default ProductCard;
