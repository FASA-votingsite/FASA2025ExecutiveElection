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
  const [voting, setVoting] = useState(false);

  useEffect(() => {
    fetchElectionData();
    fetchMyVotes();
  }, []);

  const fetchElectionData = async () => {
    try {
      const [positionsResponse, candidatesResponse] = await Promise.all([
        electionsAPI.getPositions(),
        electionsAPI.getCandidates()
      ]);
      
      // Combine positions with their candidates
      const positionsWithCandidates = positionsResponse.data.map(position => ({
        ...position,
        candidates: candidatesResponse.data.filter(candidate => 
          candidate.position === position.id
        )
      }));
      
      setPositions(positionsWithCandidates);
      setError('');
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
    }
  };

  const hasVotedForPosition = (positionId) => {
    return myVotes.some(vote => vote.position === positionId);
  };

  const getVotedCandidate = (positionId) => {
    const vote = myVotes.find(vote => vote.position === positionId);
    return vote ? vote.candidate : null;
  };

  const handleVote = async (positionId, candidateId, candidateName) => {
    if (!window.confirm(`Are you sure you want to vote for ${candidateName}? This action cannot be undone.`)) {
      return;
    }

    setVoting(true);
    try {
      await votesAPI.castVote({
        position_id: positionId,
        candidate_id: candidateId
      });
      
      alert('Vote cast successfully!');
      // Refresh votes and election data
      await fetchMyVotes();
      await fetchElectionData();
    } catch (error) {
      alert(error.response?.data?.error || 'Failed to cast vote. Please try again.');
    } finally {
      setVoting(false);
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
              <strong>You have voted for {myVotes.length} position(s). Thank you for participating!</strong>
            </div>
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="positions-grid">
          {positions.map(position => {
            const hasVoted = hasVotedForPosition(position.id);
            const votedCandidate = getVotedCandidate(position.id);
            
            return (
              <div key={position.id} className="position-card">
                <div className="position-header">
                  <h3>{position.title}</h3>
                  {hasVoted && (
                    <span className="voted-badge">Voted ✓</span>
                  )}
                </div>
                <p className="position-description">{position.description}</p>
                
                <div className="candidates-list">
                  {position.candidates.map(candidate => (
                    <div key={candidate.id} className="candidate-card">
                      <div className="candidate-info">
                        <h4>{candidate.student_name}</h4>
                        <p className="candidate-department">{candidate.student_department}</p>
                        <p className="candidate-manifesto">{candidate.manifesto}</p>
                      </div>
                      <div className="candidate-actions">
                        {hasVoted ? (
                          votedCandidate === candidate.student_name ? (
                            <button className="vote-button voted" disabled>
                              Your Vote
                            </button>
                          ) : (
                            <button className="vote-button disabled" disabled>
                              Voted
                            </button>
                          )
                        ) : (
                          <button
                            onClick={() => handleVote(position.id, candidate.id, candidate.student_name)}
                            disabled={voting}
                            className="vote-button"
                          >
                            {voting ? 'Voting...' : 'Vote'}
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;