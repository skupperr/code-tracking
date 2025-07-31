const express = require('express');
const app = express();
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');
dotenv.config();

const dbService = require('./db_service');

const db = dbService.getDbServiceInstance();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// ✅ Serve main HTML project from /Frontend
app.use(express.static(path.join(__dirname, '../Frontend')));
app.use(express.static(path.join(__dirname, '../Frontend/lib')));

// ✅ Serve built React app from /chat
app.use('/chat', express.static(path.join(__dirname, '../Frontend/chat')));

// Serve Marketplace files
app.use('/marketplace', express.static(path.join(__dirname, '../Frontend')));


// ✅ Handle React internal routes
app.get('/chat/*', (req, res) => {
    res.sendFile(path.join(__dirname, '../Frontend/chat/index.html'));
});

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../Frontend/web page/LoginRegistrationPage.html'));
});

app.use(express.static(path.join(__dirname, '../Frontend/web page')));


// app.post('/filterFriedPosts', async (req, res) => {
//     const { category } = req.body;
//     const userId = 6; // Assume this is the logged-in user's ID. You may replace it with a session-based ID.
//     const db = dbService.getDbServiceInstance();
//     try {
//         let posts;
//         if (category === 'friends') {
//             posts = db.getFriendPosts(userId);
//         } else {
//             // handle other categories or default post fetch
//             posts = db.getAllPosts(); // Or however you fetch all posts
//         }
... (truncated for brevity)