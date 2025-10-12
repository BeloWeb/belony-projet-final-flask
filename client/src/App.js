import React, { useState } from "react";
import Header from "./components/Header";
import AppRoutes from "./components/routes";
import Footer from "./components/Footer";

const App = () => {
  const [user, setUser] = useState(null);

  const updateUser = (user) => {
    setUser(user);
  };

  const ctx = { user, updateUser };

  return (
    <div className="site-container">
      <div className="content-wrap">
        <Header user={user} updateUser={updateUser} />
        <Footer user={user} updateUser={updateUser} />

        <AppRoutes context={ctx} />
      </div>
    </div>
  );
};

export default App;
