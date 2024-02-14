import React, { useContext, useEffect, useState } from 'react';
import { Routes , Route } from 'react-router-dom';


import NavBar from './NavBar';
import ErrorMessage from './ErrorMessage';
import Footer from './Footer';
import PrivacyPolicyPage from '../pages/general/PrivacyPolicy';
import TermsOfServicePage from '../pages/general/TermsOfService';
import AboutPage from '../pages/general/About';
import MissingPage from '../pages/general/404Page';
import HomePage from '../pages/Home';
import SportPage from '../pages/Sport';


function App() {
  return (
      <div className="bg-white min-h-screen flex flex-col">
      
      <NavBar/>
      <ErrorMessage />
      <div className="flex-grow ">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />
          <Route path="/terms-of-service" element={<TermsOfServicePage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/:sport" element={<SportPage />} />
        </Routes>
      </div>
      <Footer />
      </div>
  );
}

export default App;