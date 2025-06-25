import React from 'react';
import ChatInterface from '../components/ChatInterface';
import ProductCard from '../components/ProductCard';
import PreferencesForm from '../components/PreferencesForm';

// Placeholder product
const product = { name: 'Sample Product', description: 'Description here', price: 99.99 };

export default function Home() {
  return (
    <div>
      <h1>SmartReco Home</h1>
      <PreferencesForm />
      <ChatInterface />
      <ProductCard product={product} />
    </div>
  );
}
