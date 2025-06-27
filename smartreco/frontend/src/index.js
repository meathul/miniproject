import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './styles/global.css'; // ✅ Optional: only if the file exists

const root = createRoot(document.getElementById('root'));
root.render(<App />);
