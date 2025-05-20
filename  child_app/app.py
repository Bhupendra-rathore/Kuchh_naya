from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'your_very_strong_secret_key_123'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'mp3', 'wav'}
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # Session lasts 24 hours

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.before_request
def initialize_session():
    if 'user_id' not in session:
        # Generate unique user ID for this session
        session['user_id'] = str(uuid.uuid4())
    
    if 'progress' not in session:
        session['progress'] = {
            'user_id': session['user_id'],
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'completed_tests': [],
            'results': {}
        }
    session.permanent = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_assessment', methods=['POST'])
def start_assessment():
    # Capture basic information about the child
    if request.method == 'POST':
        session['child_info'] = {
            'name': request.form.get('child_name', 'Anonymous Child'),
            'age': request.form.get('child_age', 'Not specified'),
            'parent_name': request.form.get('parent_name', 'Anonymous Parent'),
            'email': request.form.get('email', '')
        }
        session.modified = True
        return redirect(url_for('test', test_name='artistic'))
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                         progress=session['progress'],
                         child_info=session.get('child_info', {}),
                         total_tests=8)

@app.route('/test/<test_name>', methods=['GET', 'POST'])
def test(test_name):
    if request.method == 'POST':
        result = {}
        user_id = session['user_id']
        
        # Handle Artistic Test (Image Upload)
        if test_name == 'artistic':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # Create user-specific folder
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'users', user_id)
                os.makedirs(os.path.join(user_folder, 'drawings'), exist_ok=True)
                
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                save_path = os.path.join(user_folder, 'drawings', filename)
                file.save(save_path)
                result = {
                    'file_path': f"/static/uploads/users/{user_id}/drawings/{filename}",
                    'status': 'uploaded',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

        # Handle Logical Test
        elif test_name == 'logical':
            user_answer = request.form.get('answer')
            correct_answer = 'red'
            result = {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': user_answer == correct_answer,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        # Handle Linguistic Test
        elif test_name == 'linguistic':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # Create user-specific folder
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'users', user_id)
                os.makedirs(os.path.join(user_folder, 'recordings'), exist_ok=True)
                
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                save_path = os.path.join(user_folder, 'recordings', filename)
                file.save(save_path)
                result = {
                    'file_path': f"/static/uploads/users/{user_id}/recordings/{filename}",
                    'status': 'uploaded',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

        # Handle Musical Test
        elif test_name == 'musical':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # Create user-specific folder
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'users', user_id)
                os.makedirs(os.path.join(user_folder, 'recordings'), exist_ok=True)
                
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                save_path = os.path.join(user_folder, 'recordings', filename)
                file.save(save_path)
                result = {
                    'file_path': f"/static/uploads/users/{user_id}/recordings/{filename}",
                    'status': 'uploaded',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

        # Handle Interpersonal Test
        elif test_name == 'interpersonal':
            user_answer = request.form.get('answer')
            correct_answer = 'A'  # Set based on your video content
            result = {
                'user_answer': user_answer,
                'correct_answer': 'Child ' + correct_answer,
                'is_correct': user_answer == correct_answer,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        # Handle Naturalistic Test
        elif test_name == 'naturalistic':
            selected_animals = request.form.getlist('animals')
            correct_answers = ['Elephant', 'Tiger']  # Define correct answers
            is_correct = set(selected_animals) == set(correct_answers)
            
            result = {
                'answers': selected_animals,
                'correct_answers': correct_answers,
                'is_correct': is_correct,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        # Handle Visual-Spatial Test
        elif test_name == 'visual':
            user_answer = request.form.get('answer')
            correct_answer = 'B'  # Set correct answer based on your puzzle
            result = {
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': user_answer == correct_answer,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        # Handle Memory Test
        elif test_name == 'memory':
            user_answer = request.form.get('answer')
            correct_answer = 'swing'  # Assuming the monkey swings after panda eats bamboo
            
            # Map answer values to readable descriptions for feedback
            answer_descriptions = {
                'swing': 'Swing on a tree',
                'splash': 'Splash water',
                'roar': 'Roar like a T-Rex'
            }
            
            result = {
                'user_answer': user_answer,
                'user_answer_text': answer_descriptions.get(user_answer, 'Unknown'),
                'correct_answer': answer_descriptions[correct_answer],
                'is_correct': user_answer == correct_answer,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        # Update session
        session['progress']['results'][test_name] = result
        if test_name not in session['progress']['completed_tests']:
            session['progress']['completed_tests'].append(test_name)
        session.modified = True

        # If this was the last test, redirect to summary
        if len(session['progress']['completed_tests']) >= 8:  # Assuming 8 total tests
            return redirect(url_for('summary'))

        return render_template('test.html',
                            test_name=test_name,
                            progress=session['progress'],
                            result=result)
    
    return render_template('test.html',
                         test_name=test_name,
                         progress=session['progress'],
                         result=None)

@app.route('/summary')
def summary():
    if 'progress' not in session:
        return redirect(url_for('index'))
    
    # Calculate intelligence profile based on test results
    profile = calculate_intelligence_profile(session['progress']['results'])
    
    return render_template('summary.html',
                         child_info=session.get('child_info', {}),
                         progress=session['progress'],
                         profile=profile)

def calculate_intelligence_profile(results):
    """Calculate intelligence profile based on test results"""
    # Initialize scores for each intelligence type
    profile = {
        'artistic': 0,
        'logical': 0,
        'linguistic': 0,
        'musical': 0,
        'interpersonal': 0,
        'naturalistic': 0,
        'visual': 0,
        'memory': 0
    }
    
    # Calculate scores based on test results
    for test_name, result in results.items():
        # For upload-based tests, give full score if uploaded
        if test_name in ['artistic', 'linguistic', 'musical']:
            if result.get('status') == 'uploaded':
                profile[test_name] = 100
        # For answer-based tests, give score based on correctness
        elif test_name in ['logical', 'interpersonal', 'visual', 'memory']:
            if result.get('is_correct'):
                profile[test_name] = 100
        # For naturalistic test with multiple answers
        elif test_name == 'naturalistic':
            if result.get('is_correct'):
                profile[test_name] = 100
            else:
                # Partial credit based on number of correct answers
                selected = set(result.get('answers', []))
                correct = set(result.get('correct_answers', []))
                if len(correct) > 0:  # Avoid division by zero
                    # Score based on both precision and recall
                    if len(selected) > 0:  # Avoid division by zero
                        precision = len(selected.intersection(correct)) / len(selected)
                        recall = len(selected.intersection(correct)) / len(correct)
                        if precision + recall > 0:  # Avoid division by zero
                            f1_score = 2 * precision * recall / (precision + recall)
                            profile[test_name] = int(f1_score * 100)
    
    # Identify strengths (top 2 intelligences)
    strengths = sorted(profile.items(), key=lambda x: x[1], reverse=True)[:2]
    
    # Prepare human-readable intelligence names
    intelligence_names = {
        'artistic': 'Artistic',
        'logical': 'Logical-Mathematical',
        'linguistic': 'Linguistic',
        'musical': 'Musical',
        'interpersonal': 'Interpersonal',
        'naturalistic': 'Naturalistic',
        'visual': 'Visual-Spatial',
        'memory': 'Memory & Sequencing'
    }
    
    return {
        'scores': profile,
        'strengths': [(intelligence_names[s[0]], s[1]) for s in strengths],
        'intelligence_names': intelligence_names
    }

@app.route('/download_report/<user_id>')
def download_report(user_id):
    # Security check - only allow downloading own report
    if session.get('user_id') != user_id:
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    # Generate PDF report (you'd need a PDF generation library like ReportLab or WeasyPrint)
    # This is a placeholder for the actual PDF generation code
    
    return "Report download functionality to be implemented"

if __name__ == '__main__':
    # Create necessary directories
    for folder in ['drawings', 'recordings', 'users']:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], folder), exist_ok=True)
    app.run(debug=True)