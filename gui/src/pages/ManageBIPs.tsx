import { useState, type ChangeEvent, type FormEvent } from 'react';

interface FormData {
  url: string;
  scheduleTime: string;
  interval: 'MINUTELY' | 'HOURLY' | 'DAILY';
}

function ManageBIPs() {
  const [formData, setFormData] = useState<FormData>({
    url: '',
    scheduleTime: '',
    interval: 'MINUTELY',
  });

  const [jsonString, setJsonString] = useState('');
  const [responseMessage, setResponseMessage] = useState('');

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const dataToSend = {
      url: formData.url,
      schedule_time: parseInt(formData.scheduleTime, 10),
      interval: formData.interval,
    };

    const json = JSON.stringify(dataToSend, null, 2);
    console.log('Wysyłany JSON:', json);
    setJsonString(json);

    try {
      const response = await fetch('http://localhost:5000/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      });

      if (response.ok) {
        const result = await response.json();
        setResponseMessage(`Sukces! Serwer zwrócił: ${JSON.stringify(result)}`);
      } else {
        const errorText = await response.text();
        setResponseMessage(`Błąd: ${response.status} - ${errorText}`);
      }
    } catch (error: unknown) {
      const errMsg = error instanceof Error ? error.message : 'Nieznany błąd';
      console.error('Błąd połączenia z API:', error);
      setResponseMessage(`Błąd połączenia: ${errMsg}`);
    }

    setFormData({
      url: '',
      scheduleTime: '',
      interval: 'MINUTELY',
    });
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>Zarządzaj listą BIP-ów</h1>
      <p>Dodaj, edytuj i usuwaj źródła.</p>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>
            URL strony:
            <input
              type="text"
              name="url"
              value={formData.url}
              onChange={handleChange}
              required
              style={{
                display: 'block',
                border: '1px solid black',
                padding: '5px',
                marginTop: '5px',
                width: '100%',
                maxWidth: '400px',
              }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            Co ile czasu scrapować:
            <input
              type="number"
              name="scheduleTime"
              value={formData.scheduleTime}
              onChange={handleChange}
              min="1"
              required
              style={{
                display: 'block',
                border: '1px solid black',
                padding: '5px',
                marginTop: '5px',
                width: '100%',
                maxWidth: '200px',
              }}
            />
          </label>
        </div>

        <div style={{ marginBottom: '10px' }}>
          <label>
            Jednostka czasu:
            <select
              name="interval"
              value={formData.interval}
              onChange={handleChange}
              style={{
                display: 'block',
                border: '1px solid black',
                padding: '5px',
                marginTop: '5px',
                width: '100%',
                maxWidth: '200px',
              }}
            >
              <option value="MINUTELY">Minuty</option>
              <option value="HOURLY">Godziny</option>
              <option value="DAILY">Dni</option>
            </select>
          </label>
        </div>

        <button
          type="submit"
          className="rounded-md"
          style={{
            backgroundColor: 'blue',
            color: 'white',
            padding: '10px 20px',
            cursor: 'pointer',
            fontSize: '16px',
          }}
        >
          Dodaj
        </button>
      </form>

      {jsonString && (
        <div style={{ marginTop: '20px' }}>
          <h2>JSON wysłany do API:</h2>
          <pre>{jsonString}</pre>
        </div>
      )}

      {responseMessage && (
        <div style={{ marginTop: '20px' }}>
          <h2>Odpowiedź z serwera:</h2>
          <pre>{responseMessage}</pre>
        </div>
      )}
    </div>
  );
}

export default ManageBIPs;
