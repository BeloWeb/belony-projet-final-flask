import React, { useState, useEffect } from "react";
import RestaurantCard from "./RestaurantCard";
import SearchFilter from "./SearchFilter";
import "../details.css";

const Restaurants = () => {
  const [restaurants, setRestaurants] = useState([]);
  const [filteredRestaurants, setFilteredRestaurants] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [alertMessage, setAlertMessage] = useState(""); // Local state for alert messages
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchRestaurants = async () => {
      setIsLoading(true);
      try {
        const response = await fetch("/restaurants");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        if (
          response.headers.get("content-type")?.includes("application/json")
        ) {
          const data = await response.json();
          setRestaurants(data);
          setFilteredRestaurants(data);
        } else {
          throw new Error("Response not JSON");
        }
      } catch (error) {
        setAlertMessage(error.message); // Update alert message state
      } finally {
        setIsLoading(false);
      }
    };

    fetchRestaurants();
  }, []);

  useEffect(() => {
    setFilteredRestaurants(
      restaurants.filter((restaurant) =>
        restaurant.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [searchTerm, restaurants]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div className="restaurants-container">
      <div className="image-overlay">
        <img src="/restaurant.jpg" alt="Restaurant Background" />
      </div>
      <div className="content-container">
        {" "}
        <div className="search-bar-container"></div>
        <SearchFilter value={searchTerm} onChange={handleSearchChange} />
        <div className="cards-container">
          {isLoading ? (
            <p>Fè yon ti tann...</p>
          ) : filteredRestaurants.length > 0 ? (
            filteredRestaurants.map((restaurant) => (
              <RestaurantCard key={restaurant.id} restaurant={restaurant} />
            ))
          ) : (
            <p>Pa gen rezilta</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Restaurants;
