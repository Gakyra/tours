from datetime import datetime
from app.models import Tour

# Функція для розрахунку знижки для туру
def calculate_discount(tour_id, discount_percentage):
    tour = Tour.query.get(tour_id)
    if tour:
        discounted_price = tour.price - (tour.price * (discount_percentage / 100))
        return discounted_price
    return None

# Функція для отримання турів, які будуть відбуватися у майбутньому
def get_upcoming_tours():
    current_date = datetime.now()
    upcoming_tours = Tour.query.filter(Tour.date >= current_date).all()
    return upcoming_tours

# Функція перевірки чи доступний тур для бронювання
def is_tour_available(tour_id):
    tour = Tour.query.get(tour_id)
    if tour and tour.date >= datetime.now():
        return True
    return False

# Функція для отримання деталей туру
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
