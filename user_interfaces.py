
class ConsoleOutput(object):

    def print(self, msg):
        print(msg)

    @staticmethod
    def _s_print(msg):
        print(msg)

##########################

class ConsoleInput(object):

        def pulsa_intro(self):
            ConsoleOutput._s_print("Pulsa Enter...")
            self.input()

        def input(self, prompt = ""):
            return input(prompt)

