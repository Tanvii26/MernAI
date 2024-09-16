import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Import the CSS file

function App() {
    const [reqt, setReqt] = useState('');
    const [score, setScore] = useState({}); // Initialize as an empty object

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/api/profile-score', {
                requirement: reqt,
            });
            console.log(response.data);
            setScore(response.data || {}); // Set score or default to empty object if undefined
        } catch (error) {
            console.error("Error fetching profile score", error);
            setScore({}); // Reset score on error
        }
    };

    return (
        <div className='body'>
            <h1>Profile Score Matching</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="requirement">Interview Requirement:</label>
                    <input
                        type="text"
                        id="requirement"
                        value={reqt}
                        onChange={(e) => setReqt(e.target.value)}
                    />
                </div>
                
                <button type="submit">Compute Score</button>
            </form>

            {Object.keys(score).length > 0 && (
                <div className="grid-container">
                    {Object.entries(score).map(([expert, candidates], index) => (
                        <div key={index} className="expert-card">
                            <h3>Expert: {expert}</h3>
                            <div className="candidate-grid">
                                {candidates.map((item, idx) => (
                                    <div key={idx} className="candidate-card">
                                        <strong>Candidate:</strong> {item.Candidate} <br />
                                        <strong>Score:</strong> {item['Relevancy Score'].toFixed(5)}
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default App;
