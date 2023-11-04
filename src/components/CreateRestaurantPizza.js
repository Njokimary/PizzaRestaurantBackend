
import React, { useState } from 'react';
import axios from '../services/api';

function CreateRestaurantPizza() {
  const [price, setPrice] = useState('');
  const [pizzaId, setPizzaId] = useState('');
  const [restaurantId, setRestaurantId] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const data = {
      price: parseFloat(price),
      pizza_id: parseInt(pizzaId),
      restaurant_id: parseInt(restaurantId),
    };

    axios.post('/restaurant_pizzas', data)
      .then(() => {
        // Handle success
        setError('');
        setPrice('');
        setPizzaId('');
        setRestaurantId('');
      })
      .catch((error) => {
        // Handle validation errors
        setError('Validation errors');
      });
  };

  return (
    <div>
      <h2>Create Restaurant Pizza</h2>
      <form onSubmit={handleSubmit}>
        <input type="number" placeholder="Price" value={price} onChange={(e) => setPrice(e.target.value)} />
        <input type="number" placeholder="Pizza ID" value={pizzaId} onChange={(e) => setPizzaId(e.target.value)} />
        <input type="number" placeholder="Restaurant ID" value={restaurantId} onChange={(e) => setRestaurantId(e.target.value)} />
        <button type="submit">Create</button>
      </form>
      {error && <p>{error}</p>}
    </div>
  );
}

export default CreateRestaurantPizza;
