#!/usr/bin/python3
"""Unit tests for the HBNB command interpreter."""

import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """Test cases for the HBNB command interpreter."""

    def setUp(self):
        """Set up test cases."""
        self.console = HBNBCommand()
        self.classes = {
            "BaseModel": BaseModel,
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }

    def tearDown(self):
        """Clean up after each test."""
        storage.all().clear()
        storage.save()

    def test_create(self):
        """test create command."""
        # test create without class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **", f.getvalue().strip())

        # test create with invalid class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("create invalidclass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())

        # test create with valid class names
        for class_name in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                self.assertTrue(len(obj_id) > 0)
                key = f"{class_name}.{obj_id}"
                self.assertIn(key, storage.all())
                # Verify storage contains the new instance
                # self.assertTrue(obj_id in storage.all())
