#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""

import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        If `cls` is provided, filters and returns objects of that class type.
        """
        if cls:
            return {
                key: obj
                for key, obj in FileStorage.__objects.items()
                if isinstance(obj, cls)
            }
        return FileStorage.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()["__class__"] + "." + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, "w") as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.amenity import Amenity
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, "r") as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it exists.
        If obj is None, does nothing.
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]

    def close(self):
        """
        call reload method for deserilazing the JSON
        file to object.
        """
        self.reload()
