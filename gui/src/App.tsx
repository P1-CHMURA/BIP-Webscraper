import './App.css';
import Layout from './layout';
import Home from './pages/Home';
import Summary from './pages/Summary';
import ManageBIPs from './pages/ManageBIPs';
import { Routes, Route } from 'react-router-dom';
import BipHistoryPage from './pages/BipHistoryPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="/podsumowania" element={<Summary />} />
        <Route path="/zarzadzaj" element={<ManageBIPs />} />
        <Route path="/bip/history/:id" element={<BipHistoryPage />} />
      </Route>
    </Routes>
  );
}

export default App;