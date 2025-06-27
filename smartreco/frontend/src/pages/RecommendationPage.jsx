import React, { useState } from 'react';
import ProductCard from '../components/ProductCard';
import './RecommendationPage.css';
import { getRecommendation } from '../services/api';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';

function RecommendationPage({ userProfile }) {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [products, setProducts] = useState([]);
  const [showProducts, setShowProducts] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleAsk = async () => {
    setLoading(true);
    setError('');
    setShowProducts(false);
    setResponse(null);
    setProducts([]);
    try {
      const result = await getRecommendation(query);
      if (result.error) {
        setError(result.error);
      } else {
        setResponse(result);
        if (Array.isArray(result.routine) && result.routine.length > 0) {
          setProducts(result.routine.map(r => ({
            ...r.product,
            description: r.explanation || r.reasoning || '',
            name: r.product?.brand || r.product?.company || '',
            price: r.product?.real_time_price || r.product?.price || '',
            image: r.product?.image || 'https://source.unsplash.com/featured/?skincare',
          })));
        } else if (result.product) {
          setProducts([{
            ...result.product,
            description: result.explanation || '',
            name: result.product.brand || result.product.company || '',
            price: result.product.real_time_price || result.product.price || '',
            image: result.product.image || 'https://source.unsplash.com/featured/?skincare',
          }]);
        }
        setShowProducts(true);
      }
    } catch (err) {
      setError('Failed to fetch recommendation.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResponse(null);
    setProducts([]);
    setShowProducts(false);
    setError('');
  };

  return (
    <div className="recommendation-bg">
      <button onClick={() => navigate('/user-info')} className="back-btn">Back to User Profile</button>
      <div className="recommendation-card">
        <header className="recommendation-header">
          <h1>DermaBot</h1>
          <p>Your AI-powered skincare companion ✨</p>
        </header>

        <div className="chat-input-area">
          <textarea
            placeholder="Ask me your skincare query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          ></textarea>
          <div className="button-group">
            <button onClick={handleAsk} disabled={loading || !query.trim()}>{loading ? 'Loading...' : 'Ask'}</button>
            <button onClick={handleClear} className="clear-btn">Clear</button>
          </div>
        </div>

        {error && (
          <div className="response-area error">
            <p>{error}</p>
          </div>
        )}

        {response && response.explanation && !error && (
          <div className="response-area">
            <ReactMarkdown>{response.explanation}</ReactMarkdown>
          </div>
        )}

        {/* Show expanded routine as Markdown if available */}
        {response && response.expanded_routine && !error && (
          <div className="routine-area">
            <h2>Routine</h2>
            <ReactMarkdown>{response.expanded_routine}</ReactMarkdown>
          </div>
        )}

        {showProducts && products.length > 0 && (
          <div className="products-area">
            <h2>Recommended Products</h2>
            <div className="product-grid">
              {products.map((product, i) => (
                <ProductCard key={i} product={product} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default RecommendationPage;
