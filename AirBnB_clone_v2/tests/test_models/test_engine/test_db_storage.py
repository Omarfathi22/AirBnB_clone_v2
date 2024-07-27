#!/usr/bin/python3
""" Module for testing database storage """
import MySQLdb
import os
import unittest
from datetime import datetime

from models import storage
from models.user import User

@unittest.skipIf(
    os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
class TestDBStorage(unittest.TestCase):
    """ Class to test the database storage method """

    def test_new(self):
        """ New object is correctly added to database """
        # Create a new User object
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        # Check if the new object is not in storage
        self.assertFalse(new in storage.all().values())
        # Save the new object
        new.save()
        # Check if the new object is now in storage
        self.assertTrue(new in storage.all().values())

        # Connect to MySQL database
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        # Execute SELECT query to fetch the new object from the database
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        # Assertions to check if data is correctly stored in the database
        self.assertTrue(result is not None)
        self.assertIn('john2020@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('John', result)
        self.assertIn('Zoldyck', result)
        cursor.close()
        dbc.close()

    def test_delete(self):
        """ Object is correctly deleted from database """
        # Create a new User object
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        obj_key = 'User.{}'.format(new.id)
        # Connect to MySQL database
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        # Save the new object
        new.save()
        # Check if the new object is in storage
        self.assertTrue(new in storage.all().values())
        cursor = dbc.cursor()
        # Execute SELECT query to fetch the new object from the database
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        # Assertions to check if data is correctly stored in the database
        self.assertTrue(result is not None)
        self.assertIn('john2020@gmail.com', result)
        self.assertIn('password', result)
        self.assertIn('John', result)
        self.assertIn('Zoldyck', result)
        # Check if object key is in storage before delete
        self.assertIn(obj_key, storage.all(User).keys())
        # Delete the object
        new.delete()
        # Check if object key is not in storage after delete
        self.assertNotIn(obj_key, storage.all(User).keys())
        cursor.close()
        dbc.close()

    def test_reload(self):
        """ Tests the reloading of the database session """
        # Connect to MySQL database
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        # Insert a new record directly into the users table
        cursor.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '4447-by-me',
                str(datetime.now()),
                str(datetime.now()),
                'ben_pike@yahoo.com',
                'pass',
                'Benjamin',
                'Pike',
            ]
        )
        dbc.commit()
        # Check if the new record key is not in storage before reload
        self.assertNotIn('User.4447-by-me', storage.all())
        # Reload the database session
        storage.reload()
        # Check if the new record key is now in storage after reload
        self.assertIn('User.4447-by-me', storage.all())
        cursor.close()
        dbc.close()

    def test_save(self):
        """ Object is successfully saved to database """
        # Create a new User object
        new = User(
            email='john2020@gmail.com',
            password='password',
            first_name='John',
            last_name='Zoldyck'
        )
        # Connect to MySQL database
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor = dbc.cursor()
        # Execute SELECT query to check if object is initially not in database
        cursor.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor.fetchone()
        cursor.execute('SELECT COUNT(*) FROM users;')
        old_cnt = cursor.fetchone()[0]
        self.assertTrue(result is None)
        self.assertFalse(new in storage.all().values())
        # Save the new object
        new.save()
        # Connect again to check if object is now in database
        dbc1 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cursor1 = dbc1.cursor()
        cursor1.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        result = cursor1.fetchone()
        cursor1.execute('SELECT COUNT(*) FROM users;')
        new_cnt = cursor1.fetchone()[0]
        self.assertFalse(result is None)
        # Check if the count of records increased by 1 after save
        self.assertEqual(old_cnt + 1, new_cnt)
        self.assertTrue(new in storage.all().values())
        cursor1.close()
        dbc1.close()
        cursor.close()
        dbc.close()

    def test_storage_var_created(self):
        """ DBStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)

    def test_new_and_save(self):
        '''testing  the new and save methods'''
        # Connect to MySQL database
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        # Create a new User object
        new_user = User(**{'first_name': 'jack',
                           'last_name': 'bond',
                           'email': 'jack@bond.com',
                           'password': 12345})
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        old_count = cur.fetchall()
        cur.close()
        db.close()
        # Save the new User object
        new_user.save()
        # Connect again to check if count of records increased by 1
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        cur = db.cursor()
        cur.execute('SELECT COUNT(*) FROM users')
        new_count = cur.fetchall()
        self.assertEqual(new_count[0][0], old_count[0][0] + 1)
        cur.close()
        db.close()

