import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
from datetime import datetime
from database import db_manager

app = Flask(__name__)

# Path configurations
LOG_FILE = 'door_access.log'
KNOWN_FACES_DIR = 'known_faces'

@app.route('/')
def index():
    """Main dashboard page showing recent access logs"""
    logs = read_access_logs()
    users = get_registered_users()
    return render_template('index.html', logs=logs[-20:][::-1], users=users)  # Show last 20 logs, newest first

@app.route('/logs')
def logs():
    """API endpoint to get all logs as JSON"""
    logs = read_access_logs()
    return jsonify(logs)

@app.route('/users')
def users():
    """Page to manage registered users"""
    users = get_registered_users()
    return render_template('users.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    """API endpoint to add a new user"""
    # In a real implementation, this would integrate with the registration system
    # For now, we'll just return a success message
    return jsonify({"status": "success", "message": "User would be added in a full implementation"})

@app.route('/delete_user/<username>')
def delete_user(username):
    """Delete a registered user"""
    try:
        # Delete user image and encoding files
        image_path = os.path.join(KNOWN_FACES_DIR, f"{username}.jpg")
        encoding_path = os.path.join(KNOWN_FACES_DIR, f"{username}_encoding.npy")
        
        if os.path.exists(image_path):
            os.remove(image_path)
        
        if os.path.exists(encoding_path):
            os.remove(encoding_path)
            
        # Also delete user from database
        db_manager.delete_user(username)
            
        return jsonify({"status": "success", "message": f"User {username} deleted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def read_access_logs():
    """Read access logs from the database"""
    logs = []
    db_logs = db_manager.get_recent_access_logs(100)  # Get last 100 logs
    for db_log in db_logs:
        logs.append({
            'timestamp': db_log[1],  # timestamp
            'event': db_log[2],      # event_type
            'person': db_log[3] or "N/A"  # person_name
        })
    return logs

def get_registered_users():
    """Get list of registered users from database"""
    db_users = db_manager.get_all_users()
    users = []
    if os.path.exists(KNOWN_FACES_DIR):
        for file in os.listdir(KNOWN_FACES_DIR):
            if file.endswith('.jpg') and not file.startswith('.'):
                username = os.path.splitext(file)[0]
                # Check if encoding file exists
                encoding_file = f"{username}_encoding.npy"
                trained = encoding_file in os.listdir(KNOWN_FACES_DIR)
                users.append({
                    'name': username,
                    'image': file,
                    'trained': trained
                })
    # Add database information to users
    for db_user in db_users:
        # Check if user is already in the list
        found = False
        for user in users:
            if user['name'] == db_user[1]:  # db_user[1] is the name
                user['created_at'] = db_user[2]
                user['last_seen'] = db_user[3]
                user['access_count'] = db_user[4]
                found = True
                break
        if not found:
            # Add user from database that doesn't have image files
            users.append({
                'name': db_user[1],
                'image': None,
                'trained': False,
                'created_at': db_user[2],
                'last_seen': db_user[3],
                'access_count': db_user[4]
            })
    return users

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    app.run(host='0.0.0.0', port=5000, debug=True)