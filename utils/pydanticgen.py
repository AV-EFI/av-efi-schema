"""Patched version of defailt LinkML pydanticgen module."""

import keyword

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, Template
from linkml.generators import pydanticgen
from linkml.generators.pydanticgen.template import PydanticTemplateModel

class PydanticGenerator(pydanticgen.PydanticGenerator):
    def _template_environment(self) -> Environment:
        env = PydanticTemplateModel.environment()
        env.filters['is_keyword'] = keyword.iskeyword
        if self.template_dir is not None:
            loader = ChoiceLoader([FileSystemLoader(self.template_dir), env.loader])
            env.loader = loader
        return env
