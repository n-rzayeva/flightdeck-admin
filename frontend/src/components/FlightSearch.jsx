import { useState } from "react";
import axios from "axios";


const FlightSearch = () => {
  const [flightNumber, setFlightNumber] = useState("");
  const [flightData, setFlightData] = useState(null);
  const [error, setError] = useState("");

  const fetchFlight = async () => {
    setError(""); 
    setFlightData(null); 

    try {
      const response = await axios.get(`http://127.0.0.1:8081/flights/${flightNumber}`);
      setFlightData(response.data);
    } catch (err) {
      setError("Flight not found or server error.");
    }
  };

  return (
    <div className="container">
      <h2>Get information about your flight</h2>
      <input
        type="text"
        placeholder="Enter flight number"
        value={flightNumber}
        onChange={(e) => setFlightNumber(e.target.value)}
      />
      <button onClick={fetchFlight}>Search</button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {flightData && (
        <table border="1">
          <thead>
            <tr>
              <th>Flight Number</th>
              <th>Departure Airport</th>
              <th>Arrival Airport</th>
              <th>Scheduled Time</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{flightData.flight_number}</td>
              <td>{flightData.departure_airport}</td>
              <td>{flightData.arrival_airport}</td>
              <td>{flightData.scheduled_time}</td>
              <td>{flightData.status}</td>
            </tr>
          </tbody>
        </table>
      )}
    </div>
  );
};

export default FlightSearch;
