const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const { Boom } = require('@hapi/boom');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

// Your backend URL
const BACKEND_URL = 'https://hackmeup.onrender.com';

async function connectToWhatsApp() {
    // Auth state management
    const { state, saveCreds } = await useMultiFileAuthState('auth_info');
    
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true, // Print QR in terminal for scanning
    });

    // Handle connection updates
    sock.ev.on('connection.update', async (update) => {
        const { connection, lastDisconnect } = update;

        if (connection === 'close') {
            const shouldReconnect = (lastDisconnect?.error instanceof Boom)?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Connection closed due to ', lastDisconnect?.error, ', reconnecting ', shouldReconnect);
            
            if (shouldReconnect) {
                connectToWhatsApp();
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

            if (messageText.toLowerCase().trim() === '@hackmeup') {
                console.log('Received @hackmeup command');
                
                try {
                    // Get data from your backend
                    const response = await axios.get(BACKEND_URL);
                    const hackathonData = response.data.data;

                    // Format the message
                    let replyMessage = '';
                    console.log(hackathonData['data'][0]);
                    const data = hackathonData['data'];
                    let i=0;
                    for(let temp of data){
                        if(i==0){
                            temp="Welcome to HackMeUp! Here are the upcoming hackathons:\n\n";+temp;
                            replyMessage+=temp;
                            i++;
                            continue;
                        }
                        if(temp.includes("UTC (UTC)")){
                            temp = temp.replace("UTC (UTC)", "UTC");
                        }
                        temp = String(temp).replaceAll('*', '');
                        replyMessage+=(i.toString()+"."+temp+"\n-----------\n");
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
}

// Create auth_info directory if it doesn't exist
const AUTH_DIR = 'auth_info';
if (!fs.existsSync(AUTH_DIR)) {
    fs.mkdirSync(AUTH_DIR);
}

// Start the bot
connectToWhatsApp();
