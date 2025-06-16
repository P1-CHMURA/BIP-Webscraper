import { useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';

interface Change {
  id: string;
  date: string;
  summary: string;
  fullContent?: string; 
}

interface ScrapedPage {
  id: string;
  name: string;
  url: string;
  allChanges: Change[]; 
}

const BipHistoryPage = () => {
  const { id } = useParams<{ id: string }>();
  
  const mockPages: ScrapedPage[] = [
    {
      id: '1',
      name: 'BIP Urząd Miasta Warszawa',
      url: 'https://bip.um.warszawa.pl',
      allChanges: [
        {
          id: '101',
          date: '2023-05-15T14:30:00',
          summary: 'Aktualizacja danych kontaktowych',
          fullContent: 'Zmieniono dane kontaktowe: nowy numer telefonu 22 111 11 11...'
        },
        {
          id: '100',
          date: '2023-05-14T10:15:00',
          summary: 'Nowe ogłoszenie o przetargu',
          fullContent: 'Opublikowano nowe ogłoszenie o przetargu nr 1234/2023...'
        },
        {
          id: '99',
          date: '2023-05-10T09:20:00',
          summary: 'Aktualizacja struktur organizacyjnych',
          fullContent: 'Zmieniono strukturę departamentów w urzędzie miasta...'
        }
      ]
    },
   
  ];

  const currentPage = mockPages.find(page => page.id === id);

  if (!currentPage) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white shadow rounded-lg p-6">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">Strona nie znaleziona</h1>
          <p className="text-gray-600">Wybrana strona BIP nie istnieje w naszej bazie.</p>
          <Link 
            to="/podsumowania" 
            className="mt-4 inline-block text-blue-600 hover:text-blue-800"
          >
            Powrót do listy stron
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link 
          to="/podsumowania" 
          className="inline-flex items-center text-blue-600 hover:text-blue-800"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Powrót do listy stron
        </Link>
      </div>

      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        Pełna historia zmian: {currentPage.name}
      </h1>
      <a 
        href={currentPage.url} 
        target="_blank" 
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline mb-6 inline-block"
      >
        {currentPage.url}
      </a>

      <div className="bg-white shadow rounded-lg overflow-hidden">
        <ul className="divide-y divide-gray-200">
          {currentPage.allChanges.map(change => (
            <li key={change.id} className="p-6 hover:bg-gray-50">
              <div className="flex flex-col md:flex-row md:justify-between md:items-start">
                <div className="mb-4 md:mb-0">
                  <h3 className="text-lg font-medium text-gray-800">{change.summary}</h3>
                  
                </div>
                <span className="text-sm text-gray-500 whitespace-nowrap">
                  {new Date(change.date).toLocaleString()}
                </span>
              </div>
              
              {change.fullContent && (
                <div className="mt-4 p-4 bg-gray-50 rounded-md">
                  <h4 className="font-medium text-gray-700 mb-2">Szczegóły zmian:</h4>
                  <p className="text-gray-600 whitespace-pre-line">{change.fullContent}</p>
                </div>
              )}
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-6 text-sm text-gray-500">
        Liczba zmian w historii: {currentPage.allChanges.length}
      </div>
    </div>
  );
};

export default BipHistoryPage;