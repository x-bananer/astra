import LayoutClient from "../components/layout/layout-client";
import { AuthProvider } from "../components/auth/auth-provider";

export const metadata = {
  title: "ASTRA | Metropolia",
  description: "ASTRA is a Metropolia Student Teamwork Assistant.",
};

const RootLayout = ({ children }) => {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <LayoutClient>{children}</LayoutClient>
        </AuthProvider>
      </body>
    </html>
  );
}

export default RootLayout;