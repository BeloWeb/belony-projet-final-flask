import React from "react";
import { Route, Routes } from "react-router-dom";
import SignUp from "../components/SignUp";
import RestaurantDetails from "../components/RestaurantDetails";
import UserProfile from "../components/UserProfile";
import AddRestaurantForm from "../components/AddRestaurantForm";
import ViewMenu from "../components/ViewMenu";
import Edit from "../components/Edit";
import AboutUs from "../components/AboutUs";
import Restaurants from "../components/Restaurants";

const AppRoutes = ({ context }) => {
  return (
    <Routes>
      <Route path="/restaurants" element={<Restaurants context={context} />} />
      <Route
        path="/restaurants/:id"
        element={<RestaurantDetails context={context} />}
      />
      <Route path="/view-menu/:id" element={<ViewMenu context={context} />} />
      <Route path="/register" element={<SignUp context={context} />} />
      <Route path="/profile/:id" element={<UserProfile context={context} />} />
      <Route path="/profile/edit" element={<Edit context={context} />} />
      <Route path="/" element={<AboutUs context={context} />} />

      <Route
        path="/add-restaurant"
        element={<AddRestaurantForm context={context} />}
      />
    </Routes>
  );
};

export default AppRoutes;
