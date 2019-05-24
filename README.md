
#### Goals:
* I really don't want to pollute another of my systems with Python2 development environments, no, not even in a virtualenv. 
* I don't really want to lose access to all of the lovely exploits in exploitdb with that pedantry
* I want to have command line arguments for these exploits to avoid rampant code editing
* I don't want credit for making these exploits, I just want them in Python3
* PEP 8, four spaces as tabs

#### How are we getting there: 
Dynamically loaded modules loaded at runtime based on the first argument provided to the watchdog script

#### basic.Exploit
This is the super class that exploits need to belong to in order to function in the framework

#### oops.*Exception
This is where we store various error types that are based on framework errors. If your code needs its own errors please locate them inside your exploit's python file

#### TotsModule
Your module's class should be named TotsModule. Yes I know thousands of files with the same class name sounds chaotic and terrible. It isn't


##Sample Module
```python
# We need these imports, you don't have to do it exactly like this, but we need access to the Exploit class from basic.
from basic import Exploit
import oops

# We need to create the class and initialize the module and the Exploit superclass
class TotsModule(Exploit):
    def __init__(self, provided_argument_string=""):
        super().__init__(provided_argument_string)

# The local arguments function let's us define what kind of variables that we need, as well as the number of them, where they should be stored, the default values and their help information.
# When this is complete the TotsModule will have class variables that are related to all of the arguments below:
# EG: this will create self.target, self.directory, self.username, self.password
    def local_arguments(self):
        return [
            {"name": "target", "type": str, "nargs": "+", "help": "Target for the exploit",
             "default": "http://SLD.TLD"},
            {"name": "directory", "type": str, "nargs": "+", "help": "Directory for the exploit",
             "default": "/admin/Cms_Wysiwyg/directive/index"},
            {"name": "username", "type": str, "nargs": "+", "help": "User to add",
             "default": "forme"},
            {"name": "password", "type": str, "nargs": "+", "help": "Password for the User",
             "default": "forme"},
        ]
        
# This is where all of your exploit code goes, You have the arguments converted to class variables, do the things.
    def exploit(self):
        pass
    
# This shows when there are issues with the arguments provided to the CLI, it really should print
    def help(self):
        print("""
        Some Help Information
        """)
    
# Please don't be a jerk, People included the thanks in their submissions for a reason, include them here.
    def thanks(self):
        return """
        All of the thanks that appear in the respective module, I especially don't want to lose the badass ASCII ART
        """
    
```