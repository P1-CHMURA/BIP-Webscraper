import { useParams, Link } from 'react-router-dom';
import React, { useEffect, useState } from 'react';

interface DocumentVersion {
  id: string;
  document_id: string;
  document_name: string;
  content: string;
  date: string;
}

const DocumentHistoryPage = () => {
  const { document_name } = useParams<{ document_name: string }>();
  const decodedDocumentName = decodeURIComponent(document_name || '');

  const [versions, setVersions] = useState<DocumentVersion[]>([]);
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchVersions = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch(`http://127.0.0.1:5011/versions/${decodedDocumentName}`);
        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.error || 'Błąd pobierania danych');
        }
        const data: DocumentVersion[] = await response.json();
        setVersions(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchVersions();
  }, [decodedDocumentName]);

  const toggleItem = (id: string) => {
    setExpandedItems(prev => {
      const newSet = new Set(prev);
      newSet.has(id) ? newSet.delete(id) : newSet.add(id);
      return newSet;
    });
  };

  if (loading) {
    return <div className="container mx-auto px-4 py-8">Ładowanie historii zmian...</div>;
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white shadow rounded-lg p-6 text-red-600">
          Błąd: {error}
        </div>
        <Link to="/summaries" className="mt-4 inline-block text-blue-600 hover:text-blue-800">
          Powrót do listy dokumentów
        </Link>
      </div>
    );
  }

  if (versions.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white shadow rounded-lg p-6 text-gray-600">
          Brak historii zmian dla dokumentu: <strong>{decodedDocumentName}</strong>
        </div>
        <Link to="/summaries" className="mt-4 inline-block text-blue-600 hover:text-blue-800">
          Powrót do listy dokumentów
        </Link>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link to="/summaries" className="inline-flex items-center text-blue-600 hover:text-blue-800">
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Powrót do listy dokumentów
        </Link>
      </div>

      <h1 className="text-3xl font-bold text-gray-800 mb-6">
        Historia zmian dokumentu: {decodedDocumentName}
      </h1>

      <div className="bg-white shadow rounded-lg overflow-hidden">
        <ul className="divide-y divide-gray-200">
          {versions.map(version => (
            <li key={version.id} className="p-4 hover:bg-gray-50 transition">
              <button
                onClick={() => toggleItem(version.id)}
                className="w-full text-left flex justify-between items-center focus:outline-none"
              >
                <span className="text-lg font-medium text-gray-800">
                  Zmiany z dnia {new Date(version.date).toLocaleDateString()}
                </span>
                <svg
                  className={`w-5 h-5 transform transition-transform duration-200 ${
                    expandedItems.has(version.id) ? 'rotate-180' : ''
                  }`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              {expandedItems.has(version.id) && (
                <div className="mt-4 text-gray-600 whitespace-pre-line">
                  {version.content}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DocumentHistoryPage;
