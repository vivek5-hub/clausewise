// server.js

const express = require('express');
const compression = require('compression'); // Step 1: Require compression

const app = express();

// Step 2: Use the compression middleware
app.use(compression());

// Your existing middleware and routes
app.get('/', (req, res) => {
    res.send('Hello, World!');
});

// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
