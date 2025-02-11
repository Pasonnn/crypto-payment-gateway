echo "Starting the Flask server..."
python3 backend/app.py &

echo "Starting the frontend application..."
cd frontend
npm run start
