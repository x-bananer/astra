"use client";

import "../../assets/style.css";
import { usePathname } from "next/navigation";
import AppHeaderLogin from "../app/appHeader/app-header-login";
import AppHeader from "../app/appHeader/app-header";
import AppFooter from "../app/appFooter/app-footer";

const LayoutClient = ({ children }) => {
  const pathname = usePathname();
  const isLogin = pathname === "/login";

  return (
    <div className="app">
      {isLogin ? (
        <AppHeaderLogin className="layout app__header" />
      ) : (
        <AppHeader className="layout app__header" />
      )}

      <main className="layout app__content">{children}</main>

      <AppFooter className="layout app__footer" />
    </div>
  );
}

export default LayoutClient;