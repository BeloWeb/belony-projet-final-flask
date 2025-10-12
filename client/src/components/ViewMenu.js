import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "../ViewMenu.css";

const ViewMenu = () => {
  const { id } = useParams();
  const [menus, setMenus] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch(`/menus?restaurant_id=${id}`)
      .then((response) => response.json())
      .then((data) => {
        setMenus(data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching menus:", error);
        setIsLoading(false);
      });
  }, [id]);

  if (isLoading) {
    return <div className="menu-loading">Lap li meni yo...</div>;
  }

  return (
    <div className="view-menu-wrapper">
      <div className="menu-image"></div>
      <div className="menu-container">
        <h1 className="menu-title"></h1>
        <div className="menu-content">
          {menus.map((menu) => (
            <section key={menu.id} className="menu-section">
              <h3 className="menu-section-title">{menu.name}</h3>
              <ul className="menu-list">
                {menu.menu_dishes.map((menuDish) => (
                  <li key={menuDish.id} className="menu-item">
                    {menuDish.dish.name} - {menuDish.dish.description} - $
                    {menuDish.dish.price}
                  </li>
                ))}
              </ul>
            </section>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ViewMenu;
