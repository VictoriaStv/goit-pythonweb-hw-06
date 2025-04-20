import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Teacher, Student, Group, Subject, Base

DB_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/students"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

model_map = {
    "Teacher": Teacher,
    "Student": Student,
    "Group": Group,
    "Subject": Subject,
}

def create_instance(session, model_name, name, group_id=None, teacher_id=None):
    model = model_map.get(model_name)
    if not model:
        print("❌ Unknown model")
        return

    data = {"name": name}
    if model_name == "Student" and group_id:
        data["group_id"] = group_id
    if model_name == "Subject" and teacher_id:
        data["teacher_id"] = teacher_id

    instance = model(**data)
    session.add(instance)
    session.commit()
    print(f"✅ Created {model_name}: {instance.name}")

def list_instances(session, model_name):
    model = model_map.get(model_name)
    if not model:
        print("❌ Unknown model")
        return
    instances = session.query(model).all()
    for obj in instances:
        print(f"{obj.id}: {obj.name}")

def update_instance(session, model_name, id, name):
    model = model_map.get(model_name)
    if not model:
        print("❌ Unknown model")
        return
    obj = session.query(model).get(id)
    if not obj:
        print(f"❌ {model_name} with id={id} not found")
        return
    obj.name = name
    session.commit()
    print(f"✅ Updated {model_name} id={id}")

def delete_instance(session, model_name, id):
    model = model_map.get(model_name)
    if not model:
        print("❌ Unknown model")
        return
    obj = session.query(model).get(id)
    if not obj:
        print(f"❌ {model_name} with id={id} not found")
        return
    session.delete(obj)
    session.commit()
    print(f"🗑️ Deleted {model_name} id={id}")

def main():
    parser = argparse.ArgumentParser(description="CRUD CLI")
    parser.add_argument("-a", "--action", required=True, help="create/list/update/delete")
    parser.add_argument("-m", "--model", required=True, help="Model: Teacher, Student, Group, Subject")
    parser.add_argument("--id", type=int, help="ID of object (for update/delete)")
    parser.add_argument("-n", "--name", help="Name of object")
    parser.add_argument("--group_id", type=int, help="Group ID for Student")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID for Subject")

    args = parser.parse_args()
    session = Session()

    match args.action:
        case "create":
            create_instance(session, args.model, args.name, args.group_id, args.teacher_id)
        case "list":
            list_instances(session, args.model)
        case "update":
            update_instance(session, args.model, args.id, args.name)
        case "delete":
            delete_instance(session, args.model, args.id)
        case _:
            print("❌ Unknown action")

    session.close()

if __name__ == "__main__":
    main()
