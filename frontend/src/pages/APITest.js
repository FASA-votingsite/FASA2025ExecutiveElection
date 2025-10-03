import React, { useState } from 'react';
import { electionsAPI } from '../services/api';

const APITest = () => {
  const [testResult, setTestResult] = useState('');
  const [loading, setLoading] = useState(false);

  const testAPI = async () => {
    setLoading(true);
    setTestResult('Testing...');
    
    try {
      const response = await electionsAPI.getPositions();
      setTestResult(`SUCCESS: Received ${response.data.length} positions\nData: ${JSON.stringify(response.data, null, 2)}`);
    } catch (error) {
      setTestResult(`ERROR: ${error.message}\n${error.response ? `Status: ${error.response.status}\nData: ${JSON.stringify(error.response.data)}` : 'No response from server'}`);
    }
    
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h1>API Connection Test</h1>
      <button onClick={testAPI} disabled={loading}>
        {loading ? 'Testing...' : 'Test API Connection'}
      </button>
      
      <div style={{ marginTop: '20px', whiteSpace: 'pre-wrap', background: '#f5f5f5', padding: '10px', borderRadius: '5px' }}>
        <h3>Test Result:</h3>
        {testResult}
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <h3>Expected API Endpoints:</h3>
        <ul>
          <li><strong>GET</strong> http://localhost:8000/api/elections/</li>
          <li><strong>GET</strong> http://localhost:8000/api/elections/positions/</li>
          <li><strong>GET</strong> http://localhost:8000/api/elections/candidates/</li>
        </ul>
      </div>
    </div>
  );
};

export default APITest;