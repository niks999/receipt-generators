"""Receipt Generators Package"""

from .book import BookGenerator
from .driver import DriverGenerator
from .education import EducationGenerator
from .fuel import FuelGenerator
from .gadget import GadgetGenerator
from .internet import InternetGenerator

__all__ = ['FuelGenerator', 'DriverGenerator', 'InternetGenerator', 'EducationGenerator', 'BookGenerator', 'GadgetGenerator', 'GENERATOR_REGISTRY']

# Generator Registry - automatically map generator names to classes
GENERATOR_REGISTRY = {
    FuelGenerator.name: FuelGenerator,
    DriverGenerator.name: DriverGenerator,
    InternetGenerator.name: InternetGenerator,
    EducationGenerator.name: EducationGenerator,
    BookGenerator.name: BookGenerator,
    GadgetGenerator.name: GadgetGenerator,
}
