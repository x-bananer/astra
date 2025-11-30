"use client";

import { createContext, useContext, useEffect, useState, useMemo } from "react";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    async function loadUser() {
        try {
            const res = await fetch("http://localhost:4000/auth/user", {
                credentials: "include"
            });
            const json = await res.json();
            if (json.authenticated) setUser(json.user);
            else setUser(null);
        } catch {
            setUser(null);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadUser();
    }, []);

    const value = {
        user,
        setUser,
        loading,
        loadUser
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);