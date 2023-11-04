import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import RestaurantList from './components/RestaurantList';
import RestaurantDetail from './components/RestaurantDetail';
import CreateRestaurantPizza from './components/CreateRestaurantPizza';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/restaurants/:id" element={<RestaurantDetail />} />
        <Route path="/create-restaurant-pizza" element={<CreateRestaurantPizza />} />
        <Route path="/" element={<RestaurantList />} />
      </Routes>
    </Router>
  );
}

export default App;
