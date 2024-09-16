// /server/server.js
const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const FASTAPI_URL = 'http://localhost:8000';  // The URL of your FastAPI service

// API route to get profile score from FastAPI
app.post('/api/profile-score', async (req, res) => {
    try {
        const { requirement } = req.body;
        console.log("calling api/match")
        // Send request to FastAPI service
        const response = await axios.post(`${FASTAPI_URL}/compute_profile_score/`, {
                requirement
        });
        
        res.json(response.data.results);
    } catch (error) {
        res.status(500).json({ error: 'Error connecting to FastAPI service' });
    }
});

const PORT = 5000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
