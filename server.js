const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 3000;

const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY; // Your OpenAI API key
const TELEGRAM_API_URL = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`;

app.use(bodyParser.json());

app.post('/api/message', async (req, res) => {
  const { message, user_id } = req.body; // Expecting message and user ID in the request

  try {
    // First, get a response from OpenAI GPT model
    const openAIResponse = await axios.post(
      'https://api.openai.com/v1/completions',
      {
        model: 'text-davinci-003', // Change as necessary to use another model
        prompt: message,
        max_tokens: 150,
      },
      {
        headers: {
          'Authorization': `Bearer ${OPENAI_API_KEY}`,
          'Content-Type': 'application/json',
        }
      }
    );

    // Now send the OpenAI response to Telegram
    const openAIMessage = openAIResponse.data.choices[0].text.trim();

    const telegramResponse = await axios.post(TELEGRAM_API_URL, {
      chat_id: user_id, // Use the user_id from request to send to correct chat
      text: openAIMessage,
    });

    res.status(200).send('Message sent to Telegram');
  } catch (error) {
    console.error('Error:', error);
    res.status(500).send('Failed to process message');
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
