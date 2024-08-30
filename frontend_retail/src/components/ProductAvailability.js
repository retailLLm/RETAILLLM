import React, { useState } from 'react';
import axios from 'axios';
import { Container, TextField, Button, Typography, Paper, Box, Avatar } from '@mui/material';
import './ProductAvailability.css';

const ProductAvailability = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  const handleSendMessage = async () => {
    if (message.trim()) {
      const newMessage = { user: 'Salesperson', text: message };
      setChatHistory(prevChatHistory => [...prevChatHistory, newMessage]);

      // Send message to backend
      try {
        const response = await axios.post('http://localhost:8000/query', 
          { query: message },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        // Extracting reply from response
        const botReply = { user: 'Bot', text: response.data.reply };
        setChatHistory(prevChatHistory => [...prevChatHistory, botReply]);
        
        // Displaying SQL results if available
        if (response.data.results) {
          response.data.results.forEach(result => {
            const dbResponse = { user: 'Bot', text: formatDBResponse(result) };
            setChatHistory(prevChatHistory => [...prevChatHistory, dbResponse]);
          });
        }
      } catch (error) {
        console.error("Error:", error);  
        const botReply = { user: 'Bot', text: 'Sorry, something went wrong. Please try again.' };
        setChatHistory(prevChatHistory => [...prevChatHistory, botReply]);
      }

      setMessage(''); // Clear input field after sending message
    }
  };

  // Helper function to format database query results
  const formatDBResponse = (result) => {
    return `SQLResult: ${JSON.stringify(result)}`;
  };

  return (
    <div className="root">
      <Container maxWidth="sm">
        <Paper elevation={3} className="paper">
          <div className="header">
            <img src="https://static2.bigstockphoto.com/7/6/4/large2/467362341.jpg" alt="store icon" />
            <Typography variant="h4" align="center">Salesperson Assistant</Typography>
          </div>
          <Box mt={3} mb={3}>
            <div className="chatBox">
              {chatHistory.map((chat, index) => (
                <div key={index} className={`chatMessage ${chat.user === 'Salesperson' ? 'salespersonMessage' : 'botMessage'}`}>
                  <Avatar className="avatar" src={chat.user === 'Salesperson' ? "https://img.icons8.com/color/48/000000/user-male.png" : "https://www.shutterstock.com/image-vector/green-robot-chatbot-template-chat-260nw-2473977839.jpg"} />
                  <Typography variant="body1" style={{ fontWeight: chat.user === 'Salesperson' ? 'bold' : 'normal' }}>
                    {chat.user}: {chat.text}
                  </Typography>
                </div>
              ))}
            </div>
            <TextField
              fullWidth
              variant="outlined"
              label="Type your message..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              className="textField"
            />
            <Button
              fullWidth
              variant="contained"
              color="primary"
              className="button"
              onClick={handleSendMessage}
            >
              Send
            </Button>
          </Box>
        </Paper>
      </Container>
    </div>
  );
};

export default ProductAvailability;
