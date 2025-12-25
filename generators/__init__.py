"""Receipt Generators Package"""

from .driver import DriverGenerator
from .education import EducationGenerator
from .fuel import FuelGenerator
from .internet import InternetGenerator

__all__ = ['FuelGenerator', 'DriverGenerator', 'InternetGenerator', 'EducationGenerator', 'GENERATOR_REGISTRY']

# Generator Registry - automatically map generator names to classes
GENERATOR_REGISTRY = {
    FuelGenerator.name: FuelGenerator,
    DriverGenerator.name: DriverGenerator,
    InternetGenerator.name: InternetGenerator,
    EducationGenerator.name: EducationGenerator,
}
