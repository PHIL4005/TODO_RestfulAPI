import json
import sqlite3
from flask import Flask
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Date, MetaData
from sqlalchemy.orm import sessionmaker
from flasgger import Swagger, swag_from

Base = declarative_base()


class Todo(Base):

    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    due_date = Column(Date())
    status = Column(String(1), comment="I: in progress, C: completed, D: deleted")


def test_orm():
    engine = create_engine('sqlite:///data.db', echo=False)
    # Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    # create session instance
    session = Session()

    # # insert
    # new_todo = Todo(name="Drink water", description="You need 8 cups of water a day.", status="I")
    # session.add(new_todo)
    new_todo = Todo(name="Drink water", description="You need 8 cups of water a day.", status="I")
    session.add(new_todo)
    print(new_todo.id)
    # table = Table("TODOS", MetaData())
    # ret = session.execute(table.insert(), {
    #         'name': 'test pk',
    #         'description': 'test pk..',
    #         'status': "I"
    #     })
    # print(ret.inserted_primary_id)

    # # select
    # query_result = session.query(Todo).filter(Todo.id > 1).first()
    # print(query_result.id)
    # print(json.dumps(query_result))
    # for res in query_result:
    #     print(res.id, res.name)
    #
    # # update
    # session.query(Todo).filter(Todo.id == 3).update({Todo.description: 'Modified description..'})
    #
    # # delete
    # session.query(Todo).filter(Todo.id == 3).delete()

    session.commit()
    print(new_todo.id)
    session.close()

    # conn = sqlite3.connect('data.db')
    # c = conn.cursor()
    # c.execute("select * from todos")
    # # c.execute("INSERT INTO TODOS (NAME, DESCRIPTION, STATUS) VALUES ('Sample task', 'Write something..', 'I')")
    # conn.commit()
    # print(c.execute("select * from todos"))
    # conn.close()


if __name__ == '__main__':
    test_orm()