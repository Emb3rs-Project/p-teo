

from dataclasses import dataclass, field

from error_handling.module_exception import ModuleException


@dataclass
class ModuleRuntimeException(ModuleException):
    type : str = field(default='buildmodel.py')