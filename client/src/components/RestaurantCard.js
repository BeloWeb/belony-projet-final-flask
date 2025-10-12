import React from "react";
import { Link } from "react-router-dom";

const Card = ({ restaurant }) => {
  if (!restaurant) {
    return <div>Pa gen enfo sou Restoran sa</div>;
  }
  const { id, image_url, name, rating, phone_number } = restaurant;

  return (
    <div className="card">
      <img src={image_url} alt={name} />
      <div className="details">
        <h2>{name}</h2>
        <div className="hidden">
          <p>{rating}</p>
          <p className="subtle">{phone_number}</p>
          <Link to={`/restaurants/${id}`}>
            <button>Konnen plis</button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Card;
