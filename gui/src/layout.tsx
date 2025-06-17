import { Outlet, NavLink } from 'react-router-dom';
import './App.css';

const Layout = () => {
  return (
    <div className="layout">
      <header className="navbar">
        <h2>BIPscrapper</h2>
        <nav className="nav-links">
          <NavLink 
            to="/" 
            end 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Strona główna
          </NavLink>
          <NavLink 
            to="/podsumowania" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Podsumowania
          </NavLink>
          <NavLink 
            to="/zarzadzaj" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Zarządzaj listą BIP-ów
          </NavLink>
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