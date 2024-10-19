from flask import render_template, redirect, url_for, request, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from .config import app, db
from .models import User, Tour, Booking
from .forms import RegistrationForm, LoginForm, BookingForm, TourForm, DiscountForm
from .views import get_tour_details, is_tour_available, get_upcoming_tours, calculate_discount
from werkzeug.utils import secure_filename
import os

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
    print(f"Tours in index: {tours}")
    return render_template('index.html', tours=tours)


# Реєстрація
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Form validated successfully")  # Логування
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Хешування пароля
        db.session.add(user)
        db.session.commit()
        print(f"User {user.username} registered successfully")
        flash('Акаунт успішно створено! Тепер ви можете увійти.', 'success')
        return redirect(url_for('login'))
    print("Form errors: ", form.errors)  # Логування
    return render_template('register.html', form=form)


# Увійти
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print(f"User found: {user.username}")
            if user.check_password(form.password.data):
                login_user(user)
                print(f"User {user.username} logged in successfully")  # Логування
                flash('Ви успішно увійшли!', 'success')
                return redirect(url_for('index'))
            else:
                print("Password incorrect")  # Логування
        else:
            print("User not found")  # Логування
        flash('Невірне ім\'я користувача або пароль', 'danger')
    print("Form errors: ", form.errors)  # Логування
    return render_template('login.html', form=form)


# Вихід
@app.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з системи!', 'success')
    return redirect(url_for('index'))


# Деталі туру
@app.route('/tour/<int:tour_id>/detail', methods=['GET'])
def tour_details(tour_id):
    tour = Tour.query.get(tour_id)
    if tour:
        if isinstance(tour.date, str):
            try:
                tour.date = datetime.strptime(tour.date, '%Y-%m-%d')
            except ValueError:
                return "Invalid date format", 400
        return render_template('tour_details.html', tour=tour)
    return redirect(url_for('index'))


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
@app.route('/tour/<int:tour_id>/discount', methods=['GET', 'POST'])
@login_required
def tour_discount(tour_id):
    if not current_user.is_admin:
        flash('Доступ заборонено: тільки адміністратори можуть застосовувати знижки.', 'danger')
        return redirect(url_for('manage_tours'))
    form = DiscountForm()
    tour = Tour.query.get_or_404(tour_id)
    discounted_price = None
    if form.validate_on_submit():
        discount_percentage = form.discount_percentage.data
        if not tour.original_price:
            tour.original_price = tour.price
        discounted_price = tour.original_price - (tour.original_price * discount_percentage / 100)
        tour.price = discounted_price
        tour.discount_percentage = discount_percentage
        db.session.commit()
        flash(f'New discounted price: {discounted_price}', 'success')
        return redirect(url_for('manage_tours'))
    return render_template('discount.html', form=form, tour=tour, discounted_price=discounted_price)



# Бронювання туру
@app.route('/tour/<int:tour_id>/book', methods=['GET', 'POST'])
@login_required
def book_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    form = BookingForm()
    if request.method == 'POST' and form.validate_on_submit():
        date = form.date.data
        people = form.number_of_people.data
        print(f"Requested spots: {people}, Available spots: {tour.available_spots}")
        if not tour.is_available(people):
            flash('Недостатньо вільних місць для бронювання!', 'danger')
            return redirect(url_for('book_tour', tour_id=tour_id))
        total_price = tour.price * people  # Розрахунок загальної ціни
        booking = Booking(
            user_id=current_user.id,
            tour_id=tour_id,
            number_of_people=people,
            date=date,
            total_price=total_price
        )
        tour.available_spots -= people
        db.session.add(booking)
        db.session.commit()
        flash(f'Бронювання успішне! Загальна ціна: {total_price}', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.date.data = tour.date.date()
    print(f"Form errors: {form.errors}")
    return render_template('book_tour.html', form=form, tour=tour)



# Керування турами
@app.route('/manage_tours', methods=['GET', 'POST'])
@login_required
def manage_tours():
    if not current_user.is_admin:
        flash('Доступ заборонено: тільки адміністратори можуть керувати турами.', 'danger')
        return redirect(url_for('index'))
    form = TourForm()
    if form.validate_on_submit():
        new_tour = Tour(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            date=form.date.data,
            available_spots=form.available_spots.data
        )
        db.session.add(new_tour)
        db.session.commit()
        flash('Тур успішно додано!', 'success')
        return redirect(url_for('manage_tours'))
    if form.errors:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}', 'danger')
    tours = Tour.query.all()
    return render_template('manage_tours.html', form=form, tours=tours)

@app.route('/tour/<int:tour_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    if not current_user.is_admin:
        flash('Доступ заборонено: тільки адміністратори можуть керувати турами.', 'danger')
        return redirect(url_for('index'))
    form = TourForm(obj=tour)
    if form.validate_on_submit():
        tour.name = form.name.data
        tour.description = form.description.data
        tour.price = form.price.data
        tour.date = form.date.data
        tour.available_spots = form.available_spots.data
        db.session.commit()
        flash('Тур успішно оновлено!', 'success')
        return redirect(url_for('manage_tours'))
    return render_template('edit_tour.html', form=form, tour=tour)





# Видалення туру
@app.route('/tour/<int:tour_id>/delete', methods=['POST'])
@login_required
def delete_tour(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    if not current_user.is_admin:
        flash('Доступ заборонено: тільки адміністратори можуть видаляти тури.', 'danger')
        return redirect(url_for('manage_tours'))

    # Видаляємо всі бронювання для цього туру
    bookings = Booking.query.filter_by(tour_id=tour.id).all()
    for booking in bookings:
        db.session.delete(booking)

    db.session.delete(tour)
    db.session.commit()
    flash('Тур успішно видалено.', 'success')
    return redirect(url_for('manage_tours'))


# Профіль користувача
@app.route('/profile')
@login_required
def profile():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    tours = [booking.tour for booking in bookings]
    return render_template('profile.html', tours=tours)

