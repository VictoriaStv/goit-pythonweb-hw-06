from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from models import Student, Grade, Subject, Teacher, Group


# 1. 5 студентів із найбільшим середнім балом
def select_1(session: Session):
    return (
        session.query(Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


# 2. Студент із найвищим середнім балом з певного предмета
def select_2(session: Session, subject_id: int):
    return (
        session.query(Student.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .first()
    )


# 3. Середній бал у групах з певного предмета
def select_3(session: Session, subject_id: int):
    return (
        session.query(Group.name, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )


# 4. Середній бал на потоці (по всіх предметах)
def select_4(session: Session):
    return session.query(func.round(func.avg(Grade.grade), 2)).scalar()


# 5. Які курси читає певний викладач
def select_5(session: Session, teacher_id: int):
    return (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )


# 6. Список студентів у певній групі
def select_6(session: Session, group_id: int):
    return (
        session.query(Student.name)
        .filter(Student.group_id == group_id)
        .all()
    )


# 7. Оцінки студентів у групі з певного предмета
def select_7(session: Session, group_id: int, subject_id: int):
    return (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )


# 8. Середній бал, який ставить певний викладач зі своїх предметів
def select_8(session: Session, teacher_id: int):
    return (
        session.query(func.round(func.avg(Grade.grade), 2))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


# 9. Курси, які відвідує певний студент
def select_9(session: Session, student_id: int):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )


# 10. Курси, які певному студенту читає певний викладач
def select_10(session: Session, student_id: int, teacher_id: int):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(
            Grade.student_id == student_id,
            Subject.teacher_id == teacher_id
        )
        .distinct()
        .all()
    )
