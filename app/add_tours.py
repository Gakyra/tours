from app import app, db
from app.models import Tour
from datetime import datetime, timedelta

def add_tours():
    tours = [
        Tour(name="Екскурсія до Карпат", description="Подорож на гору Говерла", price=2000, date=datetime.now() + timedelta(days=30)),
        Tour(name="Поїздка до Львова", description="Оглядова екскурсія містом", price=1500, date=datetime.now() + timedelta(days=15)),
        Tour(name="Тур до Одеси", description="Відпочинок на узбережжі Чорного моря", price=1800, date=datetime.now() + timedelta(days=45))
    ]

    db.session.add_all(tours)
    db.session.commit()
    print("Тури додані!")

if __name__ == "__main__":
    with app.app_context():
        add_tours()
