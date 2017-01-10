from km3pipe import Module
from honda_2015 import HondaFlux


class HondaMod(Module):
    """Get the Honda 2015 fluxes.

    """
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.key = self.require('key')
        self.average = self.get('average') or True
        self.honda = HondaFlux()

    def process(self, blob):
        if self.key not in blob:
            return blob
        flav = blob[self.key]['flavor']
        ene = blob[self.key]['energy']
        if self.average:
            zen = None
        else:
            zen = blob[self.key]['zenith']
        blob['Honda2015'] = self.honda.get(flav, ene, zen)
        return blob
