import React, { useContext } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useSnackbar } from "notistack";
import { UserContext } from "../UserContext";

const Header = () => {
  const { currentUser, logout } = useContext(UserContext);
  const navigate = useNavigate();
  const { enqueueSnackbar } = useSnackbar();

  const handleLogout = () => {
    logout()
      .then(() => {
        navigate("/");
        enqueueSnackbar("Logged out successfully", { variant: "success" });
      })
      .catch((err) => {
        enqueueSnackbar("Logout failed: " + err.message, { variant: "error" });
      });
  };

  return (
    <div id="header">
      <NavLink to={"/"}>
        <img src="/logo12.png" className="logo" alt="Kimchi-Compass Logo" />
      </NavLink>
      <nav>
        <NavLink to="/restaurants" className="header-btn">
          Restoran
        </NavLink>
        {currentUser ? (
          <>
            <NavLink to={`/profile/${currentUser.id}`} className="header-btn">
              Pwofil
            </NavLink>
            <NavLink to="/add-restaurant" className="header-btn">
              Ajoute Restoran
            </NavLink>
            <button onClick={handleLogout} className="header-btn">
              Dekonekte
            </button>
          </>
        ) : (
          <NavLink to={"/register"} className="header-btn">
            Konekte
          </NavLink>
        )}
      </nav>
    </div>
  );
};

export default Header;
