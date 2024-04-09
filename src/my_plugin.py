from fprime_gds.common.communication.framing import FramerDeframer
from fprime_gds.plugin.definitions import gds_plugin_implementation

class MyPlugin(FramerDeframer):
    START_TOKEN = b"MY-PLUGIN"
    
    def frame(self, data):
        """ Frames data with 'MY-PLUGIN' start token """
        return self.START_TOKEN + data

    def deframe(self, data, no_copy=False):
        """ Deframe data with 'MY-PLUGIN' start token """
        discarded = b""
        data = data if no_copy else b"" + data # Copy data if no_copy
        
        # Deframing can deframe until data length isn't enough to provide start token
        while len(data) > len(self.START_TOKEN):
            # Starts with start word and a second start word found
            if data[:len(self.START_TOKEN)] == self.START_TOKEN and self.START_TOKEN in data[1:]:
                data = data[len(self.START_TOKEN):] # Remove initial start token
                # Return packet (data to next start token), unconsumed data, and discarded data
                return data[:data.index(self.START_TOKEN)], data[data.index(self.START_TOKEN):], discarded
            # Starts with start token, but beginning of next packet was not found
            elif data[:len(self.START_TOKEN)] == self.START_TOKEN:
                # Wait for new data
                break
            # Does not start with requested token throw away one byte and continue
            else:
                discarded += data[1]
                data[1:]
                continue
        # No packet found, all data unconsumed, and discarded
        return None, data, discarded
    
    @classmethod
    def get_name(cls):
        """ Name of this implementation provided to CLI """
        return "my-plugin"

    @classmethod
    def get_arguments(cls):
        """ Arguments to request from the CLI """
        return {}

    @classmethod
    def check_arguments(cls):
        """ Check arguments from the CLI """
        pass

    @classmethod
    @gds_plugin_implementation
    def register_framing_plugin(cls):
        """ Register the MyPlugin plugin """
        return cls
