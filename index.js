const express = require('express');
const line = require('@line/bot-sdk');
require('dotenv').config();

// LINE Bot config
const config = {
  channelAccessToken: process.env.LINE_CHANNEL_ACCESS_TOKEN || '',
  channelSecret: process.env.LINE_CHANNEL_SECRET || ''
};

// Create LINE SDK client
const client = new line.Client(config);
const app = express();

// Register the middleware for parsing LINE webhook requests
app.use('/webhook', line.middleware(config));

// Simple home route
app.get('/', (req, res) => {
  res.status(200).send('LINE Bot is up and running!');
});

// Webhook endpoint
app.post('/webhook', async (req, res) => {
  try {
    const events = req.body.events;
    console.log('Events received:', JSON.stringify(events));
    
    // Process all events in parallel
    await Promise.all(events.map(handleEvent));
    
    // Return a successful response
    res.status(200).end();
  } catch (err) {
    console.error('Error handling webhook:', err);
    res.status(500).end();
  }
});

// Event handler function
async function handleEvent(event) {
  if (event.type !== 'message' || event.message.type !== 'text') {
    // Handle non-text messages separately
    return handleNonTextContent(event);
  }

  // Handle text messages
  const { replyToken } = event;
  const { text } = event.message;
  
  // Echo the received message for now
  const echo = { type: 'text', text: `你說: ${text}` };
  
  // Add some simple responses
  if (text.includes('你好') || text.includes('hello')) {
    return client.replyMessage(replyToken, {
      type: 'text',
      text: '你好！我是你的LINE機器人。有什麼我可以幫你的嗎？'
    });
  }
  
  if (text.includes('幫助') || text.includes('help')) {
    return client.replyMessage(replyToken, {
      type: 'text',
      text: '我可以回應你的訊息。試著傳送"你好"、"help"或任何文字給我！'
    });
  }
  
  // Default echo response
  return client.replyMessage(replyToken, echo);
}

// Handle non-text content
function handleNonTextContent(event) {
  const { replyToken } = event;
  let responseMessage;
  
  switch (event.message.type) {
    case 'image':
      responseMessage = { type: 'text', text: '收到你的圖片了！' };
      break;
    case 'video':
      responseMessage = { type: 'text', text: '收到你的影片了！' };
      break;
    case 'audio':
      responseMessage = { type: 'text', text: '收到你的語音了！' };
      break;
    case 'sticker':
      responseMessage = {
        type: 'sticker',
        packageId: '11537',
        stickerId: '52002734'
      };
      break;
    default:
      responseMessage = { type: 'text', text: '收到你的訊息了！' };
  }
  
  return client.replyMessage(replyToken, responseMessage);
}

// For local testing
if (require.main === module) {
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
}

// For Vercel
module.exports = app; 