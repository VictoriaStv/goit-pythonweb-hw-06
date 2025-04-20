import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_select import (
    select_1, select_2, select_3, select_4, select_5,
    select_6, select_7, select_8, select_9, select_10
)

DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/students"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def main():
    parser = argparse.ArgumentParser(description="Student DB Queries")
    parser.add_argument("-q", "--query", type=int, required=True, help="Query number 1–10")
    parser.add_argument("--subject_id", type=int, help="Subject ID")
    parser.add_argument("--group_id", type=int, help="Group ID")
    parser.add_argument("--student_id", type=int, help="Student ID")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID")

    args = parser.parse_args()
    session = Session()

    match args.query:
        case 1:
            result = select_1(session)
        case 2:
            result = select_2(session, args.subject_id)
        case 3:
            result = select_3(session, args.subject_id)
        case 4:
            result = select_4(session)
        case 5:
            result = select_5(session, args.teacher_id)
        case 6:
            result = select_6(session, args.group_id)
        case 7:
            result = select_7(session, args.group_id, args.subject_id)
        case 8:
            result = select_8(session, args.teacher_id)
        case 9:
            result = select_9(session, args.student_id)
        case 10:
            result = select_10(session, args.student_id, args.teacher_id)
        case _:
            print("❌ Invalid query number (1–10)")
            return

    print("✅ Result:")
    if isinstance(result, list):
        for row in result:
            print(row)
    else:
        print(result)

    session.close()

if __name__ == "__main__":
    main()
