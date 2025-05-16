#!/bin/bash

echo "Starting LINE Bot locally..."

# Check if python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. Please install Python 3."
    exit 1
fi

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "ngrok could not be found. Please install ngrok for webhook tunneling."
    echo "Visit https://ngrok.com/download for installation instructions."
    echo "Continue without ngrok? (y/n)"
    read continue_without_ngrok
    if [ "$continue_without_ngrok" != "y" ]; then
        exit 1
    fi
fi

# Check if dependencies are installed
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found."
    exit 1
else
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ".env file not found. Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Please edit .env file and add your API keys."
        exit 1
    else
        echo ".env.example not found. Please create a .env file with your API keys."
        exit 1
    fi
fi

# Run the application
echo "Running Flask application..."
python3 app.py &
APP_PID=$!

# Run ngrok if available
if command -v ngrok &> /dev/null; then
    echo "Starting ngrok tunnel on port 3000..."
    ngrok http 3000 &
    NGROK_PID=$!
    
    echo ""
    echo "👉 IMPORTANT: Copy the https URL from ngrok and set it as webhook URL in your LINE Developer Console"
    echo "   Add '/callback' to the end of the URL (e.g., https://xxxx-xxx-xxx-xx-xx.ngrok.io/callback)"
    echo ""
fi

# Handle graceful shutdown
function cleanup {
    echo "Shutting down..."
    if [ ! -z "$APP_PID" ]; then
        kill $APP_PID
    fi
    if [ ! -z "$NGROK_PID" ]; then
        kill $NGROK_PID
    fi
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep script running
echo "Press Ctrl+C to stop the server"
wait 