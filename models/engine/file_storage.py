#!/usr/bin/python3
"""this Module defines a class to manage file storage for the hbnb clone"""

import json
import os
from importlib import import_module


class FileStorage:
    """this class manages the storage of hbnb models in JSON file format"""

    __file_path = 'file.json'
    __objects = {}

    def __init__(self):
        """Initializes a FileStorage instance and loads models classes"""

        # Dictionary mapping model names to their corresponding classes .
        self.model_classes = {
            'BaseModel': import_module('models.base_model').BaseModel,
            'User': import_module('models.user').User,
            'State': import_module('models.state').State,
            'City': import_module('models.city').City,
            'Amenity': import_module('models.amenity').Amenity,
            'Place': import_module('models.place').Place,
            'Review': import_module('models.review').Review
        }

    def all(self, cls=None):
        """
        Returns A dictionary of all models currently in storage,
        or filtered by the specified class if provided.
        """
        if cls is None:
            return self.__objects
        else:
            filtered_dict = {}
            for key, value in self.__objects.items():
                if isinstance(value, cls):
                    filtered_dict[key] = value
            return filtered_dict

    def delete(self, obj=None):
        """removes the specified object from the storage dict"""
        if obj is not None:
            obj_key = obj.to_dict()['__class__'] + '.' + obj.id
            if obj_key in self.__objects.keys():
                del self.__objects[obj_key]

    def new(self, obj):
        """Adds a new object to the storage dict"""
        self.__objects.update(
            {obj.to_dict()['__class__'] + '.' + obj.id: obj}
        )

    def save(self):
        """Saves the current storage Dictionary to a JSON.file"""
        with open(self.__file_path, 'w') as file:
            temp = {}
            for key, val in self.__objects.items():
                temp[key] = val.to_dict()
            json.dump(temp, file)

    def reload(self):
        """Loads the storage Dictionary from the JSON file"""
        classes = self.model_classes
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, 'r') as file:
                temp = json.load(file)
                for key, val in temp.items():
                    self.__objects[key] = classes[val['__class__']](**val)

    def close(self):
        """closes the storage engine by reloading the data"""
        self.reload()
