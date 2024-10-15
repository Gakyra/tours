from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required

from .config import app, db
from .models import User, Tour, Booking
from .forms import RegistrationForm, LoginForm, BookingForm, TourForm
from .views import get_tour_details, is_tour_available, get_upcoming_tours, calculate_discount

__all__ = (
    'index',
    'register',
    'login',
    'logout',
    'tour_details',
    'tour_availability',
    'upcoming_tours',
    'tour_discount',
    'book_tour',
    'manage_tours',
    'edit_tour',
    'delete_tour',
    'profile',
)

# Головна сторінка
@app.route('/')
def index():
    tours = get_upcoming_tours()
    discount_percentage = 10
    tour_data = []

    for tour in tours:
        tour_info = {
            'id': tour.id,
            'name': tour.name,
            'description': tour.description,
            'price': tour.price,
            'discounted_price': calculate_discount(tour.id, discount_percentage),
            'is_available': is_tour_available(tour.id),
            'date': tour.date.strftime('%Y-%m-%d')
        }
        tour_data.append(tour_info)

    return render_template('index.html', tours=tour_data)

# Реєстрація
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Ви успішно зареєструвались!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

# Увійти
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

# Вихід
@app.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи!', 'success')
    return redirect(url_for('index'))

# Деталі туру
@app.route('/tour/<int:tour_id>/details', methods=['GET'])
def tour_details(tour_id):
    details = get_tour_details(tour_id)
    if details:
        return render_template('tour_details.html', tour=details)
    return jsonify({"error": "Тур не знайдено"}), 404

# Доступність туру
@app.route('/tour/<int:tour_id>/availability', methods=['GET'])
def tour_availability(tour_id):
    available = is_tour_available(tour_id)
    return jsonify({"available": available})

# Наступні тури
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
    return jsonify({"message": "Немає доступних наступних турів"})

# Знижка на тур
@app.route('/tour/<int:tour_id>/discount', methods=['POST'])
def tour_discount(tour_id):
    data = request.get_json()
    discount_percentage = data.get('discount_percentage')
    if discount_percentage is None:
        return jsonify({"error": "Процент знижки не вказано"}), 400

    discounted_price = calculate_discount(tour_id, discount_percentage)
    if discounted_price is not None:
        return jsonify({"discounted_price": discounted_price})
    return jsonify({"error": "Тур не знайдено"}), 404

# Бронювання туру
@app.route('/tour/<int:tour_id>/book', methods=['GET', 'POST'])
@login_required
def book_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = BookingForm()
    if form.validate_on_submit():
        date = form.date.data
        people = form.people.data

        # Розрахунок загальної ціни
        total_price = tour.price * people

        booking = Booking(
            user_id=current_user.id,
            tour_id=tour_id,
            number_of_people=people,
            date=date,
            total_price=total_price
        )

        db.session.add(booking)
        db.session.commit()

        flash('Бронювання успішне!', 'success')
        return redirect(url_for('index'))

    return render_template('book_tour.html', form=form, tour=tour)

# Керування турами
@app.route('/manage_tours', methods=['GET', 'POST'])
@login_required
def manage_tours():
    form = TourForm()
    if form.validate_on_submit():
        new_tour = Tour(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            date=form.date.data
        )
        db.session.add(new_tour)
        db.session.commit()
        flash('Тур успішно додано!', 'success')
        return redirect(url_for('manage_tours'))

    tours = Tour.query.all()
    return render_template('manage_tours.html', form=form, tours=tours)

# Редагування туру
@app.route('/tour/<int:tour_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = TourForm(obj=tour)

    if form.validate_on_submit():
        tour.name = form.name.data
        tour.description = form.description.data
        tour.price = form.price.data
        tour.date = form.date.data
        db.session.commit()
        flash('Тур успішно оновлено!', 'success')
        return redirect(url_for('manage_tours'))

    return render_template('edit_tour.html', form=form, tour=tour)

# Видалення туру
@app.route('/tour/<int:tour_id>/delete', methods=['POST'])
@login_required
def delete_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    db.session.delete(tour)
    db.session.commit()
    flash('Тур успішно видалено!', 'success')
    return redirect(url_for('manage_tours'))

# Профіль користувача
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
