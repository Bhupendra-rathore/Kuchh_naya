from flask import Flask, render_template, request, redirect, url_for, session
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp3', 'wav', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def initialize_session():
    if 'progress' not in session:
        session['progress'] = {
            'completed_tests': [],
            'results': {}
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if len(session['progress']['completed_tests']) >= 9:
        return redirect(url_for('summary'))
    return render_template('dashboard.html',
                         progress=session['progress'],
                         total_tests=9)

@app.route('/test/<test_name>', methods=['GET', 'POST'])
def test(test_name):
    if request.method == 'POST':
        result = {}
        
        if test_name in ['artistic', 'linguistic', 'musical', 'bodily']:
            file = request.files.get('file')
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{test_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                folder = 'drawings' if test_name == 'artistic' else \
                         'recordings' if test_name in ['linguistic', 'musical'] else \
                         'videos'
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
                file.save(save_path)
                result['file'] = filename
        else:
            result['answer'] = request.form.get('answer')

        session['progress']['results'][test_name] = result
        if test_name not in session['progress']['completed_tests']:
            session['progress']['completed_tests'].append(test_name)
        session.modified = True
        
        return redirect(url_for('dashboard'))
    
    
    return render_template(
        'test.html',
        test_name=test_name,
        progress=session.get('progress')  # Pass progress explicitly
    )

@app.route('/summary')
def summary():
    scores = {
        'artistic': 95, 'logical': 82, 'linguistic': 78,
        'musical': 65, 'bodily': 58, 'interpersonal': 88,
        'naturalistic': 72, 'visual': 85, 'memory': 80
    }
    
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return render_template('summary.html',
                         scores=scores,
                         strengths=sorted_scores[:3],
                         improvements=sorted_scores[-3:])

if __name__ == '__main__':
    for folder in ['drawings', 'recordings', 'videos']:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder), exist_ok=True)
    app.run(debug=True)