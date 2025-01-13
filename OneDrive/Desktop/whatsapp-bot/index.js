const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const { Boom } = require('@hapi/boom');
const axios = require('axios');
const path = require('path');
const fs = require('fs');
const express = require('express');
const app = express();

// Your backend URL
const BACKEND_URL = 'https://hackmeup.onrender.com';

// Express server setup
const port = process.env.PORT || 10000;
app.get('/', (req, res) => {
    res.send('WhatsApp Bot Server is running!');
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});

async function connectToWhatsApp() {
    // Auth state management
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
        browser: ['WhatsApp Bot', 'Chrome', '1.0.0'],
        connectTimeoutMs: 60000,
        defaultQueryTimeoutMs: 60000,
        keepAliveIntervalMs: 10000
    });

    // Handle connection updates
    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect } = update;

        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect?.error instanceof Boom)?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Connection closed due to ', lastDisconnect?.error?.output || lastDisconnect?.error, ', reconnecting ', shouldReconnect);
            
            if (shouldReconnect) {
                // Add delay before reconnecting
                setTimeout(() => {
                    connectToWhatsApp();
                }, 5000); // 5 second delay
            }
        } else if (connection === 'open') {
            console.log('Connected to WhatsApp!');
        }
    });

    // Credentials updated -- save them
    sock.ev.on('creds.update', saveCreds);

    // Handle incoming messages
    sock.ev.on('messages.upsert', async ({ messages, type }) => {
        try {
            const message = messages[0];
            
            if (!message.message || message.key.fromMe) return;

            const messageText = message.message?.conversation || 
                              message.message?.extendedTextMessage?.text || 
                              '';

            if (messageText.toLowerCase().trim() === '@hackmeup'||messageText.toLowerCase().trim() === '@online'||messageText.toLowerCase().trim() === '@offline') {
                console.log('Received command');
                
                try {
                    // Get data from your backend
                    const response = await axios.get(BACKEND_URL);
                    const hackathonData = response.data.data;

                    // Format the message
                    let replyMessage = '';
                    console.log(hackathonData['data'][0]);
                    const data = hackathonData['data'];
                    let i = 0;
                    
                    for(let temp of data) {
                        if(i === 0) {
                            temp = "Welcome to HackMeUp! Here are the upcoming hackathons:\n\n";
                            replyMessage += temp;
                            i++;
                            continue;
                        }
                        if((temp.toLowerCase().includes("online") && messageText.toLowerCase().trim() === '@offline')||(temp.toLowerCase().includes("offline") && messageText.toLowerCase().trim() === '@online'))
                            continue;
                        if(temp.includes("UTC (UTC)")) {
                            temp = temp.replaceAll("UTC (UTC)", "UTC");
                        }else if (temp.includes("UTC(UTC)")) {
                            temp = temp.replaceAll("UTC(UTC)", "UTC");
                        }
                        temp = String(temp).replaceAll('*', '');
                        replyMessage += (i.toString() + "." + temp + "\n-----------\n");
                        i++;
                    }
                    
                    console.log(replyMessage);
                    
                    // Send the reply
                    await sock.sendMessage(
                        message.key.remoteJid,
                        { text: replyMessage }
                    );

                    console.log('Reply sent successfully');
                } catch (error) {
                    console.error('Error fetching or sending data:', error);
                    
                    // Send error message to user
                    await sock.sendMessage(
                        message.key.remoteJid,
                        { text: 'Sorry, there was an error fetching the hackathon data. Please try again later.' }
                    );
                }
            }
        } catch (error) {
            console.error('Error processing message:', error);
        }
    });

    // Add periodic health check
    setInterval(() => {
        console.log('Bot health check: Running');
    }, 30000); // Every 30 seconds
}

// Create auth_info directory if it doesn't exist
const AUTH_DIR = 'auth_info';
if (!fs.existsSync(AUTH_DIR)) {
    fs.mkdirSync(AUTH_DIR);
}

// Error handling for the Express server
process.on('uncaughtException', (err) => {
    console.error('Uncaught Exception:', err);
});

process.on('unhandledRejection', (err) => {
    console.error('Unhandled Rejection:', err);
});

// Start the bot
connectToWhatsApp();
