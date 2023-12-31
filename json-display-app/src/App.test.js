import React, { useEffect, useState } from 'react';

const SERVER_URL = 'http://localhost:3001/data'; // URL for the JSON server

const waitTime = 2 * 60 * 1000; // 2 minutes in milliseconds

function App() {
  const [jsonData, setJsonData] = useState([]);

  // Function to fetch JSON data and update state
  const fetchJsonData = async () => {
    try {
      // Fetch JSON data from the server using the fetch API
      const response = await fetch(SERVER_URL);
      const data = await response.json();
      console.log(data); // Add this line to inspect the data
      setJsonData(data);
    } catch (error) {
      console.error('Error fetching JSON data:', error);
    }
  };
  

  // Function to get current time in "HH:mm:ss AM/PM" format
  const getCurrentTime = () => {
    const currentTime = new Date();
    return currentTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  };

  // Fetch JSON data on component mount and set up interval to update data every waitTime
  useEffect(() => {
    fetchJsonData();
    const interval = setInterval(fetchJsonData, waitTime);

    // Clear the interval when the component is unmounted
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>JSON Data Display</h1>
      <p>Current Time: {getCurrentTime()}</p>
      <div>
        {Array.isArray(jsonData) ? (
          jsonData.map((entry, index) => (
            <div key={index}>
              {entry.sensor_name === 'unknown' ? (
                <p>{entry.info}</p>
              ) : (
                <p>
                  Sensor: {entry.sensor_name}, Temperature: {entry.temperature}, Humidity: {entry.humidity}
                </p>
              )}
            </div>
          ))
        ) : (
          <p>Loading data...</p>
        )}
      </div>
    </div>
  );
}

export default App;
