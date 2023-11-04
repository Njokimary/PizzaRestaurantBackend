
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from '../services/api';

function RestaurantDetail() {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);

  useEffect(() => {
    axios.get(`/restaurants/${id}`)
      .then((response) => {
        setRestaurant(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, [id]);

  if (!restaurant) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>{restaurant.name}</h2>
      <p>{restaurant.address}</p>
      <h3>Pizzas</h3>
      <ul>
        {restaurant.pizzas.map((pizza) => (
          <li key={pizza.id}>{pizza.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default RestaurantDetail;
