import './App.css';
import Layout from './layout';
import Home from './pages/Home';
import Summary from './pages/Summary';
import ManageBIPs from './pages/ManageBIPs';
import { Routes, Route } from 'react-router-dom';
import DocumentHistoryPage from './pages/DocumentHistoryPage'
function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="/summaries" element={<Summary />} />
        <Route path="/manage" element={<ManageBIPs />} />
        <Route path={"/summaries/:document_name"} element={<DocumentHistoryPage />} />      </Route>
    </Routes>
  );
}

export default App;