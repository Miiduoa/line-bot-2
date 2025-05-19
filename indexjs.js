const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware for parsing JSON
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

// Simple home route
app.get('/', (req, res) => {
  res.status(200).send('Hello from LINE Bot!');
});

// Webhook endpoint
app.post('/callback', (req, res) => {
  console.log('Received webhook:', JSON.stringify(req.body));
  // Just acknowledge receipt
  res.status(200).send('OK');
});

// For local testing
if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
}

// For Vercel
module.exports = app; 