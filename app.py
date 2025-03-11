from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase setup
cred = credentials.Certificate('serviceAccountKey.json')  # Add your Firebase credentials JSON
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    matches_ref = db.collection('matches')
    matches = matches_ref.stream()
    matches_list = [{**match.to_dict(), 'id': match.id} for match in matches]
    return render_template('index.html', matches=matches_list)

@app.route('/add_match', methods=['POST'])
def add_match():
    data = {
        'team1': request.form['team1'],
        'team2': request.form['team2'],
        'date': request.form['date'],
        'venue': request.form['venue'],
        'live_stream_link': request.form['live_stream_link']
    }
    db.collection('matches').add(data)
    return redirect(url_for('home'))

@app.route('/delete_match/<match_id>')
def delete_match(match_id):
    db.collection('matches').document(match_id).delete()
    return redirect(url_for('home'))

@app.route('/edit_match/<match_id>', methods=['GET', 'POST'])
def edit_match(match_id):
    match_ref = db.collection('matches').document(match_id)
    match = match_ref.get()
    
    if request.method == 'POST':
        match_ref.update({
            'team1': request.form['team1'],
            'team2': request.form['team2'],
            'date': request.form['date'],
            'venue': request.form['venue'],
            'live_stream_link': request.form['live_stream_link']
        })
        return redirect(url_for('home'))
    
    return render_template('edit.html', match={**match.to_dict(), 'id': match.id})

if __name__ == '__main__':
    app.run(debug=True)
