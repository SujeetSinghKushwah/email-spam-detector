import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!message) return alert("Please enter some text!");
    
    setLoading(true);
    try {
      // Flask server ka address
      const response = await axios.post('https://email-spam-detector-30f1.onrender.com', {
        message: message
      });
      setResult(response.data.prediction);
    } catch (error) {
      alert("Error: Kya Backend start hai?");
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <div className="container">
        <h1>📧 Email Spam Detector</h1>
        <p>Enter the message below to check if it's Spam or Safe.</p>
        
        <textarea 
          placeholder="Paste message here..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        
        <button onClick={handlePredict} disabled={loading}>
          {loading ? "Analyzing..." : "Check Message"}
        </button>

        {result !== null && (
          <div className={`result-box ${result === 1 ? 'spam' : 'ham'}`}>
            {result === 1 ? "🚨 Warning: This is a SPAM!" : "✅ Relax: This is SAFE."}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
