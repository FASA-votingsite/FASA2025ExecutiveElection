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





        {!error && positions.length > 0 && (
          <div className="positions-grid">
            {positions.map(position => {
              const hasVoted = hasVotedForPosition(position.id);
              const votedCandidate = getVotedCandidateForPosition(position.id);
              const isVoting = votingInProgress[position.id] || false;
              
              return (
                <div key={position.id} className={`position-card ${hasVoted ? 'voted' : ''}`}>
                  <div className="position-header">
                    <h3>{position.title}</h3>
                    {hasVoted && (
                      <span className="voted-badge">✓ Voted</span>
                    )}
                  </div>
                  <p className="position-description">{position.description}</p>
                  
                  <div className="candidates-list">
                    {position.candidates && position.candidates.map(candidate => {
                      const isVotedCandidate = hasVoted && votedCandidate === candidate.student_name;

                      return (
                        <div key={candidate.id} className={`candidate-card ${isVotedCandidate ? 'user-vote' : ''}`}>
                          <div className="candidate-info">
                            <div className="candidate-header">
                              {candidate.photo_url && (
                                <img 
                                  src={`http://localhost:8000${candidate.photo_url}`} 
                                  alt={candidate.student_name}
                                  className="candidate-photo"
                                  onError={(e) => {
                                    e.target.style.display = 'none';
                                  }}
                                />
                              )}
                              <div className="candidate-details">
                                <h4>{candidate.student_name}</h4>
                                <p className="candidate-department">{candidate.student_department}</p>
                              </div>
                            </div>
                            <p className="candidate-manifesto">{candidate.manifesto}</p>
                          </div>

                          <div className="candidate-actions">
                            {hasVoted ? (
                              isVotedCandidate ? (
                                <button className="vote-button user-vote-button" disabled>
                                  Your Vote ✓
                                </button>
                              ) : (
                                <button className="vote-button disabled" disabled>
                                  Already Voted
                                </button>
                              )
                            ) : (
                              <button
                                onClick={() => handleVote(position.id, candidate.id, candidate.student_name)}
                                disabled={isVoting}
                                className={`vote-button ${isVoting ? 'voting' : ''}`}
                              >
                                {isVoting ? 'Voting...' : 'Vote'}
                              </button>
                            )}
                          </div>
                        </div>

                         );
                    })}
                    
                    {(!position.candidates || position.candidates.length === 0) && (
                      <div className="no-candidates">
                        No candidates available for this position.
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}


