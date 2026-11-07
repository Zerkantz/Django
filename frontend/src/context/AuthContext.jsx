import React, { useState, useEffect, createContext } from "react";
import { setToken, getToken, removeToken } from "../api/token";
import { useUser } from "../hooks/useUser";

export const AuthContext = createContext({
  auth: undefined,
  login: () => null,
  logout: () => null,
});

export function AuthProvider({ children }) {
  const [auth, setAuth] = useState(undefined);
  const { getMe } = useUser();

  useEffect(() => {
    (async () => {
      const token = getToken();
      if (!token) {
        setAuth(null);
      } else {
        await login(token);
      }
    })();
  }, []);

  const login = async (token) => {
    try {
      setToken(token);
      const me = await getMe(token);
      setAuth({ token, me });
    } catch (error) {
      setAuth(null);
      removeToken();
    }
  };

  const logout = () => {
    setAuth(null);
    removeToken();
  };

  const valueContext = {
    auth,
    login,
    logout,
  };

  if (auth === undefined) return null;

  return (
    <AuthContext.Provider value={valueContext}>{children}</AuthContext.Provider>
  );
}
