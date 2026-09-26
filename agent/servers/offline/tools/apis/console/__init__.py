from rich.console import Console
class ConsoleLogger:
    def __init__(self):
        self.console = Console()
        self.verbose = False  # logging disabled by default
        
    def reset(self, verbose):
        self.verbose = verbose
    
    def print(self, *args):
        self.console.print(*args)
        
    def log(self, *args):
        if self.verbose:
            self.console.log(*args)
        else:
            # If logging is not enabled, do nothing
            pass
        
console_model = ConsoleLogger()
console_model.reset(False)  # set to keep logging disabled