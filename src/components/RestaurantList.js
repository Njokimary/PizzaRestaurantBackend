
import React, { useEffect, useState } from 'react';
import axios from '../services/api';

function RestaurantList() {
  const [restaurants, setRestaurants] = useState([]);

  useEffect(() => {
    axios.get('/restaurants')
      .then((response) => {
        setRestaurants(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div>
      <h2>Restaurants</h2>
      <ul>
        {restaurants.map((restaurant) => (
          <li key={restaurant.id}>
            <a href={`/restaurants/${restaurant.id}`}>{restaurant.name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RestaurantList;
