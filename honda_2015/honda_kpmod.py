from km3pipe import Module
from honda_2015 import HondaFlux


class HondaMod(Module):
    """Get the Honda 2015 fluxes.

    """
    def __init__(self, **context):
        super(self.__class__, self).__init__(**context)
        self.honda = HondaFlux()

    def process(self, blob):
        zen = blob['McNu']['zenith']
        ene = blob['McNu']['energy']
        flav = blob['McNu']['flavor']
        blob['Honda2015'] = self.honda(flav, zen, ene)
