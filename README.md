# Kimchi-Compass

Kimchi-Compass is a full-stack web application designed for Korean food enthusiasts. It combines the power of React and Flask to provide a rich user experience, allowing users to discover, rate, and review Korean restaurants.

## Features

- **Discover Korean Restaurants**: A curated list of Korean restaurants with detailed information.
- **User Reviews and Ratings**: Users can share their experiences and rate restaurants.
- **User Authentication**: Secure login functionality with Google OAuth 2.0.
- **Responsive UI**: A sleek and responsive design for an optimal user experience on any device.

# GIF
<img src="https://github.com/JazlinBYU/Kimchi-Compass/blob/main/kimchi.gif">

## Tech Stack

- **Frontend**: React, React Router
- **Backend**: Flask, SQLAlchemy, PostgreSQL
- **Authentication**: Google OAuth 2.0
- **State Management**: React Context API
- **Styling**: CSS3

## Getting Started

Follow these instructions to get Kimchi-Compass up and running on your local machine for development and testing purposes.

### Prerequisites

- Node.js
- Python 3
- PostgreSQL

### Installation

#### Frontend

# Clone the repository

git clone https://github.com/JazlinBYU/Kimchi-Compass.git

cd Kimchi-Compass/client

# Install dependencies

npm install

# Start the React development server

npm start

#### Backend

# Navigate to the server directory

cd server

# Set up a Python virtual environment

python -m venv venv
source venv/bin/activate # Unix/Linux/MacOS
venv\Scripts\activate # Windows

# Install dependencies

pip install -r requirements.txt

# Run database migrations

flask db upgrade

# Start the Flask server

flask run

# Configuration

Create a .env file in the server directory with the following format:

DATABASE_URL="postgresql://username:password@localhost:5432/kimchi_compass"
SECRET_KEY="your_secret_key"
GOOGLE_CLIENT_ID="your_google_client_id"
GOOGLE_CLIENT_SECRET="your_google_client_secret"

# Seeding the Database

To seed the database with initial data:

python seed.py

# Usage

The application will be running on http://localhost:3000 for the frontend and http://localhost:5000 for the backend.
