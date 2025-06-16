import { useState } from 'react';
import { Link } from 'react-router-dom';

interface ScrapedPage {
  id: string;
  name: string;
  url: string;
  lastScraped: string;
  Changes: Change[];
}

interface Change {
  id: string;
  date: string;
  summary: string;
}

const Summary = () => {
  const [pages, setPages] = useState<ScrapedPage[]>([
    {
      id: '1',
      name: 'BIP Urząd Miasta Warszawa',
      url: 'https://bip.um.warszawa.pl',
      lastScraped: '2023-05-15T14:30:00',
      Changes: [
        {
          id: '101',
          date: '2023-05-15T14:30:00',
          summary: 'Aktualizacja danych kontaktowych'
        }
      ]
    },
    {
      id: '2',
      name: 'BIP Ministerstwa Zdrowia',
      url: 'https://bip.mz.gov.pl',
      lastScraped: '2023-05-14T09:45:00',
      Changes: [
        {
          id: '201',
          date: '2023-05-14T09:45:00',
          summary: 'Aktualizacja rozporządzeń'
        }
      ]
    }
  ]);

  const [expandedPageId, setExpandedPageId] = useState<string | null>(null);

  const toggleExpand = (pageId: string) => {
    setExpandedPageId(expandedPageId => expandedPageId === pageId ? null : pageId);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Monitorowane strony BIP</h1>
      <p className="text-gray-600 mb-8">
        Lista scrapowanych stron Biuletynu Informacji Publicznej. Kliknij na pozycję, aby zobaczyć ostatnie zmiany.
      </p>

      <div className="bg-white shadow rounded-lg overflow-hidden">
        <ul className="divide-y divide-gray-200">
          {pages.map(page => (
            <li key={page.id} className="hover:bg-gray-50 transition-colors">
              <div 
                className="px-6 py-4 flex justify-between items-center cursor-pointer"
                onClick={() => toggleExpand(page.id)}
              >
                <div>
                  <h3 className="text-lg font-medium text-gray-800">{page.name}</h3>
                  <p className="text-sm text-gray-500">{page.url}</p>
                </div>
                <div className="flex items-center">
                  <span className="text-sm text-gray-500 mr-4">
                    Ostatnio sprawdzane: {new Date(page.lastScraped).toLocaleString()}
                  </span>
                  <svg
                    className={`w-5 h-5 text-gray-500 transform transition-transform ${
                      expandedPageId === page.id ? 'rotate-180' : ''
                    }`}
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>

              {expandedPageId === page.id && (
                <div className="px-6 pb-4 pt-2 bg-gray-50">
                  <h4 className="font-medium text-gray-700 mb-3">Ostatnie zmiany:</h4>
                  <ul className="space-y-3">
                    {page.Changes.map(change => (
                      <li key={change.id} className="bg-white p-3 rounded shadow-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-800">{change.summary}</span>
                          <span className="text-sm text-gray-500">
                            {new Date(change.date).toLocaleString()}
                          </span>
                        </div>
                       
                      </li>
                    ))}
                  </ul>
                  <div className="mt-4 flex justify-end">
                    <Link
                      to={`/bip/history/${page.id}`}
                      className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Zobacz pełną historię zmian
                    </Link>
                  </div>
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