import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserDataForm.css';
import { getOrCreateUserId } from '../services/api';
import axios from 'axios';

function UserDataForm({ setUserProfile }) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    gender: '',
    ethnicity: '',
    skinType: '',
    skinConcerns: [],
    allergies: '',
    budget: '',
    preferredBrands: []
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === 'checkbox') {
      const updatedConcerns = checked
        ? [...formData.skinConcerns, value]
        : formData.skinConcerns.filter((concern) => concern !== value);

      setFormData({ ...formData, skinConcerns: updatedConcerns });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const updateUserProfile = async (profile) => {
    const userId = getOrCreateUserId();
    const userProfile = {
      user_id: userId,
      profile: {
        skin_type: profile.skinType,
        age: Number(profile.age),
        ethnicity: profile.ethnicity,
        budget: Number(profile.budget) || 1000, // default budget if not present
        preferred_brands: profile.preferredBrands || [],
      },
    };
    await axios.post('http://localhost:8000/update_user', userProfile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setUserProfile(formData);
    await updateUserProfile(formData);
    navigate('/recommendations');
  };

  // Add this function to clear user_id and reset form
  const handleNewUser = () => {
    localStorage.removeItem('user_id');
    setFormData({
      name: '',
      age: '',
      gender: '',
      ethnicity: '',
      skinType: '',
      skinConcerns: [],
      allergies: '',
      budget: '',
      preferredBrands: []
    });
  };

  // Add this function to navigate to landing page
  const handleGoToLanding = () => {
    navigate('/');
  };

  return (
    <div className="form-container">
      <button onClick={handleNewUser} className="new-user-btn">New User</button>
      <button onClick={handleGoToLanding} className="landing-btn">Back to Landing Page</button>
      <form onSubmit={handleSubmit} className="user-form">
        <h2>Tell Us About Your Skin</h2>
        <input type="text" name="name" placeholder="Name" value={formData.name} onChange={handleChange} required />
        <input type="number" name="age" placeholder="Age" value={formData.age} onChange={handleChange} required />

        <div className="gender-group">
          <label><input type="radio" name="gender" value="Male" onChange={handleChange} /> Male</label>
          <label><input type="radio" name="gender" value="Female" onChange={handleChange} /> Female</label>
          <label><input type="radio" name="gender" value="Other" onChange={handleChange} /> Other</label>
        </div>

        <input type="text" name="ethnicity" placeholder="Ethnicity" value={formData.ethnicity} onChange={handleChange} required />


        <select name="skinType" value={formData.skinType} onChange={handleChange} required>
          <option value="">Select Skin Type</option>
          <option value="Oily">Oily</option>
          <option value="Dry">Dry</option>
          <option value="Combination">Combination</option>
          <option value="Sensitive">Sensitive</option>
          <option value="Normal">Normal</option>
        </select>

        <div className="checkbox-group">
          <label><input type="checkbox" name="skinConcerns" value="Acne Scars" onChange={handleChange} /> Acne Scars</label>
          <label><input type="checkbox" name="skinConcerns" value="Acne Marks" onChange={handleChange} /> Acne Marks</label>
          <label><input type="checkbox" name="skinConcerns" value="Pigmentation" onChange={handleChange} /> Pigmentation</label>
          <label><input type="checkbox" name="skinConcerns" value="Dark Spots" onChange={handleChange} /> Dark Spots</label>
          <label><input type="checkbox" name="skinConcerns" value="Blackheads" onChange={handleChange} /> Blackheads</label>
          <label><input type="checkbox" name="skinConcerns" value="Redness" onChange={handleChange} /> Redness</label>
        </div>

        <input type="text" name="allergies" placeholder="Any allergies?" value={formData.allergies} onChange={handleChange} />

        <input type="number" name="budget" placeholder="Budget" value={formData.budget} onChange={handleChange} />

        <div className="checkbox-group">
          <label><input type="checkbox" name="preferredBrands" value="Brand1" onChange={handleChange} /> Brand1</label>
          <label><input type="checkbox" name="preferredBrands" value="Brand2" onChange={handleChange} /> Brand2</label>
          <label><input type="checkbox" name="preferredBrands" value="Brand3" onChange={handleChange} /> Brand3</label>
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default UserDataForm;
