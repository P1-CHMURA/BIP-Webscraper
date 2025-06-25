import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

interface Source {
  id: string;
  name: string;  // backend zwraca "name"
}

interface Document {
  id: string;
  name: string;  // backend zwraca "name"
  typ: string;
  source_name: string;
}

const Summary = () => {
  const [sources, setSources] = useState<Source[]>([]);
  const [expandedSourceId, setExpandedSourceId] = useState<string | null>(null);
  const [documentsBySource, setDocumentsBySource] = useState<{ [sourceName: string]: Document[] }>({});
  const [loadingDocs, setLoadingDocs] = useState(false);

  useEffect(() => {
    const fetchSources = async () => {
      try {
        const response = await axios.get('http://localhost:5011/sources');
        setSources(response.data);
      } catch (error) {
        console.error('Błąd przy pobieraniu źródeł:', error);
      }
    };

    fetchSources();
  }, []);

  const toggleExpand = async (sourceId: string) => {
    if (expandedSourceId === sourceId) {
      setExpandedSourceId(null);
      return;
    }

    setExpandedSourceId(sourceId);

    const source = sources.find(s => s.id === sourceId);
    if (!source) return;

    if (!documentsBySource[source.name]) {
      setLoadingDocs(true);
      try {
        // tutaj wywołujemy endpoint /documents/<source_name>
        const response = await axios.get(`http://localhost:5011/documents/${encodeURIComponent(source.name)}`);
        setDocumentsBySource(prev => ({
          ...prev,
          [source.name]: response.data,
        }));
      } catch (error) {
        console.error('Błąd przy pobieraniu dokumentów:', error);
      } finally {
        setLoadingDocs(false);
      }
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Monitorowane strony BIP</h1>
      <p className="text-gray-600 mb-8">
        Lista scrapowanych stron Biuletynu Informacji Publicznej. Kliknij na pozycję, aby zobaczyć dokumenty.
      </p>

      <div className="bg-white shadow rounded-lg overflow-hidden">
        <ul className="divide-y divide-gray-200">
          {sources.map(source => (
            <li key={source.id} className="hover:bg-gray-50 transition-colors">
              <div
                className="px-6 py-4 flex justify-between items-center cursor-pointer"
                onClick={() => toggleExpand(source.id)}
              >
                <div>
                  <a
                    href={source.name}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-lg font-medium text-gray-800 hover:underline"
                  >
                    {source.name}
                  </a>
                </div>
                <div className="flex items-center">
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform ${
                      expandedSourceId === source.id ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>

              {expandedSourceId === source.id && (
                <div className="px-6 pb-4 pt-2 bg-gray-50">
                  <h4 className="font-medium text-gray-700 mb-3">Dokumenty:</h4>
                  {loadingDocs ? (
                    <div>Ładowanie dokumentów...</div>
                  ) : documentsBySource[source.name]?.length > 0 ? (
                    <ul className="space-y-3">
                      {documentsBySource[source.name].map(document => (
                        <li key={document.id} className="bg-white p-3 rounded shadow-sm">
                          <div className="flex justify-between items-center">
                            <div>
                              <a
                                href={document.name}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-gray-800 hover:underline"
                              >
                                {document.name}
                              </a>
                              <span className="text-sm text-gray-500 ml-2">({document.typ})</span>
                            </div>
                            <Link
                              to={`/summaries/${encodeURIComponent(document.name)}`}
                              className="inline-flex items-center px-3 py-1 text-xs font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                            >
                              Historia zmian
                            </Link>
                          </div>
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <div className="text-gray-500">Brak dokumentów</div>
                  )}
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Summary;
