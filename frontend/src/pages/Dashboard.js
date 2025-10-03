import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { electionsAPI, votesAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [positions, setPositions] = useState([]);
  const [myVotes, setMyVotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [votingInProgress, setVotingInProgress] = useState({});

  useEffect(() => {
    fetchElectionData();
    fetchMyVotes();
  }, []);

  const fetchElectionData = async () => {
    try {
      console.log('Fetching election data from positions endpoint...');
      const positionsResponse = await electionsAPI.getPositions();
      
      console.log('Positions with candidates:', positionsResponse.data);

      /*  
      const activePositions = positionsResponse.data.filter(position => 
        position.election && position.election.is_active
      );*/
      
      // Combine positions with their candidates
      const positionsWithCandidates = positionsResponse.data; 

      console.log('Final positions data:', positionsWithCandidates);
      if (positionsWithCandidates.length === 0) {
        setError('No active election found. check if an election is marked active in the admin panel.');
      } else {
        setPositions(positionsWithCandidates);
        setError('');
      }
    } catch (error) {
      console.error('Error fetching election data:', error);
      setError('Failed to load election data.');
    } finally {
      setLoading(false);
    }
  };

  const fetchMyVotes = async () => {
    try {
      const response = await votesAPI.getMyVotes();
      setMyVotes(response.data);
    } catch (error) {
      console.error('Error fetching votes:', error);
      setMyVotes([]);
    }
  };

  // Check if user has voted for a specific position
  const hasVotedForPosition = (positionId) => {
    return myVotes.some(vote => {
      // Handle different data structures from API
      if (vote.position_id) {
        return vote.position_id === positionId;
      } else if (typeof vote.position === 'object') {
        return vote.position.id === positionId;
      } else {
        // If position is just a string title, we need to find the position ID
        const position = positions.find(p => p.title === vote.position);
        return position ? position.id === positionId : false;
      }
    });
  };

  // Get the candidate the user voted for in a specific position
  const getVotedCandidateForPosition = (positionId) => {
    const vote = myVotes.find(vote => {
      if (vote.position_id) {
        return vote.position_id === positionId;
      } else if (typeof vote.position === 'object') {
        return vote.position.id === positionId;
      } else {
        const position = positions.find(p => p.title === vote.position);
        return position ? position.id === positionId : false;
      }
    });
    return vote ? vote.candidate : null;
  };

  const handleVote = async (positionId, candidateId, candidateName) => {
    if (!window.confirm(`Are you sure you want to vote for ${candidateName}? This action cannot be undone.`)) {
      return;
    }

     // Set voting in progress for this specific position
    setVotingInProgress(prev => ({ ...prev, [positionId]: true }));

    try {
      await votesAPI.castVote({
        position_id: positionId,
        candidate_id: candidateId
      });
      
      alert('Vote cast successfully!');

       // Refresh the data to update the UI
      await Promise.all([fetchMyVotes(), fetchElectionData()]);
      
    } catch (error) {
      const errorMessage = error.response?.data?.error || 'Failed to cast vote. Please try again.';
      alert(errorMessage);
    } finally {
      // Clear voting in progress for this position
      setVotingInProgress(prev => ({ ...prev, [positionId]: false }));
    }
  };


  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="loading-spinner">Loading Election Data...</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
            <div>
            <img src="/logo512.png" alt="Uniben" />
            <img src="/logo192.png" alt="FASA" />
            </div>
          <div>
            <h1>Faculty of Art Elections</h1>
            <p className="election-subtitle">2025 Executive Elections</p>
          </div>
          <div className="user-info">
            <div className="user-details">
              <span className="welcome-text">Welcome, {user.full_name}</span>
              <span className="matric-number">{user.matric_number}</span>
            </div>
            <button onClick={logout} className="logout-button">Logout</button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="welcome-section">
          <h2>Cast Your Vote</h2>
          <p>Vote for each position below. You can only vote once per position.</p>
          
          {myVotes.length > 0 && (
            <div className="voted-notice">
              <strong>You have voted for {myVotes.length} position(s).</strong>
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            {error}
            <button onClick={fetchElectionData} className="retry-button">
              Retry
            </button>
          </div>
        )}

        {!error && positions.length === 0 && (
          <div className="no-data-message">
            <h3>No Election Data Available</h3>
            <p>There are no active elections or positions to display.</p>
          </div>
        )}


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
                              {candidate.photo_url ? (
                                <img 
                                  src={`http://localhost:8000${candidate.photo_url}`} 
                                  alt={candidate.student_name}
                                  className="candidate-photo"
                                  onError={(e) => {
                                    // If image fails to load, hide it and show fallback
                                    e.target.style.display = 'none';
                                  }}
                                />
                              ) : (
                                <div className="candidate-photo-placeholder">
                                  {candidate.student_name.split(' ').map(n => n[0]).join('')}
                                </div>
                              )}
                              <div className="candidate-details">
                                <h4>{candidate.student_name}</h4>
                              </div>
                            </div>
                          </div>

                          <div className="candidate-actions">
                            {hasVoted ? (
                              isVotedCandidate ? (
                                <button className="vote-button user-vote-button" disabled>
                                  Your Vote ✓
                                </button>
                              ) : (
                                <button className="vote-button disabled" disabled>
                                  Vote
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

        {myVotes.length > 0 && (
            <div className="voted-notice">
              <strong>You voted for {myVotes.length} position(s). Thank you for participating!</strong>
            </div>
          )}

      </main>
    </div>
  );
};

export default Dashboard;