"""
To-Do list application

Author:  Anshul Kharbanda
Created: 11 - 10 - 2017
"""
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField

class TodoForm(FlaskForm):
    """
    Form for updating To-Do's

    Author:  Anshul Kharbanda
    Created: 11 - 10 - 2017
    """
    text = StringField('Text')

class Todo:
    """
    Model for Todo

    Author:  Anshul Kharbanda
    Created: 11 - 11 - 2017
    """
    _collection_name = 'todos'

    @classmethod
    def collection(cls, db):
        """
        Returns the Todo collection from the database name

        :param: db the db to retrieve the collection from

        :return: the collection form the database name
        """
        return db[cls._collection_name]

    @classmethod
    def index(cls, db):
        """
        Returns all Todos from database

        :param db: the db to index

        :returen: all todos from database
        """
        return (Todo(**doc) for doc in cls.collection(db).find())

    @classmethod
    def get(cls, db, id):
        """
        Returns the Todo for the given id

        :param db: the db to retrieve from
        :param id: the id of the todo to return

        :return: the todo with the given id
        """
        doc = cls.collection(db).find_one(filter={ '_id': ObjectId(id) })
        return Todo(**doc)

    def __init__(self, text='', _id=None):
        """
        Initializes the todo with the given text and _id

        :param text: the text of the Todo
        :param _id: the _id of the Todo
        """
        self._id = _id
        self.text = text
        self.form = TodoForm()

    @property
    def doc(self):
        """
        The document dict of the Todo
        """
        return {'_id': self._id,
                'text': self.text}

    def form_submit(self):
        """
        Returns true if the given todo form is being submitted

        :return: true if the given todo form is being submitted
        """
        return self.form.validate_on_submit()

    def update(self, db):
        """
        Updates the record from the form and saves it to the database

        :param db: the database to save to
        """
        self.text = self.form.text.data
        self.save(db)

    def save(self, db):
        """
        Saves to mongo database

        :param db: the mongo database to save to
        """
        # Create new if no id is given
        if self._id is None:
            self.collection(db).insert_one(
                document={'text': self.text})

        # Else update old
        else:
            self.collection(db).update_one(
                filter={'_id': ObjectId(self._id)},
                update={'$set': {'text': self.text}})

    def delete(self, db):
        """
        Deletes the todo from the database

        :param db: the database to delete from
        """
        # Delete id if given
        if self._id is not None:
            self.collection(db).delete_one(
                filter={'_id': ObjectId(self._id)})
