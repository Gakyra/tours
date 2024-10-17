from datetime import datetime
from flask import flash
from .models import Tour

def calculate_discount(tour_id, discount_percentage):
    try:
        tour = Tour.query.get(tour_id)
        if tour:
            discounted_price = tour.price - (tour.price * (discount_percentage / 100))
            return max(discounted_price, 0)  # Забезпечте, щоб ціна не була від'ємною
    except Exception as e:
        flash(f"Error calculating discount: {str(e)}", 'danger')
    return None

def get_upcoming_tours():
    try:
        current_date = datetime.now()
        upcoming_tours = Tour.query.filter(Tour.date >= current_date).all()
        print(f"Upcoming tours: {upcoming_tours}")
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
