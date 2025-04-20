import random
from faker import Faker
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Group, Student, Teacher, Subject, Grade

# DB connection
DB_URL = 'postgresql+psycopg2://postgres:12345@localhost:5432/students'
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


groups = session.query(Group).all()

# Якщо груп ще немає — створити
if not groups:
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

#  groups гарантовано не пустий


session.commit()

teachers = [Teacher(name=fake.name()) for _ in range(5)]
session.add_all(teachers)
session.commit()

subjects = [
    Subject(name=fake.word().capitalize(), teacher=random.choice(teachers))
    for _ in range(8)
]
session.add_all(subjects)
session.commit()

students = [
    Student(name=fake.name(), group=random.choice(groups))
    for _ in range(50)
]
session.add_all(students)
session.commit()

for student in students:
    for subject in random.sample(subjects, k=random.randint(3, 6)):
        for _ in range(random.randint(10, 20)):
            grade = Grade(
                grade=round(random.uniform(60, 100), 2),
                date_of=fake.date_between(start_date='-1y', end_date='today'),
                student=student,
                subject=subject
            )
            session.add(grade)

session.commit()
session.close()

print("✅ Seed completed.")
