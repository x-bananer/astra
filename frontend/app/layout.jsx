import "../src/assets/style.css";

import AppHeader from '../src/components/app/appHeader/app-header';
import AppFooter from '../src/components/app/appFooter/app-footer';

export const metadata = {
  title: "ASTRA | Metropolia",
  description: "ASTRA is a Metropolia Student Teamwork Assistant. ASTRA provides Metropolia students with teamwork analytics, project insights, and AI-driven support.",
};

export default function RootLayout({
  children,
}) {
  return (
    <html lang="en">
      <body className="antialiased">
        <div className="app">
          <AppHeader className="layout app__header" />
          <main className="layout app__content">
            {children}
          </main>
          <AppFooter className="layout app__footer" />
        </div>
      </body>
    </html>
  );
}
