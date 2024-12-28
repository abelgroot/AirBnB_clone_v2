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
        """Test create command with and without parameters."""
        # Test create without class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual("** class name missing **", f.getvalue().strip())
    
        # Test create with invalid class name
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd("create InvalidClass")
            self.assertEqual("** class doesn't exist **", f.getvalue().strip())
    
        # Test create with valid class names without parameters
        for class_name in self.classes:
            with patch("sys.stdout", new=StringIO()) as f:
                self.console.onecmd(f"create {class_name}")
                obj_id = f.getvalue().strip()
                self.assertTrue(len(obj_id) > 0)
                key = f"{class_name}.{obj_id}"
                self.assertIn(key, storage.all())

        # Test create with valid parameters
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd('create Place name="My_little_house" number_rooms=4 latitude=37.773972 longitude=-122.431297')
            obj_id = f.getvalue().strip()
            self.assertTrue(len(obj_id) > 0)
            key = f"Place.{obj_id}"
            self.assertIn(key, storage.all())
            obj = storage.all()[key]
            self.assertEqual(obj.name, "My little house")
            self.assertEqual(obj.number_rooms, 4)
            self.assertEqual(obj.latitude, 37.773972)
            self.assertEqual(obj.longitude, -122.431297)
    
        # Test create with invalid parameters (should skip them)
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd('create Place name="Invalid name with space" invalid_param="123" number_rooms=4')
            obj_id = f.getvalue().strip()
            self.assertTrue(len(obj_id) > 0)
            key = f"Place.{obj_id}"
            self.assertIn(key, storage.all())
            obj = storage.all()[key]
            # "Invalid name with space" should be skipped
            self.assertEqual(obj.name, '')
            # "invalid_param" should be correctly set
            self.assertEqual(obj.invalid_param, '123')
            # "number_rooms" should be correctly set
            self.assertEqual(obj.number_rooms, 4)

        # Test create with escaped quotes and underscores
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.onecmd('create Place description="A_house_with_\"escaped\"_quotes" max_guest=10')
            obj_id = f.getvalue().strip()
            self.assertTrue(len(obj_id) > 0)
            key = f"Place.{obj_id}"
            self.assertIn(key, storage.all())
            obj = storage.all()[key]
            self.assertEqual(obj.description, 'A house with "escaped" quotes')
            self.assertEqual(obj.max_guest, 10)
