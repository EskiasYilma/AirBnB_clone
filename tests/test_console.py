#!/usr/bin/python3
"""
Unittest for Console
"""
from contextlib import contextmanager
from io import StringIO
import unittest
from unittest.mock import patch
from datetime import datetime
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models import storage
from models.engine.file_storage import FileStorage
import os


class TestConsole(unittest.TestCase):
    """
    Test cases for the Console class

    Tests all methods and errors for HBNBCommand class
    """

    def setUp(self):
        """
        setUp function docstring

        Setting up the test environment
        """

        args = {'created_at': datetime(2023, 3, 8, 19, 30, 48, 436849),
                'updated_at': datetime(2023, 3, 8, 19, 30, 48, 436966),
                'id': 'd42f98a5-71d3-4237-83f3-f480c9dc3c18',
                'name': 'model_1'}
        self.model = BaseModel(**args)
        self.model.save()

        self.console = HBNBCommand()
        self.mock_stdout = StringIO()

    def tearDown(self):
        all_objs = storage.all()
        for k in list(all_objs.keys()):
            del all_objs[k]

    def test_do_quit(self):
        """test_do_quit Docstring"""
        with self.assertRaises(SystemExit):
            self.console.do_quit(self.console)

    def test_do_EOF(self):
        """test_do_EOF Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(self.console.do_EOF(""))

    def test_emptyline(self):
        """test_emptyline Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertIsNone(self.console.emptyline())

    def test_do_create_error(self):
        """test_do_create_error Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("")
            self.assertEqual("** class name missing **\n",
                             f.getvalue())

    def test_do_create(self):
        """test_do_create Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("BaseModel")
        output = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_show("BaseModel {}".format(output))
        output2 = f.getvalue().strip()

        self.assertTrue(output in output2)

    def test_do_show_instance_not_found(self):
        """test_do_show_instance_not_found Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_show("BaseModel 1234")
            self.assertEqual("** no instance found **\n",
                             f.getvalue())

    def test_do_show_no_class(self):
        """test_do_show_no_class Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_show("")
            self.assertEqual("** class name missing **\n",
                             f.getvalue())

    def test_do_show_id_missing(self):
        """test_do_show_id_missing Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_show("BaseModel")
            self.assertEqual("** instance id missing **\n",
                             f.getvalue())

    def test_do_show_class_doesnt_exist(self):
        """test_do_show_class_doesnt_exist Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_show("JustModel")
            self.assertEqual("** class doesn't exist **\n",
                             f.getvalue())

    def test_do_show_correct(self):
        """test_do_show_correct Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_show("BaseModel \
                                  d42f98a5-71d3-4237-83f3-f480c9dc3c18")
            self.assertFalse("2023, 3, 8, 19, 30, 48, 436966"
                             in f.getvalue().strip())
            # self.assertTrue('2023, 3, 8, 19, 30, 48, 436849'
            #                 in f.getvalue().strip())

    def test_do_all(self):
        """test_do_all Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_all("")
            self.assertFalse("2023, 3, 8, 19, 30, 48, 436966"
                             in f.getvalue().strip())
            self.assertTrue('2023, 3, 8, 19, 30, 48, 436849'
                            in f.getvalue().strip())

        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("BaseModel")
            self.console.do_all("BaseModel")
            self.assertIn(str(list(storage.all().values())[0]),
                          f.getvalue())

    def test_all_error_class_doesnt_exist(self):
        """test_all_error_class_doesnt_exist Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_all("C")
        self.assertEqual(f.getvalue().strip(),
                         "** class doesn't exist **")

    def test_do_destroy_correct(self):
        """test_do_destroy_correct Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("BaseModel")
            all_objs = storage.all()
            obj_id = list(all_objs.values())[0].id
            self.console.do_destroy("BaseModel " + obj_id)
            self.assertTrue("BaseModel." + obj_id not in storage.all().keys())

    def test_destroy_error_class_doesnt_exist(self):
        """test_destroy_error_class_doesnt_exist Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_destroy("d3da85f2-499c-43cb-b33d-3d7935bc808c")
        self.assertEqual(f.getvalue().strip(),
                         "** class doesn't exist **")

    def test_destroy_error_class_missing(self):
        """test_destroy_error_class_missing Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_destroy("")
        self.assertEqual(f.getvalue().strip(),
                         "** class name missing **")

    def test_destroy_error_no_instance_found(self):
        """test_destroy_error_no_instance_found Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_destroy("BaseModel 1234")
        self.assertEqual(f.getvalue().strip(),
                         "** no instance found **")

    def test_destroy_error_id_instance_misssing(self):
        """test_destroy_error_id_instance_misssing Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_destroy("BaseModel")
        self.assertEqual(f.getvalue().strip(),
                         "** instance id missing **")

    def test_do_update_error(self):
        """test_do_update_error Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_update("BaseModel 1234")
            self.assertEqual("** no instance found **\n",
                             f.getvalue())

    def test_update_error_class_doesnt_exist(self):
        """test_update_error_class_doesnt_exist Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_update("TEst")
        self.assertEqual(f.getvalue().strip(),
                         "** class doesn't exist **")

    def test_update_error_class_missing(self):
        """test_update_error_class_missing Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_update("")
        self.assertEqual(f.getvalue().strip(),
                         "** class name missing **")

    def test_update_error_no_instance_found(self):
        """test_update_error_no_instance_found Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_update("BaseModel 1234")
        self.assertEqual(f.getvalue().strip(),
                         "** no instance found **")

    def test_update_error_id_instance_misssing(self):
        """test_update_error_id_instance_misssing Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_update("BaseModel")
        self.assertEqual(f.getvalue().strip(),
                         "** instance id missing **")

    def test_do_update_attr_missing(self):
        """test_do_update_attr_missing Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("User")
            all_objs = storage.all()
            obj_id = list(all_objs.values())[0].id
            self.console.do_update("User " + obj_id)
        self.assertEqual(f.getvalue().strip().split("\n")[1],
                         "** attribute name missing **")

    def test_do_update_attr_value_missing(self):
        """test_do_update_attr_value_missing Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("User")
            all_objs = storage.all()
            obj_id = list(all_objs.values())[0].id
            self.console.do_update("User " + obj_id + " first_name")
        self.assertEqual(f.getvalue().strip().split("\n")[1],
                         "** value missing **")

    def test_do_update_correct(self):
        """test_do_update_correct Docstring"""
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("BaseModel")
            all_objs = storage.all()
            obj_id = list(all_objs.values())[0].id
            self.console.do_update("BaseModel " + obj_id + " name 'test'")
            self.assertTrue("test" in getattr(list(storage.all().values())[0],
                            "name"))


class TestConsole_count(unittest.TestCase):
    """
    Unittests for .count() method
    """
    def setUp(self):
        """
        Setting up testing environment
        """
        self.console = HBNBCommand()
        # try:
        #     os.rename("file.json", "tmp")
        # except IOError:
        #     pass
        # FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        """
        Cleanup environment
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_valid(self):
        """
        Tests for .count() methods with correct input and output
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.console.do_create("BaseModel")
            self.console.do_create("User")
            self.console.do_create("State")
            self.console.do_create("Review")
            self.console.do_create("Place")
            self.console.do_create("City")
            self.console.do_create("Amenity")

        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("BaseModel.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("User.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("State.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("Review.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("Place.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("City.count()"))
            self.assertEqual("1", f.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("Amenity.count()"))
            self.assertEqual("1", f.getvalue().strip())

    def test_count_no_class(self):
        """
        Tests for .count() methods with correct input but no classes
        """
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("BaseModel.count()"))
            self.assertEqual("0", f.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
