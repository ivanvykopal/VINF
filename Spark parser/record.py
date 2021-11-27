class Record:

    def __init__(self, title=None, types=None, alternatives=None):
        self.title = title

        if not types:
            self.types = set()
        else:
            self.types = types

        if not alternatives:
            self.alts = set()
        else:
            self.alts = alternatives

    def __add__(self, b):
        return Record(
            self.title or b.title or None,
            self.types | b.types,
            self.alts | b.alts
        )

    def to_string(self):

        string = self.title + '\t'

        if self.types:
            string = string + 'TYPES\t'+ '\t'.join(self.types) + '\t'
        else:
            string = string + 'TYPES\t'

        if self.alts:
            string = string + 'ALTS\t' + '\t'.join(self.alts) + '\t'
        else:
            string = string + 'ALTS\t'

        return string