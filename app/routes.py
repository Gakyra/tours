from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user
from app import app, db
from app.models import User, Tour
from datetime import datetime

__all__ = (
    'index',
    'register',
    'login',
    'logout',
    'tour_details',
    'tour_availability',
    'upcoming_tours',
    'tour_discount',
    'calculate_discount',
    'get_upcoming_tours',
    'is_tour_available',
    'get_tour_details'
)

# Маршрути
@app.route('/')
def index():
    tours = Tour.query.all()
    return render_template('index.html', tours=tours)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/tour/<int:tour_id>/details', methods=['GET'])
def tour_details(tour_id):
    details = get_tour_details(tour_id)
    if details:
        return jsonify(details)
    return jsonify({"error": "Tour not found"}), 404

@app.route('/tour/<int:tour_id>/availability', methods=['GET'])
def tour_availability(tour_id):
    available = is_tour_available(tour_id)
    return jsonify({"available": available})

@app.route('/tours/upcoming', methods=['GET'])
def upcoming_tours():
    tours = get_upcoming_tours()
    if tours:
        return jsonify([{
            'name': tour.name,
            'description': tour.description,
            'price': tour.price,
            'date': tour.date.strftime('%Y-%m-%d'),
        } for tour in tours])
    return jsonify({"message": "No upcoming tours available"})

@app.route('/tour/<int:tour_id>/discount', methods=['POST'])
def tour_discount(tour_id):
    data = request.get_json()
    discount_percentage = data.get('discount_percentage')
    if discount_percentage is None:
        return jsonify({"error": "Discount percentage not provided"}), 400

    discounted_price = calculate_discount(tour_id, discount_percentage)
    if discounted_price is not None:
        return jsonify({"discounted_price": discounted_price})
    return jsonify({"error": "Tour not found"}), 404


# Функції
def calculate_discount(tour_id, discount_percentage):
    tour = Tour.query.get(tour_id)
    if tour:
        discounted_price = tour.price - (tour.price * (discount_percentage / 100))
        return discounted_price
    return None

def get_upcoming_tours():
    current_date = datetime.now()
    upcoming_tours = Tour.query.filter(Tour.date >= current_date).all()
    return upcoming_tours

def is_tour_available(tour_id):
    tour = Tour.query.get(tour_id)
    if tour and tour.date >= datetime.now():
        return True
    return False

def get_tour_details(tour_id):
    tour = Tour.query.get(tour_id)
    if tour:
        return {
            'name': tour.name,
            'description': tour.description,
            'price': tour.price,
            'date': tour.date.strftime('%Y-%m-%d'),
        }
    return None
