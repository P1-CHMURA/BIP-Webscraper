import { Outlet, Link } from "react-router-dom";

const Layout = () => {
  return (
    <div>
      <header>
        <nav>

        </nav>
      </header>
      <main>
        <Outlet />
      </main>
      <footer>© 2025 BIPscrapper</footer>
    </div>
  );
};

export default Layout;