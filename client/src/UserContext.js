import React, { createContext, useState, useEffect } from "react";

export const UserContext = createContext({
  currentUser: null,
  isLoading: true,
  login: () => {},
  logout: () => {},
});

export const UserProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check session on app load
    fetch("/check_session", {
      credentials: "include", // Necessary for cookies to be sent and received
    })
      .then((res) => res.json())
      .then((data) => {
        if (data && data.id) {
          setCurrentUser(data);
        }
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, []);

  const updateUser = (newUser) => {
    setCurrentUser(newUser);
  };

  useEffect(() => {
    if (currentUser && currentUser.id) {
      fetch(`/food_users/${currentUser.id}`)
        .then((response) => response.json())
        .then((data) => {
          setCurrentUser(data);
        })
        .catch((error) =>
          console.error("Failed to fetch updated user data", error)
        );
    }
  }, [currentUser?.id]);

  const logout = async () => {
    const response = await fetch("/logout", {
      method: "DELETE", // Change to DELETE if that's what the server expects
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Logout failed");
    }
    setCurrentUser(null);
  };
  const login = (userData) => {
    setCurrentUser(userData); // Update state with the user data
  };

  return (
    <UserContext.Provider
      value={{ currentUser, isLoading, login, logout, updateUser }}>
      {children}
    </UserContext.Provider>
  );
};
