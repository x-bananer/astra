import LayoutClient from "../components/layout/layout-client";

export const metadata = {
  title: "ASTRA | Metropolia",
  description: "ASTRA is a Metropolia Student Teamwork Assistant.",
};

const RootLayout = ({ children }) => {
  return (
    <html lang="en">
      <body>
        <LayoutClient>{children}</LayoutClient>
      </body>
    </html>
  );
}

export default RootLayout;