import sys
from fprime_gds.plugin.definitions import gds_plugin_implementation
from fprime_gds.executables.apps import GdsApp

class MyApp(GdsApp):
    """ An app for the GDS """

    def __init__(self, message):
        """ Constructor """
        super().__init__()
        self.message = message

    def get_process_invocation(self):
        """ Process invocation """
        # Inject message into command line to print
        return [sys.executable, "-c", f"print(f'{self.message}')"]

    @classmethod
    def get_name(cls):
        """ Get name """
        return "my-app"
    
    @classmethod
    def get_arguments(cls):
        """ Get arguments """
        return {
            ("--message", ): {
                "type": str,
                "help": "Message to print",
                "required": True
            }
        }

    @classmethod
    def check_arguments(cls, message):
        """ Check arguments """
        if "'" in message or '\n' in message:
            raise ValueError("--message must not include ' nor a newline")
  
    @classmethod
    @gds_plugin_implementation
    def register_gds_app_plugin(cls):
        """ Register a good plugin """
        return cls
