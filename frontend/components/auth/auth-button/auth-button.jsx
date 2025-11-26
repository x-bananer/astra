"use client";

import styles from "./auth-button.module.css";

const AuthButton = () => {
    const login = () => {
        window.location.href = "http://localhost:4000/auth/google/login";
    };

    return (
        <button className={styles['auth-button']} onClick={login}>
            <img src="/google-logo.png" className={styles['auth-button__icon']} alt="Google authentification button" />
            Sign in with Google
        </button>
    );
}

export default AuthButton;