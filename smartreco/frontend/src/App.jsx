import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage'; 
import UserDataForm from './pages/UserDataForm';
import RecommendationPage from './pages/RecommendationPage';
import ShopPage from './pages/ShopPage';
import ModelResponsePage from './pages/ModelResponsePage';

function App() {
  const [userProfile, setUserProfile] = useState(null);
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/user-info" element={<UserDataForm setUserProfile={setUserProfile} />} />
        <Route path="/recommendations" element={<RecommendationPage userProfile={userProfile} />} />
        <Route path="/shop" element={<ShopPage />} />
        <Route path="/model-response" element={<ModelResponsePage />} />
      </Routes>
    </Router>
  );
}

export default App;
