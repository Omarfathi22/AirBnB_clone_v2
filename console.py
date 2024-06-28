#!/usr/bin/python3
"""Command Line Interface Module for HBNB Project"""
import cmd
from datetime import datetime
import re
import os
import sys
import uuid

from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command Line Interface for managing HBNB project models"""

    # Determine the prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    # Mapping of model names to their corresponding classes
    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }

    # Commands that use dot notation for operation
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']

    # Types for attributes that require special handling
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints prompt if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformats command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # Check for the general format i.e., '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # Parse line left to right
            pline = line[:]  # Parsed line

            # Isolate <class name>
            _cls = pline[:pline.find('.')]

            # Isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # If parentheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # Partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # Pline convert to tuple

                # Isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # Possible bug here:
                # Empty quotes register as empty _id when replaced

                # If arguments exist beyond _id
                pline = pline[2].strip()  # Pline is now str
                if pline:
                    # Check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints prompt if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """Exit the HBNB console"""
        exit(0)

    def help_quit(self):
        """Prints help documentation for quit command"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        exit(0)

    def help_EOF(self):
        """Prints help documentation for EOF command"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the emptyline method of CMD"""
        return False

    def do_create(self, args):
        """Create an object of any class"""
        ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
        class_name = ''
        name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        class_match = re.match(name_pattern, args)
        obj_kwargs = {}
        if class_match is not None:
            class_name = class_match.group('name')
            params_str = args[len(class_name):].strip()
            params = params_str.split(' ')
            str_pattern = r'(?P<t_str>"([^"]|\")*")'
            float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
            int_pattern = r'(?P<t_int>[-+]?\d+)'
            param_pattern = '{}=({}|{}|{})'.format(
                name_pattern,
                str_pattern,
                float_pattern,
                int_pattern
            )
            for param in params:
                param_match = re.fullmatch(param_pattern, param)
                if param_match is not None:
                    key_name = param_match.group('name')
                    str_v = param_match.group('t_str')
                    float_v = param_match.group('t_float')
                    int_v = param_match.group('t_int')
                    if float_v is not None:
                        obj_kwargs[key_name] = float(float_v)
                    if int_v is not None:
                        obj_kwargs[key_name] = int(int_v)
                    if str_v is not None:
                        obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
        else:
            class_name = args
        if not class_name:
            print("** class name missing **")
            return
        elif class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if not hasattr(obj_kwargs, 'id'):
                obj_kwargs['id'] = str(uuid.uuid4())
            if not hasattr(obj_kwargs, 'created_at'):
                obj_kwargs['created_at'] = str(datetime.now())
            if not hasattr(obj_kwargs, 'updated_at'):
                obj_kwargs['updated_at'] = str(datetime.now())
            new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
            new_instance.save()
            print(new_instance.id)
        else:
            new_instance = HBNBCommand.classes[class_name]()
            for key, value in obj_kwargs.items():
                if key not in ignored_attrs:
                    setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

    def help_create(self):
        """Help information for the create method"""
        print("Creates an instance of a specified class")
        print("[Usage]: create <className> [<attrName>='<attrValue>']\n")

    def do_show(self, args):
        """Show details of a specific object"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # Guard against trailing arguments
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Help information for the show method"""
        print("Displays details of a specific instance")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Deletes an object specified by class name and id"""
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            storage.delete(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Help information for the destroy method"""
        print("Deletes a specified instance by class name and id")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Lists all instances or all instances of a specified class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # Remove possible trailing arguments
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = 0
        for k, v in storage.all().items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """Prints help documentation for count command"""
        print("Counts the number of instances of a specified class")
        print("Usage: count <class_name>\n")

    def do_update(self, args):
        """Updates attributes of a specified object"""
        c_name = c_id = att_name = att_val = kwargs = ''

        # Isolate class name from id/arguments, e.g., (<class>, delim, <id/arguments>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else:  # Class name not provided
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # Invalid class name
            print("** class doesn't exist **")
            return

        # Isolate id from arguments
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else:  # ID not provided
            print("** instance id missing **")
            return

        # Generate key from class name and id
        key = c_name + "." + c_id

        # Check if key exists in storage
        if key not in storage.all():
            print("** no instance found **")
            return

        # Determine if kwargs or arguments are provided
        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []  # Reformat kwargs into list, e.g., [<name>, <value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # Isolate arguments
            args = args[2]
            if args and args[0] == '\"':  # Check for quoted argument
                second_quote = args.find('\"', 1)
                att_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            # If attribute name was not quoted
            if not att_name and args[0] != ' ':
                att_name = args[0]
            # Check for quoted value argument
            if args[2] and args[2][0] == '\"':
                att_val = args[2][1:args[2].find('\"', 1)]

            # If attribute value was not quoted
            if not att_val and args[2]:
                att_val = args[2].partition(' ')[0]

            args = [att_name, att_val]

        # Retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # Iterate through attribute names and values
        for i, att_name in enumerate(args):
            # Block runs only on even iterations
            if (i % 2 == 0):
                att_val = args[i + 1]  # Following item is value
                if not att_name:  # Check for attribute name
                    print("** attribute name missing **")
                    return
                if not att_val:  # Check for attribute value
                    print("** value missing **")
                    return
                # Type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # Update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # Save updates to file

    def help_update(self):
        """Help information for the update command"""
        print("Updates attributes of a specified object")
        print("Usage: update <className> <objectId> <attributeName> <attributeValue>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
    
