from datetime import datetime
from app.models import Tour


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
