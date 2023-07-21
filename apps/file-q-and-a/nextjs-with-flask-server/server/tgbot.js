const TelegramBot = require('node-telegram-bot-api');
const serverless = require('serverless-http');
const express = require('express');

const app = express();
const bot = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN);

app.use(express.json());

app.post('/webhook', (req, res) => {
  const { message } = req.body;

  if (message) {
    const chatId = message.chat.id;
    const text = message.text;

    // Determine the appropriate response based on the incoming message
    const response = 'Hello, world!';

    // Send the response back to the user
    bot.sendMessage(chatId, response);
  }

  res.sendStatus(200);
});

module.exports.handler = serverless(app);