import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import Landing from './Pages/Landing_page/Landing_Page.jsx';

export default function App() {

  
  // Theme State: Defaulting to dark mode to match your requested vibe
  const [isDark, setIsDark] = useState(true);

  // Apply the dark class to the HTML root element dynamically
  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [isDark]);

  return (
    <BrowserRouter>
      <Routes>
        <Route 
          path="/" 
          element={ <Landing/> } 
        />
       
      </Routes>
    </BrowserRouter>
  );
}