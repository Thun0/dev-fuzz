class Generator:

    def __init__(self):
        pass

    def generate_from_template(self, filepath):
        with open(filepath) as file:
            template = file.read()
            self.parse(template)

    def parse_template(self, template):
        pass
