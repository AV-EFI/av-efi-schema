"""Patched version of defailt LinkML pydanticgen module."""

import keyword
from typing import Callable

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, Template
from linkml.generators import pydanticgen
from linkml.generators.pydanticgen.template import (
    PydanticAttribute, PydanticTemplateModel,
)
from pydantic import computed_field

class PydanticGenerator(pydanticgen.PydanticGenerator):
    def _template_environment(self) -> Environment:
        env = PydanticTemplateModel.environment()
        env.filters['is_keyword'] = keyword.iskeyword
        if self.template_dir is not None:
            loader = ChoiceLoader([FileSystemLoader(self.template_dir), env.loader])
            env.loader = loader
        return env


def init_empty_lists(
        func: Callable[[PydanticAttribute], str],
) -> Callable[[PydanticAttribute], str]:
    def wrapper(self: PydanticAttribute) -> str:
        result = func(self)
        if self.multivalued and result == "None":
            return "[]"
        else:
            return result
    return wrapper

PydanticAttribute.field = computed_field(init_empty_lists(
    PydanticAttribute.field.fget))
