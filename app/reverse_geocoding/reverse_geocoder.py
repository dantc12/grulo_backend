import abc

from .place import Place


class ReverseGeocoder(abc.ABC):

    @abc.abstractmethod
    def reverse_geocode(self, lat: str, lon: str) -> Place:
        pass
