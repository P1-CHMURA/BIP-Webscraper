import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

interface Source {
  id: string;
  name: string;
}

interface Document {
  id: string;
  name: string;
  typ: string;
  source_name: string;
}

interface Summary {
  id: number;
  content: string;
  date: string;
  document_id: number;
  document_name: string;
}

const Summary = () => {
  const [sources, setSources] = useState<Source[]>([]);
  const [expandedSourceId, setExpandedSourceId] = useState<string | null>(null);
  const [documentsBySource, setDocumentsBySource] = useState<{ [sourceName: string]: Document[] }>({});
  const [summariesByDocument, setSummariesByDocument] = useState<{ [documentName: string]: Summary[] }>({});
  const [loadingDocs, setLoadingDocs] = useState(false);
  const [loadingSummaries, setLoadingSummaries] = useState<{ [documentName: string]: boolean }>({});
  const [expandedSummaries, setExpandedSummaries] = useState<{ [summaryId: number]: boolean }>({});

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

  const fetchSummariesForDocument = async (documentName: string) => {
    if (summariesByDocument[documentName]) return;

    setLoadingSummaries(prev => ({ ...prev, [documentName]: true }));

    try {
      const response = await axios.get(`http://localhost:5011/summaries/${encodeURIComponent(documentName)}`);
      setSummariesByDocument(prev => ({
        ...prev,
        [documentName]: response.data,
      }));
    } catch (error) {
      console.error('Błąd przy pobieraniu podsumowań:', error);
      setSummariesByDocument(prev => ({
        ...prev,
        [documentName]: [],
      }));
    } finally {
      setLoadingSummaries(prev => ({ ...prev, [documentName]: false }));
    }
  };

  const getSummaryCount = (documentName: string): number => {
    return summariesByDocument[documentName]?.length || 0;
  };

  const hasLoadedSummaries = (documentName: string): boolean => {
    return summariesByDocument.hasOwnProperty(documentName);
  };

  // Handler do rozwijania/zwijania konkretnego podsumowania
  const toggleSummaryExpand = (summaryId: number) => {
    setExpandedSummaries(prev => ({
      ...prev,
      [summaryId]: !prev[summaryId],
    }));
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
                            <div className="flex-1">
                              <a
                                href={document.name}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-gray-800 hover:underline"
                              >
                                {document.name}
                              </a>
                              <span className="text-sm text-gray-500 ml-2">({document.typ})</span>
                              {hasLoadedSummaries(document.name) && (
                                <span className="text-xs text-green-600 ml-2">
                                  ({getSummaryCount(document.name)} podsumowań)
                                </span>
                              )}
                            </div>
                            <div className="flex gap-2">
                              <button
                                onClick={() => fetchSummariesForDocument(document.name)}
                                disabled={loadingSummaries[document.name]}
                                className="inline-flex items-center px-3 py-1 text-xs font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 disabled:bg-gray-400"
                              >
                                {loadingSummaries[document.name] ? 'Ładowanie...' : 'Sprawdź podsumowania'}
                              </button>
                              <Link
                                to={`/summaries/${encodeURIComponent(document.name)}`}
                                className="inline-flex items-center px-3 py-1 text-xs font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700"
                              >
                                Historia zmian
                              </Link>
                            </div>
                          </div>
                          {/* Wyświetlanie podsumowań */}
                          {summariesByDocument[document.name] && summariesByDocument[document.name].length > 0 && (
                            <div className="mt-3 p-3 bg-gray-100 rounded">
                              <h5 className="font-medium text-gray-700 mb-2">Najnowsze podsumowania:</h5>
                              <ul className="space-y-2">
                                {summariesByDocument[document.name].slice(0, 3).map(summary => (
                                  <li key={summary.id} className="text-sm">
                                    <div className="text-gray-600">{new Date(summary.date).toLocaleString()}</div>
                                    <div className="text-gray-800 break-words">
                                      {expandedSummaries[summary.id]
                                        ? summary.content
                                        : summary.content.length > 100
                                          ? `${summary.content.substring(0, 100)}...`
                                          : summary.content
                                      }
                                      {summary.content.length > 100 && (
                                        <button
                                          className="ml-2 text-blue-600 underline text-xs"
                                          onClick={() => toggleSummaryExpand(summary.id)}
                                        >
                                          {expandedSummaries[summary.id] ? 'Ukryj' : 'Pokaż całość'}
                                        </button>
                                      )}
                                    </div>
                                  </li>
                                ))}
                              </ul>
                              {summariesByDocument[document.name].length > 3 && (
                                <div className="text-xs text-gray-500 mt-2">
                                  ... i {summariesByDocument[document.name].length - 3} więcej
                                </div>
                              )}
                            </div>
                          )}
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