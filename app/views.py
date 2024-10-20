from datetime import datetime
from flask import flash
from .models import Tour
from .config import db


def calculate_discount(tour_id, discount_percentage):
    try:
        tour = Tour.query.get(tour_id)
        if tour:
            discounted_price = tour.price - (tour.price * (discount_percentage / 100))
            tour.price = max(discounted_price, 0)
            db.session.commit()
            return tour.price
        return None
    except Exception as e:
        flash(f"Error calculating discount: {str(e)}", 'danger')
        return None


def get_upcoming_tours():
    try:
        current_date = datetime.now().date()
        print(f"Current date: {current_date}")
        tours = Tour.query.all()
        print(f"All tours: {tours}")
        upcoming_tours = []
        for tour in tours:
            print(f"Tour: {tour.name}, Date: {tour.date}, Type: {type(tour.date)}")
            tour_date = tour.date.date()
            print(f"Parsed date: {tour_date}")

            if tour_date >= current_date:
                upcoming_tours.append(tour)

        print(f"Upcoming tours retrieved: {upcoming_tours}")
        if not upcoming_tours:
            flash("Немає доступних наступних турів", 'warning')
        return upcoming_tours
    except Exception as e:
        flash(f"Error fetching upcoming tours: {str(e)}", 'danger')
        return []


def is_tour_available(tour_id):
    try:
        tour = Tour.query.get(tour_id)
        if tour and tour.date >= datetime.now():
            return True
    except Exception as e:
        flash(f"Error checking tour availability: {str(e)}", 'danger')
    return False


def get_tour_details(tour_id):
    try:
        tour = Tour.query.get(tour_id)
        if tour:
            return {
                'name': tour.name,
                'description': tour.description,
                'price': tour.price,
                'date': tour.date.strftime('%Y-%m-%d'),
            }
    except Exception as e:
        flash(f"Error fetching tour details: {str(e)}", 'danger')
    return None
