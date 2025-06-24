from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_curi_maps': ['semweb_context'],
     'default_prefix': 'avefi',
     'default_range': 'string',
     'description': 'Metadata schema for persistent film identifiers developed in '
                    'the\n'
                    'AVefi project. See also the corresponding [Entity relation\n'
                    'diagram](https://github.com/AV-EFI/av-efi-schema/blob/main/avefi_er_diagram.md).\n'
                    'Additionally, consult the [FIAF Moving Image Cataloguing\n'
                    'Manual](https://www.fiafnet.org/pages/E-Resources/Cataloguing-Manual.html)\n'
                    'and the [FIAF Glossary of Filmographic\n'
                    'Terms](https://www.fiafnet.org/images/tinyUpload/E-Resources/Reports-Glossaries-And-Papers/GlossaryMasterCombo19.htm)\n'
                    'as indicated in the documentation below for definitions, '
                    'usage\n'
                    'instructions and best practices',
     'emit_prefixes': ['fiaf', 'owl', 'rdf', 'rdfs', 'xsd'],
     'id': 'https://av-efi.github.io/av-efi-schema/model',
     'imports': ['linkml:types', 'vocab'],
     'name': 'model',
     'prefixes': {'avefi': {'prefix_prefix': 'avefi',
                            'prefix_reference': 'https://av-efi.net/av-efi-schema/'},
                  'fiaf': {'prefix_prefix': 'fiaf',
                           'prefix_reference': 'https://fiafcore.org/ontology/'},
                  'foaf': {'prefix_prefix': 'foaf',
                           'prefix_reference': 'http://xmlns.com/foaf/0.1/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'rdf': {'prefix_prefix': 'rdf',
                          'prefix_reference': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'},
                  'unit': {'prefix_prefix': 'unit',
                           'prefix_reference': 'http://qudt.org/vocab/unit/'},
                  'wdrs': {'prefix_prefix': 'wdrs',
                           'prefix_reference': 'http://www.w3.org/2007/05/powder-s#'}},
     'source_file': '/home/eo/src/av-efi/av-efi-schema/src/avefi_schema/model.yaml',
     'subsets': {'TypeRegistrySubset': {'description': 'Classes that are to be '
                                                       'implemented as infoTypes '
                                                       'in the type registry',
                                        'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                                        'name': 'TypeRegistrySubset'}},
     'title': 'AVefi data model',
     'types': {'AVefi': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                  'value': {'maxLength': 256,
                                                                            'minLength': 1}},
                                         'pid': {'tag': 'pid',
                                                 'value': '21.T11969/10a6d4dc54ac4827a50b'}},
                         'description': 'Handle with the prefix allocated for '
                                        'AVefi (eventually)',
                         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                         'in_subset': ['TypeRegistrySubset'],
                         'name': 'AVefi',
                         'pattern': '^21(\\.([0-9A-Za-z])+)*/[!-~]+$',
                         'typeof': 'string'},
               'AVefiCurie': {'annotations': {'pid': {'tag': 'pid',
                                                      'value': '21.T11969/5ccbf9c9c5fc1bc34df8'}},
                              'description': 'To be used as range for type '
                                             'designator slots, i.e. const values',
                              'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                              'in_subset': ['TypeRegistrySubset'],
                              'name': 'AVefiCurie',
                              'typeof': 'uriorcurie'},
               'DOI': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                'value': {'maxLength': 256,
                                                                          'minLength': 1}},
                                       'pid': {'tag': 'pid',
                                               'value': '21.T11969/94dbc30c6c4a38e84e6f'}},
                       'description': 'Digital Object Identifier maintained by the '
                                      'DOI Foundation and commonly used for '
                                      'scientific publications including films',
                       'examples': [{'description': 'DOI for "The FIAF Moving '
                                                    'Image Cataloguing Manual"',
                                     'value': '10.2307/j.ctt2005t2g'},
                                    {'description': 'DOI for "DOI Handbook"',
                                     'value': '10.1000/182'}],
                       'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                       'in_subset': ['TypeRegistrySubset'],
                       'name': 'DOI',
                       'pattern': '^10\\.[0-9]{4,9}(\\.[0-9]+)*(/|%2F)((?![\\"&\\\'])\\S)+$',
                       'see_also': ['https://dx.doi.org/',
                                    'https://www.wikidata.org/wiki/Property:P356'],
                       'typeof': 'string'},
               'Decimal': {'annotations': {'pid': {'tag': 'pid',
                                                   'value': '21.T11969/fcbe592c37410a1b261d'}},
                           'description': 'Decimal numbers',
                           'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                           'in_subset': ['TypeRegistrySubset'],
                           'name': 'Decimal',
                           'typeof': 'decimal'},
               'EIDR': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                 'value': {'maxLength': 256,
                                                                           'minLength': 1}},
                                        'pid': {'tag': 'pid',
                                                'value': '21.T11969/99119b0c92c93022d478'}},
                        'description': 'Entertainment Identifier Registry ID',
                        'examples': [{'description': 'EIDR for "The Simpsons"',
                                      'value': '10.5240/58DD-06EB-3EED-A705-EE28-7'}],
                        'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                        'in_subset': ['TypeRegistrySubset'],
                        'name': 'EIDR',
                        'pattern': '^10\\.5240(/|%2F)((?![\\"&\\\'])\\S)+$',
                        'see_also': ['https://www.eidr.org/',
                                     'https://www.wikidata.org/wiki/Property:P2704'],
                        'typeof': 'string'},
               'FilmportalID': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                         'value': {'maxLength': 256,
                                                                                   'minLength': 1}},
                                                'pid': {'tag': 'pid',
                                                        'value': '21.T11969/4099938c39f6b2a57877'}},
                                'description': 'Identifier of the German '
                                               'Filmportal.de',
                                'examples': [{'description': 'Filmportal-ID for '
                                                             'creative work '
                                                             '"Nosferatu"',
                                              'value': 'd70835e558264328a39112994449d17f'},
                                             {'description': 'Filmportal-ID for '
                                                             'person "Rainer '
                                                             'Werner Fassbinder"',
                                              'value': 'a89f90efdb664915ad2651ff0406736f'}],
                                'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                                'in_subset': ['TypeRegistrySubset'],
                                'name': 'FilmportalID',
                                'pattern': '^[\\da-f]{32}$',
                                'see_also': ['https://www.filmportal.de/',
                                             'https://www.wikidata.org/entity/P2639'],
                                'typeof': 'string'},
               'GNDID': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                  'value': {'maxLength': 256,
                                                                            'minLength': 1}},
                                         'pid': {'tag': 'pid',
                                                 'value': '21.T11969/85336bee084e8645831d'}},
                         'description': 'Gemeinsame Normdatei (GND) identifier '
                                        'maintained by Deutsche Nationalbibliothek '
                                        '(German National Library)',
                         'examples': [{'description': 'GND-ID for creative work '
                                                      '"Nosferatu"',
                                       'value': '4228455-7'},
                                      {'description': 'GND-ID for place "Frankfurt '
                                                      'am Main"',
                                       'value': '4018118-2'},
                                      {'description': 'GND-ID for organization '
                                                      '"Deutsche '
                                                      'Nationalbibliothek"',
                                       'value': '10140798-1'},
                                      {'description': 'GND-ID for person "Rainer '
                                                      'Werner Fassbinder"',
                                       'value': '118532022'},
                                      {'description': 'GND-ID for subject heading '
                                                      '"Vampir"',
                                       'value': '4187368-3'}],
                         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                         'in_subset': ['TypeRegistrySubset'],
                         'name': 'GNDID',
                         'pattern': '^[-\\dX]+$',
                         'see_also': ['https://www.wikidata.org/entity/P227'],
                         'typeof': 'string'},
               'HttpUri': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                    'value': {'maxLength': 512}},
                                           'pid': {'tag': 'pid',
                                                   'value': '21.T11969/4f13820c6cdbd8a7136f'}},
                           'description': 'Full URI starting with http or https',
                           'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                           'in_subset': ['TypeRegistrySubset'],
                           'name': 'HttpUri',
                           'pattern': '^https?://[^/?#]+(/[^?#]*(\\?([^#]*))?(#(.*))?)?$',
                           'typeof': 'uri'},
               'IDString': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                     'value': {'maxLength': 256,
                                                                               'minLength': 1}},
                                            'pid': {'tag': 'pid',
                                                    'value': '21.T11969/4af5369dc8358733d34c'}},
                            'description': 'ASCII string suitable for identifiers',
                            'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                            'in_subset': ['TypeRegistrySubset'],
                            'name': 'IDString',
                            'pattern': '^((?![\\"&\\\'])\\S)+$',
                            'typeof': 'string'},
               'ISIL': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                 'value': {'maxLength': 256,
                                                                           'minLength': 1}},
                                        'pid': {'tag': 'pid',
                                                'value': '21.T11969/0f04aac5809944fbe63f'}},
                        'description': 'International Standard Identifier for '
                                       'Libraries and Related Organizations '
                                       'including (film) archives',
                        'examples': [{'description': 'ISIL-ID for organization '
                                                     '"Filmmuseum Düsseldorf"',
                                      'value': 'DE-MUS-432511'},
                                     {'description': 'ISIL-ID for organization '
                                                     '"Deutsche Kinemathek"',
                                      'value': 'DE-B1528'}],
                        'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                        'in_subset': ['TypeRegistrySubset'],
                        'name': 'ISIL',
                        'pattern': '^[A-Z]{2}-[A-Za-z\\-0-9:/]{1,15}$',
                        'see_also': ['https://biblstandard.dk/isil/index.htm',
                                     'https://www.wikidata.org/wiki/Property:P791'],
                        'typeof': 'string'},
               'ISODate': {'annotations': {'pid': {'tag': 'pid',
                                                   'value': '21.T11969/90ce854c789144a37fb7'}},
                           'description': 'ISO 8601 date or interval/period, more '
                                          'specifically, EDTF conformance level 0 '
                                          'as well as qualifiers ? (uncertain '
                                          'date) and ~ (approximate date). See '
                                          'examples and references for more '
                                          'information',
                           'examples': [{'description': 'complete date, i.e. year, '
                                                        'month and day',
                                         'value': '2024-04-24'},
                                        {'description': 'year and month',
                                         'value': '2024-04'},
                                        {'description': 'year only',
                                         'value': '2024'},
                                        {'description': 'approximate date (2024 or '
                                                        'at least close to 2024)',
                                         'value': '2024~'},
                                        {'description': 'uncertain date (2024 or '
                                                        'may be something '
                                                        'different)',
                                         'value': '2024?'},
                                        {'description': 'interval (2023 until '
                                                        '2024)',
                                         'value': '2023/2024'}],
                           'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                           'in_subset': ['TypeRegistrySubset'],
                           'name': 'ISODate',
                           'pattern': '^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$',
                           'see_also': ['https://www.loc.gov/standards/datetime/'],
                           'typeof': 'string'},
               'ISODateTimeUTC': {'annotations': {'pid': {'tag': 'pid',
                                                          'value': '21.T11969/27064b567b4f9f7017ae'}},
                                  'description': 'Timestamp in UTC',
                                  'examples': [{'value': '2024-04-24 '
                                                         '16:36:14+00:00'}],
                                  'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                                  'in_subset': ['TypeRegistrySubset'],
                                  'name': 'ISODateTimeUTC',
                                  'pattern': '^2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\\.[0-9]+)?(Z|\\+00:00)$',
                                  'typeof': 'datetime'},
               'ISODurationInHours': {'annotations': {'pid': {'tag': 'pid',
                                                              'value': '21.T11969/a9cc3bf7aa659fe0f9e5'}},
                                      'description': 'ISO 8601 duration format. '
                                                     'See examples',
                                      'examples': [{'description': '3 hours, 18 '
                                                                   'minutes, 45 '
                                                                   'seconds',
                                                    'value': 'PT03H18M45S'},
                                                   {'description': '2 hours, 9 '
                                                                   'minutes',
                                                    'value': 'PT02H09M00S'},
                                                   {'description': '6 minutes, 12 '
                                                                   'seconds',
                                                    'value': 'PT00H06M12S'}],
                                      'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                                      'in_subset': ['TypeRegistrySubset'],
                                      'name': 'ISODurationInHours',
                                      'notes': ['https://www.w3.org/TR/xmlschema11-2/#duration'],
                                      'pattern': '^PT[1-9]*[0-9][0-9]H[0-5][0-9]M[0-5][0-9]S$',
                                      'typeof': 'string'},
               'TGNID': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                  'value': {'maxLength': 256,
                                                                            'minLength': 1}},
                                         'pid': {'tag': 'pid',
                                                 'value': '21.T11969/279a437ca7ffc31a26d6'}},
                         'description': 'Getty Thesaurus of Geographic Names ID',
                         'examples': [{'description': 'TGN-ID for place '
                                                      '"Göttingen"',
                                       'value': '7183809'},
                                      {'description': 'TGN-ID for place "Hannover"',
                                       'value': '7013260'}],
                         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                         'in_subset': ['TypeRegistrySubset'],
                         'name': 'TGNID',
                         'pattern': '^[1-9][0-9]{6}$',
                         'see_also': ['https://www.getty.edu/research/tools/vocabularies/tgn/index.html',
                                      'https://vocab.getty.edu/resource?uri=http://vocab.getty.edu/dataset/tgn',
                                      'https://www.wikidata.org/wiki/Property:P1667'],
                         'typeof': 'string'},
               'TextArea': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                     'value': {'maxLength': 8192,
                                                                               'minLength': 1}},
                                            'pid': {'tag': 'pid',
                                                    'value': '21.T11969/8717ca7ca5aff686b379'}},
                            'description': 'Non-empty string possibly containing '
                                           'line breaks',
                            'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                            'in_subset': ['TypeRegistrySubset'],
                            'name': 'TextArea',
                            'typeof': 'string'},
               'TextLine': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                     'value': {'maxLength': 250,
                                                                               'minLength': 1}},
                                            'pid': {'tag': 'pid',
                                                    'value': '21.T11969/7ac5a4f0445cbffc6a27'}},
                            'description': 'Non-empty string without line breaks '
                                           'intended for names and similar data',
                            'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                            'in_subset': ['TypeRegistrySubset'],
                            'name': 'TextLine',
                            'pattern': '^.+$',
                            'typeof': 'string'},
               'VIAFID': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                   'value': {'maxLength': 256,
                                                                             'minLength': 1}},
                                          'pid': {'tag': 'pid',
                                                  'value': '21.T11969/815abb512b729cbe019d'}},
                          'description': 'Virtual International Authority File '
                                         'identifier',
                          'examples': [{'description': 'VIAF-ID for creative work '
                                                       '"Nosferatu"',
                                        'value': '316753491'},
                                       {'description': 'VIAF-ID for place "Berlin"',
                                        'value': '122530980'},
                                       {'description': 'VIAF-ID for organization '
                                                       '"International Federation '
                                                       'of Film Archives"',
                                        'value': '7183809'},
                                       {'description': 'VIAF-ID for person "Rainer '
                                                       'Werner Fassbinder"',
                                        'value': '66467014'}],
                          'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                          'in_subset': ['TypeRegistrySubset'],
                          'name': 'VIAFID',
                          'pattern': '^\\d+$',
                          'see_also': ['https://viaf.org/',
                                       'https://www.wikidata.org/entity/P214'],
                          'typeof': 'string'},
               'WikidataID': {'annotations': {'data_type_properties': {'tag': 'data_type_properties',
                                                                       'value': {'maxLength': 256,
                                                                                 'minLength': 1}},
                                              'pid': {'tag': 'pid',
                                                      'value': '21.T11969/fa9d47f9d4107f21daa2'}},
                              'description': 'Identifier for Wikidata entities',
                              'examples': [{'description': 'Wikidata-ID for '
                                                           'creative work '
                                                           '"Nosferatu"',
                                            'value': 'Q151895'},
                                           {'description': 'Wikidata-ID for place '
                                                           '"Berlin"',
                                            'value': 'Q64'},
                                           {'description': 'Wikidata-ID for '
                                                           'organization '
                                                           '"International '
                                                           'Federation of Film '
                                                           'Archives"',
                                            'value': 'Q586693'},
                                           {'description': 'Wikidata-ID for person '
                                                           '"Rainer Werner '
                                                           'Fassbinder"',
                                            'value': 'Q44426'},
                                           {'description': 'Wikidata-ID for '
                                                           'subject heading '
                                                           '"Vampire"',
                                            'value': 'Q46721'}],
                              'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
                              'in_subset': ['TypeRegistrySubset'],
                              'name': 'WikidataID',
                              'pattern': '^[LPQ]\\d+$',
                              'see_also': ['https://www.wikidata.org/wiki/Wikidata:Identifiers'],
                              'typeof': 'string'}}} )

class AnimationActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.13
    """
    # FIAF Glossary of Filmographic Terms B.13.1
    Animation = "Animation"
    # FIAF Glossary of Filmographic Terms B.13.9
    AnimationDirector = "AnimationDirector"
    # FIAF Glossary of Filmographic Terms B.13.19
    AnimationLighter = "AnimationLighter"
    # FIAF Glossary of Filmographic Terms B.13.11
    Animator = "Animator"
    # FIAF Glossary of Filmographic Terms B.13.14
    CharacterDesigner = "CharacterDesigner"
    # FIAF Glossary of Filmographic Terms B.13.15
    Cleanup = "Cleanup"
    # FIAF Glossary of Filmographic Terms B.13.10
    LeadAnimator = "LeadAnimator"
    # FIAF Glossary of Filmographic Terms B.13.17
    ModelMaker = "ModelMaker"


class CastActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.7
    """
    # FIAF Glossary of Filmographic Terms B.7.12
    AnimalTrainer = "AnimalTrainer"
    # FIAF Glossary of Filmographic Terms B.7.1
    CastMember = "CastMember"
    # FIAF Glossary of Filmographic Terms B.7.5
    Dancer = "Dancer"
    # FIAF Glossary of Filmographic Terms B.7.8
    DialogueCoach = "DialogueCoach"
    # FIAF Glossary of Filmographic Terms B.7.2
    Double = "Double"
    # FIAF Glossary of Filmographic Terms B.7.4
    Extra = "Extra"
    # FIAF Glossary of Filmographic Terms B.7.9
    Interviewer = "Interviewer"
    # FIAF Glossary of Filmographic Terms B.7.10
    Narrator = "Narrator"
    # FIAF Glossary of Filmographic Terms B.7.6
    Singer = "Singer"
    # FIAF Glossary of Filmographic Terms B.7.3
    StandIn = "StandIn"
    # FIAF Glossary of Filmographic Terms B.7.11
    StuntPerformer = "StuntPerformer"
    # FIAF Glossary of Filmographic Terms B.7.7
    Voices = "Voices"
    # FIAF Glossary of Filmographic Terms B.7.13
    Wrangler = "Wrangler"


class CensorshipActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.1
    """
    # FIAF Glossary of Filmographic Terms C.1.1
    Censor = "Censor"


class CinematographyActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.5
    """
    # FIAF Glossary of Filmographic Terms B.5.4
    AerialPhotography = "AerialPhotography"
    # FIAF Glossary of Filmographic Terms B.5.12
    BestBoy = "BestBoy"
    # FIAF Glossary of Filmographic Terms B.5.7
    CameraAssistant = "CameraAssistant"
    # FIAF Glossary of Filmographic Terms B.5.3
    CameraOperator = "CameraOperator"
    # FIAF Glossary of Filmographic Terms B.5.1
    Cinematographer = "Cinematographer"
    # FIAF Glossary of Filmographic Terms B.5.19
    ColorConsultant = "ColorConsultant"
    # FIAF Glossary of Filmographic Terms B.5.16
    CraneOperator = "CraneOperator"
    # FIAF Glossary of Filmographic Terms B.5.15
    DollyGrip = "DollyGrip"
    # FIAF Glossary of Filmographic Terms B.5.13
    Electrician = "Electrician"
    # FIAF Glossary of Filmographic Terms B.5.8
    FocusPuller = "FocusPuller"
    # FIAF Glossary of Filmographic Terms B.5.11
    GafferLighting = "GafferLighting"
    # FIAF Glossary of Filmographic Terms B.5.17
    GeneratorOperator = "GeneratorOperator"
    # FIAF Glossary of Filmographic Terms B.5.14
    Grip = "Grip"
    # FIAF Glossary of Filmographic Terms B.5.20
    Lenses = "Lenses"
    # FIAF Glossary of Filmographic Terms B.5.9
    LoaderClapper = "LoaderClapper"
    # FIAF Glossary of Filmographic Terms B.5.2
    SecondUnitDirectorofPhotography = "SecondUnitDirectorofPhotography"
    # FIAF Glossary of Filmographic Terms B.5.6
    SteadicamOperator = "SteadicamOperator"
    # FIAF Glossary of Filmographic Terms B.5.18
    StillPhotographer = "StillPhotographer"
    # FIAF Glossary of Filmographic Terms B.5.5
    UnderwaterPhotography = "UnderwaterPhotography"
    # FIAF Glossary of Filmographic Terms B.5.10
    VideoAssist = "VideoAssist"


class CopyrightAndDistributionActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.2
    """
    # FIAF Glossary of Filmographic Terms C.2.3
    Distributor = "Distributor"
    # FIAF Glossary of Filmographic Terms C.2.6
    NationalDistributor = "NationalDistributor"
    # FIAF Glossary of Filmographic Terms C.2.1
    OriginalCopyrightOwner = "OriginalCopyrightOwner"
    # FIAF Glossary of Filmographic Terms C.2.4
    OriginalDistributor = "OriginalDistributor"
    # FIAF Glossary of Filmographic Terms C.2.2
    PresentCopyrightOwner = "PresentCopyrightOwner"
    # FIAF Glossary of Filmographic Terms C.2.7
    RegionalDistributor = "RegionalDistributor"
    # FIAF Glossary of Filmographic Terms C.2.5
    WorldDistributor = "WorldDistributor"


class DirectingActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.3
    """
    # FIAF Glossary of Filmographic Terms B.3.2
    AssistantDirector = "AssistantDirector"
    # FIAF Glossary of Filmographic Terms B.3.4
    CastingDirector = "CastingDirector"
    # FIAF Glossary of Filmographic Terms B.3.5
    Continuity = "Continuity"
    # FIAF Glossary of Filmographic Terms B.3.1
    Director = "Director"
    # FIAF Glossary of Filmographic Terms B.3.7
    FightArranger = "FightArranger"
    # FIAF Glossary of Filmographic Terms B.3.3
    SecondUnitDirector = "SecondUnitDirector"
    # FIAF Glossary of Filmographic Terms B.3.6
    StuntArranger = "StuntArranger"


class EditingActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.10
    """
    # FIAF Glossary of Filmographic Terms B.10.2
    AssistantFilmEditor = "AssistantFilmEditor"
    # Person responsible content-wise in a non-fiction film production, e.g. a documentary. Unlike a film editor, this activity includes duties like writing a concept, drafting the story, and preparing interviews in preproduction as well as supervising and supporting the camera team
    Editor = "Editor"
    # FIAF Glossary of Filmographic Terms B.10.1
    FilmEditor = "FilmEditor"


class LaboratoryActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.12
    """
    # FIAF Glossary of Filmographic Terms B.12.4
    Colorist = "Colorist"
    # FIAF Glossary of Filmographic Terms B.12.1
    Laboratory = "Laboratory"
    # FIAF Glossary of Filmographic Terms B.12.2
    LaboratoryTechnician = "LaboratoryTechnician"
    # FIAF Glossary of Filmographic Terms B.12.3
    NegativeCutter = "NegativeCutter"


class MusicActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.11
    """
    # FIAF Glossary of Filmographic Terms B.11.15
    Choreographer = "Choreographer"
    # FIAF Glossary of Filmographic Terms B.11.1
    Composer = "Composer"
    # FIAF Glossary of Filmographic Terms B.11.13
    Lyricist = "Lyricist"
    # FIAF Glossary of Filmographic Terms B.11.4
    MusicArranger = "MusicArranger"
    # FIAF Glossary of Filmographic Terms B.11.6
    MusicConductor = "MusicConductor"
    # FIAF Glossary of Filmographic Terms B.11.9
    MusicContractor = "MusicContractor"
    # FIAF Glossary of Filmographic Terms B.11.14
    MusicEditor = "MusicEditor"
    # FIAF Glossary of Filmographic Terms B.11.7
    MusicPerformer = "MusicPerformer"
    # FIAF Glossary of Filmographic Terms B.11.3
    MusicSupervisor = "MusicSupervisor"
    # FIAF Glossary of Filmographic Terms B.11.8
    SingingVoice = "SingingVoice"
    # FIAF Glossary of Filmographic Terms B.11.12
    SongComposer = "SongComposer"


class ProducingActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.2
    """
    # FIAF Glossary of Filmographic Terms B.2.19
    Advisor = "Advisor"
    # FIAF Glossary of Filmographic Terms B.2.8
    AssistantProducer = "AssistantProducer"
    # FIAF Glossary of Filmographic Terms B.2.6
    AssociateProducer = "AssociateProducer"
    # FIAF Glossary of Filmographic Terms B.2.22
    Cooperation = "Cooperation"
    # FIAF Glossary of Filmographic Terms B.2.5
    Coproducer = "Coproducer"
    # FIAF Glossary of Filmographic Terms B.2.4
    ExecutiveProducer = "ExecutiveProducer"
    # FIAF Glossary of Filmographic Terms B.2.7
    LineProducer = "LineProducer"
    # FIAF Glossary of Filmographic Terms B.2.12
    LocationManager = "LocationManager"
    # FIAF Glossary of Filmographic Terms B.2.15
    PostProductionSupervisor = "PostProductionSupervisor"
    # FIAF Glossary of Filmographic Terms B.2.21
    Presenter = "Presenter"
    # FIAF Glossary of Filmographic Terms B.2.3
    Producer = "Producer"
    # FIAF Glossary of Filmographic Terms B.2.11
    ProductionAccountant = "ProductionAccountant"
    # FIAF Glossary of Filmographic Terms B.2.14
    ProductionAssistant = "ProductionAssistant"
    # FIAF Glossary of Filmographic Terms B.2.1
    ProductionCompany = "ProductionCompany"
    # FIAF Glossary of Filmographic Terms B.2.10
    ProductionCoordinator = "ProductionCoordinator"
    # FIAF Glossary of Filmographic Terms B.2.9
    ProductionManager = "ProductionManager"
    # FIAF Glossary of Filmographic Terms B.2.16
    Publicist = "Publicist"
    # FIAF Glossary of Filmographic Terms B.2.17
    SeriesProducer = "SeriesProducer"
    # FIAF Glossary of Filmographic Terms B.2.20
    Sponsor = "Sponsor"
    # FIAF Glossary of Filmographic Terms B.2.23
    Studio = "Studio"
    # FIAF Glossary of Filmographic Terms B.2.13
    TransportationManager = "TransportationManager"


class ProductionDesignActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.6
    """
    # FIAF Glossary of Filmographic Terms B.6.2
    ArtDirector = "ArtDirector"
    # FIAF Glossary of Filmographic Terms B.6.3
    AssistantArtDirector = "AssistantArtDirector"
    # FIAF Glossary of Filmographic Terms B.6.8
    ConstructionCoordinator = "ConstructionCoordinator"
    # FIAF Glossary of Filmographic Terms B.6.12
    CostumeDesigner = "CostumeDesigner"
    # FIAF Glossary of Filmographic Terms B.6.17
    CostumeMaker = "CostumeMaker"
    # FIAF Glossary of Filmographic Terms B.6.13
    CostumeSupervisor = "CostumeSupervisor"
    # FIAF Glossary of Filmographic Terms B.6.18
    CostumeSupplier = "CostumeSupplier"
    # FIAF Glossary of Filmographic Terms B.6.14
    Costumer = "Costumer"
    # FIAF Glossary of Filmographic Terms B.6.16
    Gowns = "Gowns"
    # FIAF Glossary of Filmographic Terms B.6.11
    Greensperson = "Greensperson"
    # FIAF Glossary of Filmographic Terms B.6.20
    HairStylist = "HairStylist"
    # FIAF Glossary of Filmographic Terms B.6.9
    LeadPerson = "LeadPerson"
    # FIAF Glossary of Filmographic Terms B.6.19
    MakeUpArtist = "MakeUpArtist"
    # FIAF Glossary of Filmographic Terms B.6.1
    ProductionDesigner = "ProductionDesigner"
    # FIAF Glossary of Filmographic Terms B.6.7
    PropertyMaster = "PropertyMaster"
    # FIAF Glossary of Filmographic Terms B.6.10
    ScenicArtist = "ScenicArtist"
    # FIAF Glossary of Filmographic Terms B.6.6
    SetDecorator = "SetDecorator"
    # FIAF Glossary of Filmographic Terms B.6.5
    SetDesigner = "SetDesigner"
    # FIAF Glossary of Filmographic Terms B.6.4
    StoryboardArtist = "StoryboardArtist"
    # FIAF Glossary of Filmographic Terms B.6.21
    TitleDesigner = "TitleDesigner"
    # FIAF Glossary of Filmographic Terms B.6.15
    WardrobeSupervisor = "WardrobeSupervisor"


class PuppetActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.14
    """
    # FIAF Glossary of Filmographic Terms B.14.7
    Puppeteer = "Puppeteer"


class SoundActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.9
    """
    # FIAF Glossary of Filmographic Terms B.9.4
    BoomOperator = "BoomOperator"
    # FIAF Glossary of Filmographic Terms B.9.8
    DialogueEditor = "DialogueEditor"
    # FIAF Glossary of Filmographic Terms B.9.13
    DubbingDirector = "DubbingDirector"
    # FIAF Glossary of Filmographic Terms B.9.14
    DubbingEditor = "DubbingEditor"
    # FIAF Glossary of Filmographic Terms B.9.11
    DubbingMixer = "DubbingMixer"
    # FIAF Glossary of Filmographic Terms B.9.15
    DubbingSpeaker = "DubbingSpeaker"
    # FIAF Glossary of Filmographic Terms B.9.9
    FoleyArtist = "FoleyArtist"
    # FIAF Glossary of Filmographic Terms B.9.1
    SoundDesigner = "SoundDesigner"
    # FIAF Glossary of Filmographic Terms B.9.7
    SoundEditor = "SoundEditor"
    # FIAF Glossary of Filmographic Terms B.9.5
    SoundEngineer = "SoundEngineer"
    # FIAF Glossary of Filmographic Terms B.9.3
    SoundRecorderMixer = "SoundRecorderMixer"
    # FIAF Glossary of Filmographic Terms B.9.2
    SoundSupervisor = "SoundSupervisor"
    # FIAF Glossary of Filmographic Terms B.9.6
    SupervisingSoundEditor = "SupervisingSoundEditor"


class SpecialEffectsActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.8
    """
    # FIAF Glossary of Filmographic Terms B.8.4
    Animatronics = "Animatronics"
    # FIAF Glossary of Filmographic Terms B.8.7
    Armorer = "Armorer"
    # FIAF Glossary of Filmographic Terms B.8.12
    CGIArtist = "CGIArtist"
    # FIAF Glossary of Filmographic Terms B.8.10
    Compositor = "Compositor"
    # FIAF Glossary of Filmographic Terms B.8.8
    MatteArtist = "MatteArtist"
    # FIAF Glossary of Filmographic Terms B.8.3
    MechanicalEffects = "MechanicalEffects"
    # FIAF Glossary of Filmographic Terms B.8.13
    MotionCapture = "MotionCapture"
    # FIAF Glossary of Filmographic Terms B.8.5
    Prosthetics = "Prosthetics"
    # FIAF Glossary of Filmographic Terms B.8.6
    Pyrotechnics = "Pyrotechnics"
    # FIAF Glossary of Filmographic Terms B.8.9
    RotoscopeArtist = "RotoscopeArtist"
    # FIAF Glossary of Filmographic Terms B.8.1
    SpecialEffects = "SpecialEffects"
    # FIAF Glossary of Filmographic Terms B.8.2
    VisualEffects = "VisualEffects"


class WritingActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.4
    """
    # FIAF Glossary of Filmographic Terms B.4.11
    Adaptation = "Adaptation"
    # FIAF Glossary of Filmographic Terms B.4.5
    BasedonCharactersCreatedby = "BasedonCharactersCreatedby"
    # FIAF Glossary of Filmographic Terms B.4.6
    Idea = "Idea"
    # FIAF Glossary of Filmographic Terms B.4.15
    NarrationWriter = "NarrationWriter"
    # FIAF Glossary of Filmographic Terms B.4.16
    Research = "Research"
    # FIAF Glossary of Filmographic Terms B.4.3
    ScreenStory = "ScreenStory"
    # FIAF Glossary of Filmographic Terms B.4.7
    SeriesCreatedby = "SeriesCreatedby"
    # FIAF Glossary of Filmographic Terms B.4.4
    SourceMaterial = "SourceMaterial"
    # FIAF Glossary of Filmographic Terms B.4.8
    Stagedby = "Stagedby"
    # FIAF Glossary of Filmographic Terms B.4.2
    Writer = "Writer"


class ManifestationActivityTypeEnum(str, Enum):
    """
    Activity types / roles. See also: FIAF Moving Image Cataloguing Manual 2.4.1.1, D.8
    """
    # FIAF Moving Image Cataloguing Manual D.8.11
    AgentNotIdentified = "AgentNotIdentified"
    # FIAF Moving Image Cataloguing Manual D.8.6
    AgentResponsibleForPreservation = "AgentResponsibleForPreservation"
    # FIAF Moving Image Cataloguing Manual D.8.7
    AgentResponsibleForReproductionOrTransfer = "AgentResponsibleForReproductionOrTransfer"
    # FIAF Moving Image Cataloguing Manual D.8.8
    AgentResponsibleForTheArchivalAvailability = "AgentResponsibleForTheArchivalAvailability"
    # FIAF Moving Image Cataloguing Manual D.8.9
    AgentResponsibleForTheMereAvailability = "AgentResponsibleForTheMereAvailability"
    # FIAF Moving Image Cataloguing Manual D.8.10
    AgentUnclearOrUndetermined = "AgentUnclearOrUndetermined"
    # FIAF Moving Image Cataloguing Manual D.8.3
    Broadcaster = "Broadcaster"
    # FIAF Moving Image Cataloguing Manual D.8.2
    DistributorNonTheatrical = "DistributorNonTheatrical"
    # FIAF Moving Image Cataloguing Manual D.8.1
    DistributorTheatrical = "DistributorTheatrical"
    # FIAF Moving Image Cataloguing Manual D.8.5
    Manufacturer = "Manufacturer"
    # FIAF Moving Image Cataloguing Manual D.8.4
    Publisher = "Publisher"
    # FIAF Moving Image Cataloguing Manual 1.4.1.1, 2.4.1.1, 3.3.1.1
    UnknownActivity = "UnknownActivity"


class AgentTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual 1.4.1
    """
    CorporateBody = "CorporateBody"
    Family = "Family"
    Person = "Person"
    PersonGroup = "PersonGroup"


class ColourTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual 2.3.4.4, 3.1.5.6, D.7.11
    """
    # FIAF Moving Image Cataloguing Manual D.7.11
    BlackAndWhite = "BlackAndWhite"
    # FIAF Moving Image Cataloguing Manual D.7.11
    BlackAndWhiteTinted = "BlackAndWhiteTinted"
    # FIAF Moving Image Cataloguing Manual D.7.11
    BlackAndWhiteTintedAndToned = "BlackAndWhiteTintedAndToned"
    # FIAF Moving Image Cataloguing Manual D.7.11
    BlackAndWhiteToned = "BlackAndWhiteToned"
    # FIAF Moving Image Cataloguing Manual D.7.11
    Colour = "Colour"
    # FIAF Moving Image Cataloguing Manual D.7.11
    ColourBlackAndWhite = "ColourBlackAndWhite"
    # FIAF Moving Image Cataloguing Manual D.7.11
    Sepia = "Sepia"
    # FIAF Moving Image Cataloguing Manual D.7.11
    Tinted = "Tinted"


class ManufactureEventTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.4.7, D.14
    """
    # FIAF Moving Image Cataloguing Manual D.14
    FilmPrintingEvent = "FilmPrintingEvent"
    # FIAF Moving Image Cataloguing Manual D.14
    MasteringEvent = "MasteringEvent"
    # FIAF Moving Image Cataloguing Manual D.14
    ScanningEvent = "ScanningEvent"
    # FIAF Moving Image Cataloguing Manual D.14
    TelecineEvent = "TelecineEvent"
    # FIAF Moving Image Cataloguing Manual D.14
    UploadingEvent = "UploadingEvent"
    # FIAF Moving Image Cataloguing Manual D.14
    VideoCopyingEvent = "VideoCopyingEvent"


class PreservationEventTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.4.5
    """
    # FIAF Moving Image Cataloguing Manual D.12
    DigitisationEvent = "DigitisationEvent"
    # FIAF Moving Image Cataloguing Manual D.12
    DuplicationEvent = "DuplicationEvent"
    # FIAF Moving Image Cataloguing Manual D.12
    ReproductionEvent = "ReproductionEvent"
    # FIAF Moving Image Cataloguing Manual D.4.5
    RestorationEvent = "RestorationEvent"
    # FIAF Moving Image Cataloguing Manual D.12
    TransferEvent = "TransferEvent"


class ProductionEventTypeEnum(str, Enum):
    """
    Leave unset for main production event, otherwise see FIAF Moving Image Cataloguing Manual D.4.3, D.11
    """
    # FIAF Moving Image Cataloguing Manual D.11
    CastingEvent = "CastingEvent"
    # FIAF Moving Image Cataloguing Manual D.11
    IndoorShootingEvent = "IndoorShootingEvent"
    # FIAF Moving Image Cataloguing Manual D.11
    OutdoorShootingEvent = "OutdoorShootingEvent"
    # FIAF Moving Image Cataloguing Manual D.11
    PostProductionEvent = "PostProductionEvent"


class PublicationEventTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.4.1, D.10
    """
    # FIAF Moving Image Cataloguing Manual D.10
    BroadcastEvent = "BroadcastEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    DistributionEvent = "DistributionEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    HomeVideoPublicationEvent = "HomeVideoPublicationEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    NonTheatricalDistributionEvent = "NonTheatricalDistributionEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    NotForReleaseEvent = "NotForReleaseEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    OnlineTransmissionEvent = "OnlineTransmissionEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    PreReleaseEvent = "PreReleaseEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    ReleaseEvent = "ReleaseEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    TheatricalDistributionEvent = "TheatricalDistributionEvent"
    # FIAF Moving Image Cataloguing Manual D.10
    UnknownEvent = "UnknownEvent"


class FormatAudioTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_16mmMagneticTrack = "16mmMagneticTrack"
    number_17FULL_STOP5mmMagneticTrack = "17.5mmMagneticTrack"
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_35mmMagneticTrack = "35mmMagneticTrack"
    # FIAF Moving Image Cataloguing Manual D.7.2
    Audiocassette = "Audiocassette"
    # FIAF Moving Image Cataloguing Manual D.7.2
    HalfInchAudioReel = "HalfInchAudioReel"
    # FIAF Moving Image Cataloguing Manual D.7.2
    OneInchAudioReel = "OneInchAudioReel"
    # FIAF Moving Image Cataloguing Manual D.7.2
    QuarterInchAudioReel = "QuarterInchAudioReel"
    # FIAF Moving Image Cataloguing Manual D.7.2
    TwoInchAudioReel = "TwoInchAudioReel"


class FormatDigitalFileEncodingTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    # FIAF Moving Image Cataloguing Manual D.7.2
    MPEG4 = "MPEG4"
    # FIAF Moving Image Cataloguing Manual D.7.2
    Quicktime = "Quicktime"
    # FIAF Moving Image Cataloguing Manual D.7.2
    RealVideo = "RealVideo"
    # FIAF Moving Image Cataloguing Manual D.7.2
    SVCD = "SVCD"
    # FIAF Moving Image Cataloguing Manual D.7.2
    VCD = "VCD"
    # FIAF Moving Image Cataloguing Manual D.7.2
    WindowsMedia = "WindowsMedia"


class FormatDigitalFileTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    # FIAF Moving Image Cataloguing Manual D.7.2
    AVI = "AVI"
    # FIAF Moving Image Cataloguing Manual D.7.2
    DPX = "DPX"
    DV = "DV"
    # FIAF Moving Image Cataloguing Manual D.7.2
    MOV = "MOV"
    # FIAF Moving Image Cataloguing Manual D.7.2
    MP4 = "MP4"
    # FIAF Moving Image Cataloguing Manual D.7.2
    MXF = "MXF"
    # Video Object File (MPEG-2 subset)
    VOB = "VOB"
    WebM = "WebM"


class FormatFilmTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_16mmFilm = "16mmFilm"
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_17FULL_STOP5mmFilm = "17.5mmFilm"
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_35mmFilm = "35mmFilm"
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_70mmFilm = "70mmFilm"
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_8mmFilm = "8mmFilm"
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_9FULL_STOP5mmFilm = "9.5mmFilm"
    # FIAF Moving Image Cataloguing Manual D.7.2
    Super16mmFilm = "Super16mmFilm"
    # FIAF Moving Image Cataloguing Manual D.7.2
    Super8mmFilm = "Super8mmFilm"


class FormatOpticalTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    # FIAF Moving Image Cataloguing Manual D.7.2
    BluRay = "BluRay"
    # FIAF Moving Image Cataloguing Manual D.7.2
    CD = "CD"
    # FIAF Moving Image Cataloguing Manual D.7.2
    DVD = "DVD"
    # FIAF Moving Image Cataloguing Manual D.7.2
    LaserDisc = "LaserDisc"


class FormatVideoTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_1InchCFormat = "1InchCFormat"
    # FIAF Moving Image Cataloguing Manual D.7.2
    number_2InchQuadruplex = "2InchQuadruplex"
    # FIAF Moving Image Cataloguing Manual D.7.2
    BetacamSP = "BetacamSP"
    # FIAF Moving Image Cataloguing Manual D.7.2
    D1 = "D1"
    # FIAF Moving Image Cataloguing Manual D.7.2
    D5 = "D5"
    Digital8 = "Digital8"
    # FIAF Moving Image Cataloguing Manual D.7.2
    DigitalBetacam = "DigitalBetacam"
    DV = "DV"
    DVCAM = "DVCAM"
    DVCPro = "DVCPro"
    DVCPro50 = "DVCPro50"
    # FIAF Moving Image Cataloguing Manual D.7.2
    DVCPROHD = "DVCPROHD"
    HDCAM = "HDCAM"
    # FIAF Moving Image Cataloguing Manual D.7.2
    HDCAMSR = "HDCAMSR"
    HDV = "HDV"
    MiniDV = "MiniDV"
    SVHS = "SVHS"
    UMatic = "UMatic"
    IMX = "IMX"
    VHS = "VHS"


class FrameRateEnum(str, Enum):
    """
    Frames per second of an item.
    """
    # FIAF Moving Image Cataloguing Manual D.7.18
    number_16fps = "16fps"
    # FIAF Moving Image Cataloguing Manual D.7.18
    number_23FULL_STOP98fps = "23.98fps"
    # FIAF Moving Image Cataloguing Manual D.7.18
    number_24fps = "24fps"
    # FIAF Moving Image Cataloguing Manual D.7.18
    number_25fps = "25fps"
    # FIAF Moving Image Cataloguing Manual D.7.18
    number_30fps = "30fps"
    # FIAF Moving Image Cataloguing Manual D.7.18
    number_48fps = "48fps"
    # FIAF Moving Image Cataloguing Manual D.7.18
    VariableFrameRate = "VariableFrameRate"


class ItemAccessStatusEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.3
    """
    Archive = "Archive"
    Distribution = "Distribution"
    # FIAF Moving Image Cataloguing Manual D.7.3
    Master = "Master"
    # FIAF Moving Image Cataloguing Manual D.7.3
    Removed = "Removed"
    # FIAF Moving Image Cataloguing Manual D.7.3
    Viewing = "Viewing"


class ItemElementTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.7.8
    """
    # FIAF Moving Image Cataloguing Manual D.7.8
    ColourNegative = "ColourNegative"
    # FIAF Moving Image Cataloguing Manual D.7.8
    ColourPositive = "ColourPositive"
    # FIAF Moving Image Cataloguing Manual D.7.8
    CopperTonedPositive = "CopperTonedPositive"
    # FIAF Moving Image Cataloguing Manual D.7.8
    CyanMatrix = "CyanMatrix"
    DCDM = "DCDM"
    # FIAF Moving Image Cataloguing Manual D.7.8
    DCP = "DCP"
    # FIAF Moving Image Cataloguing Manual D.7.8
    DirectBWPositive = "DirectBWPositive"
    # FIAF Moving Image Cataloguing Manual D.7.8
    DuplicateNegative = "DuplicateNegative"
    # FIAF Moving Image Cataloguing Manual D.7.8
    DuplicatePositive = "DuplicatePositive"
    EditDecisionList = "EditDecisionList"
    # FIAF Moving Image Cataloguing Manual D.7.8
    ImageNegative = "ImageNegative"
    # FIAF Moving Image Cataloguing Manual D.7.8
    Lavender = "Lavender"
    # FIAF Moving Image Cataloguing Manual D.7.8
    OriginalNegative = "OriginalNegative"
    # FIAF Moving Image Cataloguing Manual D.7.8
    OriginalPositiveReversalFilm = "OriginalPositiveReversalFilm"
    # FIAF Moving Image Cataloguing Manual D.7.8
    Positive = "Positive"
    # FIAF Moving Image Cataloguing Manual D.7.8
    SoundNegative = "SoundNegative"
    Subtitles = "Subtitles"


class LanguageCodeEnum(str, Enum):
    """
    [ISO 639-2 code](https://id.loc.gov/vocabulary/iso639-2.html) for the Representation of Names of Languages (Part 2: Alpha-3)
    """
    aar = "aar"
    abk = "abk"
    ace = "ace"
    ach = "ach"
    ada = "ada"
    ady = "ady"
    afa = "afa"
    afh = "afh"
    afr = "afr"
    ain = "ain"
    aka = "aka"
    akk = "akk"
    alb = "alb"
    ale = "ale"
    alg = "alg"
    alt = "alt"
    amh = "amh"
    ang = "ang"
    anp = "anp"
    apa = "apa"
    ara = "ara"
    arc = "arc"
    arg = "arg"
    arm = "arm"
    arn = "arn"
    arp = "arp"
    art = "art"
    arw = "arw"
    asm = "asm"
    ast = "ast"
    ath = "ath"
    aus = "aus"
    ava = "ava"
    ave = "ave"
    awa = "awa"
    aym = "aym"
    aze = "aze"
    bad = "bad"
    bai = "bai"
    bak = "bak"
    bal = "bal"
    bam = "bam"
    ban = "ban"
    baq = "baq"
    bas = "bas"
    bat = "bat"
    bej = "bej"
    bel = "bel"
    bem = "bem"
    ben = "ben"
    ber = "ber"
    bho = "bho"
    bih = "bih"
    bik = "bik"
    bin = "bin"
    bis = "bis"
    bla = "bla"
    bnt = "bnt"
    bod = "bod"
    bos = "bos"
    bra = "bra"
    bre = "bre"
    btk = "btk"
    bua = "bua"
    bug = "bug"
    bul = "bul"
    bur = "bur"
    byn = "byn"
    cad = "cad"
    cai = "cai"
    car = "car"
    cat = "cat"
    cau = "cau"
    ceb = "ceb"
    cel = "cel"
    ces = "ces"
    cha = "cha"
    chb = "chb"
    che = "che"
    chg = "chg"
    chi = "chi"
    chk = "chk"
    chm = "chm"
    chn = "chn"
    cho = "cho"
    chp = "chp"
    chr = "chr"
    chu = "chu"
    chv = "chv"
    chy = "chy"
    cmc = "cmc"
    cnr = "cnr"
    cop = "cop"
    cor = "cor"
    cos = "cos"
    cpe = "cpe"
    cpf = "cpf"
    cpp = "cpp"
    cre = "cre"
    crh = "crh"
    crp = "crp"
    csb = "csb"
    cus = "cus"
    cym = "cym"
    cze = "cze"
    dak = "dak"
    dan = "dan"
    dar = "dar"
    day = "day"
    del_ = "del"
    den = "den"
    deu = "deu"
    dgr = "dgr"
    din = "din"
    div = "div"
    doi = "doi"
    dra = "dra"
    dsb = "dsb"
    dua = "dua"
    dum = "dum"
    dut = "dut"
    dyu = "dyu"
    dzo = "dzo"
    efi = "efi"
    egy = "egy"
    eka = "eka"
    ell = "ell"
    elx = "elx"
    eng = "eng"
    enm = "enm"
    epo = "epo"
    est = "est"
    eus = "eus"
    ewe = "ewe"
    ewo = "ewo"
    fan = "fan"
    fao = "fao"
    fas = "fas"
    fat = "fat"
    fij = "fij"
    fil = "fil"
    fin = "fin"
    fiu = "fiu"
    fon = "fon"
    fra = "fra"
    fre = "fre"
    frm = "frm"
    fro = "fro"
    frr = "frr"
    frs = "frs"
    fry = "fry"
    ful = "ful"
    fur = "fur"
    gaa = "gaa"
    gay = "gay"
    gba = "gba"
    gem = "gem"
    geo = "geo"
    ger = "ger"
    gez = "gez"
    gil = "gil"
    gla = "gla"
    gle = "gle"
    glg = "glg"
    glv = "glv"
    gmh = "gmh"
    goh = "goh"
    gon = "gon"
    gor = "gor"
    got = "got"
    grb = "grb"
    grc = "grc"
    gre = "gre"
    grn = "grn"
    gsw = "gsw"
    guj = "guj"
    gwi = "gwi"
    hai = "hai"
    hat = "hat"
    hau = "hau"
    haw = "haw"
    heb = "heb"
    her = "her"
    hil = "hil"
    him = "him"
    hin = "hin"
    hit = "hit"
    hmn = "hmn"
    hmo = "hmo"
    hrv = "hrv"
    hsb = "hsb"
    hun = "hun"
    hup = "hup"
    hye = "hye"
    iba = "iba"
    ibo = "ibo"
    ice = "ice"
    ido = "ido"
    iii = "iii"
    ijo = "ijo"
    iku = "iku"
    ile = "ile"
    ilo = "ilo"
    ina = "ina"
    inc = "inc"
    ind = "ind"
    ine = "ine"
    inh = "inh"
    ipk = "ipk"
    ira = "ira"
    iro = "iro"
    isl = "isl"
    ita = "ita"
    jav = "jav"
    jbo = "jbo"
    jpn = "jpn"
    jpr = "jpr"
    jrb = "jrb"
    kaa = "kaa"
    kab = "kab"
    kac = "kac"
    kal = "kal"
    kam = "kam"
    kan = "kan"
    kar = "kar"
    kas = "kas"
    kat = "kat"
    kau = "kau"
    kaw = "kaw"
    kaz = "kaz"
    kbd = "kbd"
    kha = "kha"
    khi = "khi"
    khm = "khm"
    kho = "kho"
    kik = "kik"
    kin = "kin"
    kir = "kir"
    kmb = "kmb"
    kok = "kok"
    kom = "kom"
    kon = "kon"
    kor = "kor"
    kos = "kos"
    kpe = "kpe"
    krc = "krc"
    krl = "krl"
    kro = "kro"
    kru = "kru"
    kua = "kua"
    kum = "kum"
    kur = "kur"
    kut = "kut"
    lad = "lad"
    lah = "lah"
    lam = "lam"
    lao = "lao"
    lat = "lat"
    lav = "lav"
    lez = "lez"
    lim = "lim"
    lin = "lin"
    lit = "lit"
    lol = "lol"
    loz = "loz"
    ltz = "ltz"
    lua = "lua"
    lub = "lub"
    lug = "lug"
    lui = "lui"
    lun = "lun"
    luo = "luo"
    lus = "lus"
    mac = "mac"
    mad = "mad"
    mag = "mag"
    mah = "mah"
    mai = "mai"
    mak = "mak"
    mal = "mal"
    man = "man"
    mao = "mao"
    map = "map"
    mar = "mar"
    mas = "mas"
    may = "may"
    mdf = "mdf"
    mdr = "mdr"
    men = "men"
    mga = "mga"
    mic = "mic"
    min = "min"
    mis = "mis"
    mkd = "mkd"
    mkh = "mkh"
    mlg = "mlg"
    mlt = "mlt"
    mnc = "mnc"
    mni = "mni"
    mno = "mno"
    moh = "moh"
    mon = "mon"
    mos = "mos"
    mri = "mri"
    msa = "msa"
    mul = "mul"
    mun = "mun"
    mus = "mus"
    mwl = "mwl"
    mwr = "mwr"
    mya = "mya"
    myn = "myn"
    myv = "myv"
    nah = "nah"
    nai = "nai"
    nap = "nap"
    nau = "nau"
    nav = "nav"
    nbl = "nbl"
    nde = "nde"
    ndo = "ndo"
    nds = "nds"
    nep = "nep"
    new = "new"
    nia = "nia"
    nic = "nic"
    niu = "niu"
    nld = "nld"
    nno = "nno"
    nob = "nob"
    nog = "nog"
    non = "non"
    nor = "nor"
    nqo = "nqo"
    nso = "nso"
    nub = "nub"
    nwc = "nwc"
    nya = "nya"
    nym = "nym"
    nyn = "nyn"
    nyo = "nyo"
    nzi = "nzi"
    oci = "oci"
    oji = "oji"
    ori = "ori"
    orm = "orm"
    osa = "osa"
    oss = "oss"
    ota = "ota"
    oto = "oto"
    paa = "paa"
    pag = "pag"
    pal = "pal"
    pam = "pam"
    pan = "pan"
    pap = "pap"
    pau = "pau"
    peo = "peo"
    per = "per"
    phi = "phi"
    phn = "phn"
    pli = "pli"
    pol = "pol"
    pon = "pon"
    por = "por"
    pra = "pra"
    pro = "pro"
    pus = "pus"
    que = "que"
    raj = "raj"
    rap = "rap"
    rar = "rar"
    roa = "roa"
    roh = "roh"
    rom = "rom"
    ron = "ron"
    rum = "rum"
    run = "run"
    rup = "rup"
    rus = "rus"
    sad = "sad"
    sag = "sag"
    sah = "sah"
    sai = "sai"
    sal = "sal"
    sam = "sam"
    san = "san"
    sas = "sas"
    sat = "sat"
    scn = "scn"
    sco = "sco"
    sel = "sel"
    sem = "sem"
    sga = "sga"
    sgn = "sgn"
    shn = "shn"
    sid = "sid"
    sin = "sin"
    sio = "sio"
    sit = "sit"
    sla = "sla"
    slk = "slk"
    slo = "slo"
    slv = "slv"
    sma = "sma"
    sme = "sme"
    smi = "smi"
    smj = "smj"
    smn = "smn"
    smo = "smo"
    sms = "sms"
    sna = "sna"
    snd = "snd"
    snk = "snk"
    sog = "sog"
    som = "som"
    son = "son"
    sot = "sot"
    spa = "spa"
    sqi = "sqi"
    srd = "srd"
    srn = "srn"
    srp = "srp"
    srr = "srr"
    ssa = "ssa"
    ssw = "ssw"
    suk = "suk"
    sun = "sun"
    sus = "sus"
    sux = "sux"
    swa = "swa"
    swe = "swe"
    syc = "syc"
    syr = "syr"
    tah = "tah"
    tai = "tai"
    tam = "tam"
    tat = "tat"
    tel = "tel"
    tem = "tem"
    ter = "ter"
    tet = "tet"
    tgk = "tgk"
    tgl = "tgl"
    tha = "tha"
    tib = "tib"
    tig = "tig"
    tir = "tir"
    tiv = "tiv"
    tkl = "tkl"
    tlh = "tlh"
    tli = "tli"
    tmh = "tmh"
    tog = "tog"
    ton = "ton"
    tpi = "tpi"
    tsi = "tsi"
    tsn = "tsn"
    tso = "tso"
    tuk = "tuk"
    tum = "tum"
    tup = "tup"
    tur = "tur"
    tut = "tut"
    tvl = "tvl"
    twi = "twi"
    tyv = "tyv"
    udm = "udm"
    uga = "uga"
    uig = "uig"
    ukr = "ukr"
    umb = "umb"
    und = "und"
    urd = "urd"
    uzb = "uzb"
    vai = "vai"
    ven = "ven"
    vie = "vie"
    vol = "vol"
    vot = "vot"
    wak = "wak"
    wal = "wal"
    war = "war"
    was = "was"
    wel = "wel"
    wen = "wen"
    wln = "wln"
    wol = "wol"
    xal = "xal"
    xho = "xho"
    yao = "yao"
    yap = "yap"
    yid = "yid"
    yor = "yor"
    ypk = "ypk"
    zap = "zap"
    zbl = "zbl"
    zen = "zen"
    zgh = "zgh"
    zha = "zha"
    zho = "zho"
    znd = "znd"
    zul = "zul"
    zun = "zun"
    zxx = "zxx"
    zza = "zza"


class LanguageUsageEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual 2.3.3, D.6
    """
    # Audio description for the visually impaired
    AudioDescription = "AudioDescription"
    # FIAF Moving Image Cataloguing Manual D.6
    Captions = "Captions"
    ClosingCredits = "ClosingCredits"
    # FIAF Moving Image Cataloguing Manual 2.3.3
    Dubbed = "Dubbed"
    # FIAF Moving Image Cataloguing Manual D.6
    Intertitles = "Intertitles"
    # FIAF Moving Image Cataloguing Manual D.6
    NoDialogue = "NoDialogue"
    OpeningCredits = "OpeningCredits"
    # Subtitles for the Deaf and Hard of hearing
    SDHSubtitles = "SDHSubtitles"
    # FIAF Moving Image Cataloguing Manual D.6
    SignedLanguage = "SignedLanguage"
    # FIAF Moving Image Cataloguing Manual D.6
    SpokenLanguage = "SpokenLanguage"
    # FIAF Moving Image Cataloguing Manual D.6
    Subtitles = "Subtitles"
    # FIAF Moving Image Cataloguing Manual D.6
    SungLanguage = "SungLanguage"
    VoiceOver = "VoiceOver"


class PrecisionEnum(str, Enum):
    """
    Qualifier indicating the precision of an extent value or duration
    """
    # Value may be inaccurate but is regarded to be close to the real thing
    Approximate = "Approximate"
    # Sources for the given value are deemed unreliable, so it may as well be off the mark
    Uncertain = "Uncertain"


class SoundTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual 2.3.4.3, 3.1.5.3, D.7.4
    """
    # FIAF Moving Image Cataloguing Manual D.7.4
    Combined = "Combined"
    # FIAF Moving Image Cataloguing Manual D.7.4
    CombinedAsMute = "CombinedAsMute"
    # FIAF Moving Image Cataloguing Manual D.7.4
    CombinedAsSound = "CombinedAsSound"
    # FIAF Moving Image Cataloguing Manual D.7.4
    MixedSound = "MixedSound"
    # FIAF Moving Image Cataloguing Manual D.7.4
    Mute = "Mute"
    # FIAF Moving Image Cataloguing Manual D.7.4
    Silent = "Silent"
    # FIAF Moving Image Cataloguing Manual D.7.4
    Sound = "Sound"
    # FIAF Moving Image Cataloguing Manual D.7.4
    Temporary = "Temporary"


class TitleTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual A.2
    """
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    AbbreviatedTitle = "AbbreviatedTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    AcquisitionTitle = "AcquisitionTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4
    AlternativeTitle = "AlternativeTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    CorrectedTitle = "CorrectedTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    PreReleaseTitle = "PreReleaseTitle"
    # FIAF Moving Image Cataloguing Manual A.2.0
    PreferredTitle = "PreferredTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    SearchTitle = "SearchTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    SeriesTitle = "SeriesTitle"
    # FIAF Moving Image Cataloguing Manual A.2.5
    SuppliedDevisedTitle = "SuppliedDevisedTitle"
    # FIAF Moving Image Cataloguing Manual A.2.2
    TitleProper = "TitleProper"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    TranslatedTitle = "TranslatedTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    TransliteratedTitle = "TransliteratedTitle"
    # FIAF Moving Image Cataloguing Manual A.2.4.1
    WorkingTitle = "WorkingTitle"


class UnitEnum(str, Enum):
    """
    Units of measurement. Definitions are taken from the Quantities, Units, Dimensions and Data Types Ontologies (QUDT)
    """
    # Unit of length defined as being 0.3048 metres
    Feet = "Feet"
    # Unit for digital information equivalent to 1000 megabytes
    GigaByte = "GigaByte"
    # Unit for digital information equivalent to 1000 bytes
    KiloByte = "KiloByte"
    # Metric and SI base unit of distance
    Metre = "Metre"
    # Unit for digital information equivalent to 1000 kilobytes
    MegaByte = "MegaByte"
    # Unit for digital information equivalent to 1000 gigabytes
    TeraByte = "TeraByte"


class VariantTypeEnum(str, Enum):
    """
    FIAF Moving Image Cataloguing Manual D.2
    """
    # FIAF Moving Image Cataloguing Manual D.2
    AbridgedCondensed = "AbridgedCondensed"
    # FIAF Moving Image Cataloguing Manual D.2
    Augmented = "Augmented"
    # FIAF Moving Image Cataloguing Manual D.2
    BlackAndWhiteCopyOfWorkOriginallyIssuedInColour = "BlackAndWhiteCopyOfWorkOriginallyIssuedInColour"
    # FIAF Moving Image Cataloguing Manual D.2
    Censored = "Censored"
    # FIAF Moving Image Cataloguing Manual D.2
    Colourized = "Colourized"
    # FIAF Moving Image Cataloguing Manual D.2
    DifferentSoundTrack = "DifferentSoundTrack"
    # FIAF Moving Image Cataloguing Manual D.2
    Dubbed = "Dubbed"
    # FIAF Moving Image Cataloguing Manual D.2
    PreservationRestoration = "PreservationRestoration"
    # FIAF Moving Image Cataloguing Manual D.2
    Sonorized = "Sonorized"
    # FIAF Moving Image Cataloguing Manual D.2
    Subtitled = "Subtitled"


class WorkVariantTypeEnum(str, Enum):
    """
    Work/Variant description type. See also: FIAF Moving Image Cataloguing Manual 1.2.1, D.1
    """
    # Content that is contained in another content
    Analytic = "Analytic"
    # Content issued in several independent parts; an ‘umbrella’ work title covering a number of different Works/Variants/Manifestations
    Collection = "Collection"
    # Complete content in one part or intended to be completed in a finite number of parts
    Monographic = "Monographic"
    # Content issued in successive parts and intended to be continued indefinitely, or across a span of time. A Work record for a television series is catalogued as a “Serial”, individual episodes may be catalogued as a Monographic record
    Serial = "Serial"


class WorkFormEnum(str, Enum):
    """
    FIAF Glossary of Filmographic Terms D.1
    """
    # FIAF Glossary of Filmographic Terms D.1.9
    AmateurFilm = "AmateurFilm"
    # FIAF Glossary of Filmographic Terms D.1.6
    Compilation = "Compilation"
    # FIAF Glossary of Filmographic Terms D.1.13
    Excerpt = "Excerpt"
    # FIAF Glossary of Filmographic Terms D.1.2
    Feature = "Feature"
    # FIAF Glossary of Filmographic Terms D.1.8
    Featurette = "Featurette"
    # FIAF Glossary of Filmographic Terms D.1.10
    HomeMovie = "HomeMovie"
    # FIAF Glossary of Filmographic Terms D.1.11
    Outtake = "Outtake"
    # FIAF Glossary of Filmographic Terms D.1.15
    ScreenTest = "ScreenTest"
    # FIAF Glossary of Filmographic Terms D.1.4
    Series = "Series"
    # FIAF Glossary of Filmographic Terms D.1.3
    Short = "Short"
    # FIAF Glossary of Filmographic Terms D.1.12
    StockFootage = "StockFootage"
    # FIAF Glossary of Filmographic Terms D.1.7
    Trailer = "Trailer"
    # FIAF Glossary of Filmographic Terms D.1.14
    UneditedFootage = "UneditedFootage"
    # FIAF Moving Image Cataloguing Manual E.2.2
    AnthologyFilm = "AnthologyFilm"
    # FIAF Moving Image Cataloguing Manual E.2.2
    Commercial = "Commercial"
    # FIAF Moving Image Cataloguing Manual 0.1.2, D.5.3
    EducationalFilm = "EducationalFilm"
    # FIAF Moving Image Cataloguing Manual 0.1.2
    EssayFilm = "EssayFilm"
    # FIAF Moving Image Cataloguing Manual 0.1.2
    ExperimentalFilm = "ExperimentalFilm"
    # FIAF Moving Image Cataloguing Manual D.5.3
    IndustrialFilm = "IndustrialFilm"
    # FIAF Moving Image Cataloguing Manual D.18
    MusicVideo = "MusicVideo"
    # http://www.screenonline.org.uk/film/id/476463/index.html
    Newsreel = "Newsreel"



class CategorizedThing(ConfiguredBaseModel):
    """
    Root for all classes with subclasses in this schema
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/be101407612d022cfdcc'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model'})

    category: Literal["https://av-efi.net/av-efi-schema/CategorizedThing","avefi:CategorizedThing"] = Field(default="avefi:CategorizedThing", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class MovingImageRecord(CategorizedThing):
    """
    Base class defining slots that are common to all levels of the WVMI metadata model
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/2e9c01efa0f0f6881365'},
                         'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/0e3ed2fb51ddeec3cb1f'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model'})

    described_by: Optional[DescriptionResource] = Field(default=None, description="""Also record some metadata about the PID itself rather than the identified object""", json_schema_extra = { "linkml_meta": {'alias': 'described_by',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'slot_uri': 'wdrs:describedby'} })
    has_alternative_title: Optional[List[Title]] = Field(default=None, description="""Additional title(s) associated with the work / variant, manifestation, or item.""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternative_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 3} })
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default=None, description="""Associate event(s) with a moving image record""", json_schema_extra = { "linkml_meta": {'alias': 'has_event',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 6} })
    has_identifier: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Record PID in this slot when exporting data from the PID system. Use local identifiers instead when PIDs have not been registered yet. The latter is suitable for transferring data to the agent responsible for registering PIDs""", json_schema_extra = { "linkml_meta": {'alias': 'has_identifier', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    has_primary_title: Optional[Title] = Field(default=None, description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""", json_schema_extra = { "linkml_meta": {'alias': 'has_primary_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 2} })
    has_source_key: Optional[List[str]] = Field(default=None, description="""Indicate a dataset this record has been generated or derived from. For example, a converter generating AVefi moving image records from data in some other schema may record the original identifier here.""", json_schema_extra = { "linkml_meta": {'alias': 'has_source_key', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/MovingImageRecord","avefi:MovingImageRecord"] = Field(default="avefi:MovingImageRecord", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class DescriptionResource(ConfiguredBaseModel):
    """
    Metadata about the PID rather than the identified object, i.e. who modified the PID metadata record when, making what changes
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/d0995eaddeeb07f3428d'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset']})

    has_history: Optional[str] = Field(default=None, description="""Link to revision history of this PID""", json_schema_extra = { "linkml_meta": {'alias': 'has_history', 'domain_of': ['DescriptionResource']} })
    has_issuer_id: str = Field(default=..., description="""Identifier for the responsible party as an URI suitable for linked data""", json_schema_extra = { "linkml_meta": {'alias': 'has_issuer_id',
         'domain_of': ['DescriptionResource'],
         'examples': [{'description': 'Link based on ISIL of the Filmmuseum Düsseldorf '
                                      '(preferred)',
                       'value': 'https://w3id.org/isil/DE-MUS-432511'},
                      {'description': 'ISIL of the Filmmuseum Düsseldorf resolved via '
                                      'Deutsche ISIL-Agentur directly',
                       'value': 'https://ld.zdb-services.de/resource/organisations/DE-MUS-432511'}],
         'in_subset': ['TypeRegistrySubset'],
         'slot_uri': 'wdrs:issuedby'} })
    has_issuer_name: str = Field(default=..., description="""Name of the responsible party""", json_schema_extra = { "linkml_meta": {'alias': 'has_issuer_name',
         'domain_of': ['DescriptionResource'],
         'examples': [{'description': 'Human readable name of the issuer',
                       'value': 'Filmmuseum Düsseldorf'}],
         'in_subset': ['TypeRegistrySubset'],
         'slot_uri': 'dcterms:contributor'} })
    last_modified: Optional[datetime ] = Field(default=None, description="""Timestamp (in UTC) for the latest modification to any field in the PID metadata record""", json_schema_extra = { "linkml_meta": {'alias': 'last_modified',
         'domain_of': ['DescriptionResource'],
         'slot_uri': 'dcterms:modified'} })


class WorkVariant(MovingImageRecord):
    """
    FIAF Moving Image Cataloguing Manual 1.0
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/7529ed598d0bd4fcf3d8'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'related_mappings': ['fiaf:WorkVariant'],
         'slot_usage': {'has_primary_title': {'name': 'has_primary_title',
                                              'required': True},
                        'same_as': {'annotations': {'pid': {'tag': 'pid',
                                                            'value': '21.T11969/6cd9c85272885fefa9c0'}},
                                    'any_of': [{'range': 'EIDRResource'},
                                               {'range': 'FilmportalResource'},
                                               {'range': 'GNDResource'},
                                               {'range': 'VIAFResource'},
                                               {'range': 'WikidataResource'}],
                                    'in_subset': ['TypeRegistrySubset'],
                                    'name': 'same_as'},
                        'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'WorkVariantTypeEnum',
                                 'required': True}},
         'structured_aliases': {'Werk': {'in_language': 'de', 'literal_form': 'Werk'},
                                'Work': {'in_language': 'en', 'literal_form': 'Work'}}})

    has_form: Optional[List[WorkFormEnum]] = Field(default=None, description="""Form describes the format and/or purpose of a Work, e.g., “non-fiction”, “short” and “animation”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.1""", json_schema_extra = { "linkml_meta": {'alias': 'has_form',
         'domain_of': ['WorkVariant'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 14} })
    has_genre: Optional[List[Genre]] = Field(default=None, description="""Genre describes categories of Works, characterized by similar plots, themes, settings, situations, and characters. Examples of genres are “westerns” and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.1""", json_schema_extra = { "linkml_meta": {'alias': 'has_genre',
         'domain_of': ['WorkVariant'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 15} })
    has_subject: Optional[List[Union[Agent, GeographicName, Subject]]] = Field(default=None, description="""Subject descriptor terms for the content of a film specifying its period, themes, locations, etc. Not to be confused with Genre. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.3""", json_schema_extra = { "linkml_meta": {'alias': 'has_subject',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/92555879f9ec3adef772'}},
         'any_of': [{'range': 'Subject'},
                    {'range': 'Agent'},
                    {'range': 'GeographicName'}],
         'domain_of': ['WorkVariant'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 14} })
    is_part_of: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Relate, for instance, episodes to a series / serial. See also: FIAF Moving Image Cataloguing Manual D.17""", json_schema_extra = { "linkml_meta": {'alias': 'is_part_of',
         'domain_of': ['WorkVariant'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 17} })
    is_variant_of: Optional[Union[MovingImageResource,AVefiResource,LocalResource]] = Field(default=None, description="""Link to the reference WorkVariant for the currently described variant. See also: FIAF Moving Image Cataloguing Manual 1.0.2, 1.1.2, 1.4.5""", json_schema_extra = { "linkml_meta": {'alias': 'is_variant_of',
         'domain_of': ['WorkVariant'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 18} })
    same_as: Optional[List[Union[EIDRResource, FilmportalResource, GNDResource, VIAFResource, WikidataResource]]] = Field(default=None, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'same_as',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/6cd9c85272885fefa9c0'}},
         'any_of': [{'range': 'EIDRResource'},
                    {'range': 'FilmportalResource'},
                    {'range': 'GNDResource'},
                    {'range': 'VIAFResource'},
                    {'range': 'WikidataResource'}],
         'domain_of': ['WorkVariant',
                       'GeographicName',
                       'Genre',
                       'Subject',
                       'Agent',
                       'Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    type: WorkVariantTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    variant_type: Optional[VariantTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual D.2""", json_schema_extra = { "linkml_meta": {'alias': 'variant_type',
         'domain_of': ['WorkVariant'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 18} })
    described_by: Optional[DescriptionResource] = Field(default=None, description="""Also record some metadata about the PID itself rather than the identified object""", json_schema_extra = { "linkml_meta": {'alias': 'described_by',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'slot_uri': 'wdrs:describedby'} })
    has_alternative_title: Optional[List[Title]] = Field(default=None, description="""Additional title(s) associated with the work / variant, manifestation, or item.""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternative_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 3} })
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default=None, description="""Associate event(s) with a moving image record""", json_schema_extra = { "linkml_meta": {'alias': 'has_event',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 6} })
    has_identifier: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Record PID in this slot when exporting data from the PID system. Use local identifiers instead when PIDs have not been registered yet. The latter is suitable for transferring data to the agent responsible for registering PIDs""", json_schema_extra = { "linkml_meta": {'alias': 'has_identifier', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    has_primary_title: Title = Field(default=..., description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""", json_schema_extra = { "linkml_meta": {'alias': 'has_primary_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 2} })
    has_source_key: Optional[List[str]] = Field(default=None, description="""Indicate a dataset this record has been generated or derived from. For example, a converter generating AVefi moving image records from data in some other schema may record the original identifier here.""", json_schema_extra = { "linkml_meta": {'alias': 'has_source_key', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/WorkVariant","avefi:WorkVariant"] = Field(default="avefi:WorkVariant", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class GeographicName(CategorizedThing):
    """
    Name of country, region or other location. Names should be taken from appropriate authorities (e.g. GND) and recorded as a human readable string in the name attribute and as linked data in the same_as attribute. See also: FIAF Moving Image Cataloguing Manual 1.3.3, D.4
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/bacbc4ae5eb2ac96982c'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 12,
         'related_mappings': ['fiaf:Country', 'fiaf:Location'],
         'slot_usage': {'same_as': {'annotations': {'pid': {'tag': 'pid',
                                                            'value': '21.T11969/dd35cd4d748c1785083a'}},
                                    'any_of': [{'range': 'GNDResource'},
                                               {'range': 'TGNResource'},
                                               {'range': 'VIAFResource'},
                                               {'range': 'WikidataResource'}],
                                    'in_subset': ['TypeRegistrySubset'],
                                    'name': 'same_as'}}})

    has_alternate_name: Optional[List[str]] = Field(default=None, description="""Alternative human-readable name(s) for a thing. Whereas has_name provides the preferred display name for the described entity, alternatives can be recorded here in order to be indexed in search engines, for instance""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternate_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 10,
         'slot_uri': 'schema:alternateName'} })
    has_name: str = Field(default=..., description="""Human-readable name for a thing. This is to be treated as the preferred display label in a UI context, whereas has_alternate_name can provide additional terms, e.g. for matching in search operations""", json_schema_extra = { "linkml_meta": {'alias': 'has_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent', 'Title'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 4,
         'slot_uri': 'schema:name'} })
    same_as: Optional[List[Union[GNDResource, TGNResource, VIAFResource, WikidataResource]]] = Field(default=None, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'same_as',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/dd35cd4d748c1785083a'}},
         'any_of': [{'range': 'GNDResource'},
                    {'range': 'TGNResource'},
                    {'range': 'VIAFResource'},
                    {'range': 'WikidataResource'}],
         'domain_of': ['WorkVariant',
                       'GeographicName',
                       'Genre',
                       'Subject',
                       'Agent',
                       'Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/GeographicName","avefi:GeographicName"] = Field(default="avefi:GeographicName", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Genre(ConfiguredBaseModel):
    """
    Genre describes categories of Works, characterized by similar plots, themes, settings, situations, and characters. Examples of genres are “westerns” and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.1
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/e70e5ae724f625a7477f'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 25,
         'slot_usage': {'same_as': {'in_subset': ['TypeRegistrySubset'],
                                    'name': 'same_as',
                                    'range': 'GNDResource'}},
         'structured_aliases': {'Genre': {'in_language': 'default',
                                          'literal_form': 'Genre'}}})

    has_alternate_name: Optional[List[str]] = Field(default=None, description="""Alternative human-readable name(s) for a thing. Whereas has_name provides the preferred display name for the described entity, alternatives can be recorded here in order to be indexed in search engines, for instance""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternate_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 10,
         'slot_uri': 'schema:alternateName'} })
    has_name: str = Field(default=..., description="""Human-readable name for a thing. This is to be treated as the preferred display label in a UI context, whereas has_alternate_name can provide additional terms, e.g. for matching in search operations""", json_schema_extra = { "linkml_meta": {'alias': 'has_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent', 'Title'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 4,
         'slot_uri': 'schema:name'} })
    same_as: Optional[List[GNDResource]] = Field(default=None, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'same_as',
         'domain_of': ['WorkVariant',
                       'GeographicName',
                       'Genre',
                       'Subject',
                       'Agent',
                       'Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })


class Subject(CategorizedThing):
    """
    Subject descriptor terms for the content of a film specifying its period, themes, locations, etc. Not to be confused with Genre. Provide name and if at all possible identifier(s) from supported authorities in the same_as slot. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.3
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/a3e99e02ddcb607c5242'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 23,
         'slot_usage': {'same_as': {'annotations': {'pid': {'tag': 'pid',
                                                            'value': '21.T11969/8281679d0e53548893b8'}},
                                    'any_of': [{'range': 'AVefiResource'},
                                               {'range': 'EIDRResource'},
                                               {'range': 'FilmportalResource'},
                                               {'range': 'GNDResource'},
                                               {'range': 'VIAFResource'},
                                               {'range': 'WikidataResource'}],
                                    'name': 'same_as'}},
         'structured_aliases': {'Schlagwort': {'in_language': 'de',
                                               'literal_form': 'Schlagwort'},
                                'Subject': {'in_language': 'en',
                                            'literal_form': 'Subject'}}})

    has_alternate_name: Optional[List[str]] = Field(default=None, description="""Alternative human-readable name(s) for a thing. Whereas has_name provides the preferred display name for the described entity, alternatives can be recorded here in order to be indexed in search engines, for instance""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternate_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 10,
         'slot_uri': 'schema:alternateName'} })
    has_name: str = Field(default=..., description="""Human-readable name for a thing. This is to be treated as the preferred display label in a UI context, whereas has_alternate_name can provide additional terms, e.g. for matching in search operations""", json_schema_extra = { "linkml_meta": {'alias': 'has_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent', 'Title'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 4,
         'slot_uri': 'schema:name'} })
    same_as: Optional[List[Union[AVefiResource, EIDRResource, FilmportalResource, GNDResource, VIAFResource, WikidataResource]]] = Field(default=None, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'same_as',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/8281679d0e53548893b8'}},
         'any_of': [{'range': 'AVefiResource'},
                    {'range': 'EIDRResource'},
                    {'range': 'FilmportalResource'},
                    {'range': 'GNDResource'},
                    {'range': 'VIAFResource'},
                    {'range': 'WikidataResource'}],
         'domain_of': ['WorkVariant',
                       'GeographicName',
                       'Genre',
                       'Subject',
                       'Agent',
                       'Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Subject","avefi:Subject"] = Field(default="avefi:Subject", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Activity(CategorizedThing):
    """
    FIAF Moving Image Cataloguing Manual 1.4.1.1
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/56b195f0220b7e220710'},
                         'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/e93415afce13f521e241'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 17,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'required': True}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: str = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Activity","avefi:Activity"] = Field(default="avefi:Activity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class AnimationActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.13
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/253658316bd6be837db1'}},
         'close_mappings': ['fiaf:AnimationActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'AnimationActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: AnimationActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/AnimationActivity","avefi:AnimationActivity"] = Field(default="avefi:AnimationActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class CastActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.7
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/c6830294ff6a4d8cbd75'}},
         'close_mappings': ['fiaf:CastActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'CastActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: CastActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/CastActivity","avefi:CastActivity"] = Field(default="avefi:CastActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class CensorshipActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.1
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/46ee382e391c4888ed22'}},
         'close_mappings': ['fiaf:CensorshipActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'CensorshipActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: CensorshipActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/CensorshipActivity","avefi:CensorshipActivity"] = Field(default="avefi:CensorshipActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class CinematographyActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.5
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/bae0899a406a0bd2bdaf'}},
         'close_mappings': ['fiaf:CinematographyActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'CinematographyActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: CinematographyActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/CinematographyActivity","avefi:CinematographyActivity"] = Field(default="avefi:CinematographyActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class CopyrightAndDistributionActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/bc2aab64b865b9d83909'}},
         'close_mappings': ['fiaf:CopyrightandDistributionActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'CopyrightAndDistributionActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: CopyrightAndDistributionActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/CopyrightAndDistributionActivity","avefi:CopyrightAndDistributionActivity"] = Field(default="avefi:CopyrightAndDistributionActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class DirectingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.3
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/484efc6c28cfc7732e75'}},
         'close_mappings': ['fiaf:DirectingActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'DirectingActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: DirectingActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/DirectingActivity","avefi:DirectingActivity"] = Field(default="avefi:DirectingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class EditingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.10
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/8b0add304c707db873f1'}},
         'close_mappings': ['fiaf:EditingActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'EditingActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: EditingActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/EditingActivity","avefi:EditingActivity"] = Field(default="avefi:EditingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class LaboratoryActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.12
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/9d570998dedf7c199c50'}},
         'close_mappings': ['fiaf:LaboratoryActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'LaboratoryActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: LaboratoryActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/LaboratoryActivity","avefi:LaboratoryActivity"] = Field(default="avefi:LaboratoryActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class MusicActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.11
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/92d2e34b5e93501ff9c7'}},
         'close_mappings': ['fiaf:MusicActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'MusicActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: MusicActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/MusicActivity","avefi:MusicActivity"] = Field(default="avefi:MusicActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class ProducingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/77193f6b9ff25dfd42f6'}},
         'close_mappings': ['fiaf:ProducingActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'ProducingActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: ProducingActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/ProducingActivity","avefi:ProducingActivity"] = Field(default="avefi:ProducingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class ProductionDesignActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.6
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/66f94179b4bc0ed8553f'}},
         'close_mappings': ['fiaf:ProductionDesignActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'ProductionDesignActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: ProductionDesignActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/ProductionDesignActivity","avefi:ProductionDesignActivity"] = Field(default="avefi:ProductionDesignActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class PuppetActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.14
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/cfe02de2e73e35984272'}},
         'close_mappings': ['fiaf:PuppetActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'PuppetActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: PuppetActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/PuppetActivity","avefi:PuppetActivity"] = Field(default="avefi:PuppetActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class SoundActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.9
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/33a013a7965dfd0337fa'}},
         'close_mappings': ['fiaf:SoundActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'SoundActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: SoundActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/SoundActivity","avefi:SoundActivity"] = Field(default="avefi:SoundActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class SpecialEffectsActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.8
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/ba0a31696080a881a41e'}},
         'close_mappings': ['fiaf:SpecialEffectsActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'SpecialEffectsActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: SpecialEffectsActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/SpecialEffectsActivity","avefi:SpecialEffectsActivity"] = Field(default="avefi:SpecialEffectsActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class WritingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.4
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/7b479b9faf0a25d41679'}},
         'close_mappings': ['fiaf:WritingActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'WritingActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: WritingActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/WritingActivity","avefi:WritingActivity"] = Field(default="avefi:WritingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class ManifestationActivity(Activity):
    """
    Activity types / roles. See also: FIAF Moving Image Cataloguing Manual 2.4.1.1, D.8
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/7a9e75d630f9d2d508f8'}},
         'close_mappings': ['fiaf:ManifestationActivity'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 16,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'ManifestationActivityTypeEnum'}}})

    has_agent: List[Agent] = Field(default=..., description="""Agent involved in some activity related to the moving image resource""", json_schema_extra = { "linkml_meta": {'alias': 'has_agent',
         'domain_of': ['Activity'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 9} })
    type: ManifestationActivityTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/ManifestationActivity","avefi:ManifestationActivity"] = Field(default="avefi:ManifestationActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Agent(CategorizedThing):
    """
    Agent involved in some activity related to the moving image resource. For agents of type \"Person\" specify name according to the convention \"family name, given name\"
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/77048147e58b6707508a'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 18,
         'related_mappings': ['fiaf:Agent', 'foaf:Agent'],
         'slot_usage': {'has_name': {'description': 'For natural persons, always use '
                                                    'the convention "family name, '
                                                    'given name"',
                                     'in_subset': ['TypeRegistrySubset'],
                                     'name': 'has_name'},
                        'same_as': {'annotations': {'pid': {'tag': 'pid',
                                                            'value': '21.T11969/7e899c043d05318a8ef7'}},
                                    'any_of': [{'range': 'FilmportalResource'},
                                               {'range': 'GNDResource'},
                                               {'range': 'VIAFResource'},
                                               {'range': 'WikidataResource'}],
                                    'in_subset': ['TypeRegistrySubset'],
                                    'name': 'same_as'},
                        'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'AgentTypeEnum',
                                 'required': True}}})

    has_alternate_name: Optional[List[str]] = Field(default=None, description="""Alternative human-readable name(s) for a thing. Whereas has_name provides the preferred display name for the described entity, alternatives can be recorded here in order to be indexed in search engines, for instance""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternate_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 10,
         'slot_uri': 'schema:alternateName'} })
    has_name: str = Field(default=..., description="""For natural persons, always use the convention \"family name, given name\"""", json_schema_extra = { "linkml_meta": {'alias': 'has_name',
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent', 'Title'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 4,
         'slot_uri': 'schema:name'} })
    same_as: Optional[List[Union[FilmportalResource, GNDResource, VIAFResource, WikidataResource]]] = Field(default=None, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""", json_schema_extra = { "linkml_meta": {'alias': 'same_as',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/7e899c043d05318a8ef7'}},
         'any_of': [{'range': 'FilmportalResource'},
                    {'range': 'GNDResource'},
                    {'range': 'VIAFResource'},
                    {'range': 'WikidataResource'}],
         'domain_of': ['WorkVariant',
                       'GeographicName',
                       'Genre',
                       'Subject',
                       'Agent',
                       'Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    type: AgentTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Agent","avefi:Agent"] = Field(default="avefi:Agent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Event(CategorizedThing):
    """
    Significant event in the lifecycle of moving image work / variant, manifestation or item. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country where the principal offices or production facilities of the production company are located for a production event. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual 1.4.2, 2.4.2, 3.3.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/28f74ae4dafa9d4dca35'},
                         'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/c60ff3f44c089ef17142'}},
         'close_mappings': ['fiaf:Event'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'rank': 15})

    has_activity: Optional[List[Union[Activity,AnimationActivity,CastActivity,CensorshipActivity,CinematographyActivity,CopyrightAndDistributionActivity,DirectingActivity,EditingActivity,LaboratoryActivity,MusicActivity,ProducingActivity,ProductionDesignActivity,PuppetActivity,SoundActivity,SpecialEffectsActivity,WritingActivity,ManifestationActivity]]] = Field(default=None, description="""Associate activity (and subsequently agents) with event""", json_schema_extra = { "linkml_meta": {'alias': 'has_activity',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 8} })
    has_date: Optional[str] = Field(default=None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See type ISODate definition for details""", json_schema_extra = { "linkml_meta": {'alias': 'has_date',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'notes': ['https://www.w3.org/TR/xmlschema11-2/#date'],
         'rank': 7} })
    located_in: Optional[List[GeographicName]] = Field(default=None, description="""Location associated with an event, e.g. the country where the principal offices or production facilities of the production company are located should be associated with the production event""", json_schema_extra = { "linkml_meta": {'alias': 'located_in',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 7} })
    category: Literal["https://av-efi.net/av-efi-schema/Event","avefi:Event"] = Field(default="avefi:Event", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class ProductionEvent(Event):
    """
    Production event of a work/variant (or manifestation produced as a restoration). Provide a date or a period of time via has_date and specify located_in as appropriate, e.g. the country where the principal offices or production facilities of the production company are located. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.3
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/85073ea1c5b995826a3c'}},
         'close_mappings': ['fiaf:ProductionEvent'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 13,
         'slot_usage': {'has_activity': {'annotations': {'pid': {'tag': 'pid',
                                                                 'value': '21.T11969/000ee0907b3a25f21d22'}},
                                         'any_of': [{'range': 'AnimationActivity'},
                                                    {'range': 'CastActivity'},
                                                    {'range': 'CinematographyActivity'},
                                                    {'range': 'DirectingActivity'},
                                                    {'range': 'EditingActivity'},
                                                    {'range': 'MusicActivity'},
                                                    {'range': 'ProducingActivity'},
                                                    {'range': 'ProductionDesignActivity'},
                                                    {'range': 'PuppetActivity'},
                                                    {'range': 'SoundActivity'},
                                                    {'range': 'SpecialEffectsActivity'},
                                                    {'range': 'WritingActivity'}],
                                         'in_subset': ['TypeRegistrySubset'],
                                         'name': 'has_activity'},
                        'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'ProductionEventTypeEnum'}},
         'structured_aliases': {'Production': {'in_language': 'en',
                                               'literal_form': 'Production'},
                                'Produktion': {'in_language': 'de',
                                               'literal_form': 'Produktion'}}})

    type: Optional[ProductionEventTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    has_activity: Optional[List[Union[AnimationActivity, CastActivity, CinematographyActivity, DirectingActivity, EditingActivity, MusicActivity, ProducingActivity, ProductionDesignActivity, PuppetActivity, SoundActivity, SpecialEffectsActivity, WritingActivity]]] = Field(default=None, description="""Associate activity (and subsequently agents) with event""", json_schema_extra = { "linkml_meta": {'alias': 'has_activity',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/000ee0907b3a25f21d22'}},
         'any_of': [{'range': 'AnimationActivity'},
                    {'range': 'CastActivity'},
                    {'range': 'CinematographyActivity'},
                    {'range': 'DirectingActivity'},
                    {'range': 'EditingActivity'},
                    {'range': 'MusicActivity'},
                    {'range': 'ProducingActivity'},
                    {'range': 'ProductionDesignActivity'},
                    {'range': 'PuppetActivity'},
                    {'range': 'SoundActivity'},
                    {'range': 'SpecialEffectsActivity'},
                    {'range': 'WritingActivity'}],
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 8} })
    has_date: Optional[str] = Field(default=None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See type ISODate definition for details""", json_schema_extra = { "linkml_meta": {'alias': 'has_date',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'notes': ['https://www.w3.org/TR/xmlschema11-2/#date'],
         'rank': 7} })
    located_in: Optional[List[GeographicName]] = Field(default=None, description="""Location associated with an event, e.g. the country where the principal offices or production facilities of the production company are located should be associated with the production event""", json_schema_extra = { "linkml_meta": {'alias': 'located_in',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 7} })
    category: Literal["https://av-efi.net/av-efi-schema/ProductionEvent","avefi:ProductionEvent"] = Field(default="avefi:ProductionEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class PreservationEvent(Event):
    """
    Preservation event originating a manifestation or possibly a vaniant. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.5
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/267f87868c98b2157407'}},
         'close_mappings': ['fiaf:PreservationEvent'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 13,
         'slot_usage': {'has_activity': {'in_subset': ['TypeRegistrySubset'],
                                         'name': 'has_activity',
                                         'range': 'ManifestationActivity',
                                         'required': True},
                        'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'PreservationEventTypeEnum',
                                 'required': True}}})

    type: PreservationEventTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    has_activity: List[ManifestationActivity] = Field(default=..., description="""Associate activity (and subsequently agents) with event""", json_schema_extra = { "linkml_meta": {'alias': 'has_activity',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 8} })
    has_date: Optional[str] = Field(default=None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See type ISODate definition for details""", json_schema_extra = { "linkml_meta": {'alias': 'has_date',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'notes': ['https://www.w3.org/TR/xmlschema11-2/#date'],
         'rank': 7} })
    located_in: Optional[List[GeographicName]] = Field(default=None, description="""Location associated with an event, e.g. the country where the principal offices or production facilities of the production company are located should be associated with the production event""", json_schema_extra = { "linkml_meta": {'alias': 'located_in',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 7} })
    category: Literal["https://av-efi.net/av-efi-schema/PreservationEvent","avefi:PreservationEvent"] = Field(default="avefi:PreservationEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class PublicationEvent(Event):
    """
    Publication event of a manifestation or possibly the first known publication of a work. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country where the manifestation was published. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.1
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/8e1f90c97bb610491c08'}},
         'close_mappings': ['fiaf:PublicationEvent'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 13,
         'slot_usage': {'has_activity': {'in_subset': ['TypeRegistrySubset'],
                                         'name': 'has_activity',
                                         'range': 'ManifestationActivity'},
                        'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'PublicationEventTypeEnum',
                                 'required': True}}})

    type: PublicationEventTypeEnum = Field(default=..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    has_activity: Optional[List[ManifestationActivity]] = Field(default=None, description="""Associate activity (and subsequently agents) with event""", json_schema_extra = { "linkml_meta": {'alias': 'has_activity',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 8} })
    has_date: Optional[str] = Field(default=None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See type ISODate definition for details""", json_schema_extra = { "linkml_meta": {'alias': 'has_date',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'notes': ['https://www.w3.org/TR/xmlschema11-2/#date'],
         'rank': 7} })
    located_in: Optional[List[GeographicName]] = Field(default=None, description="""Location associated with an event, e.g. the country where the principal offices or production facilities of the production company are located should be associated with the production event""", json_schema_extra = { "linkml_meta": {'alias': 'located_in',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 7} })
    category: Literal["https://av-efi.net/av-efi-schema/PublicationEvent","avefi:PublicationEvent"] = Field(default="avefi:PublicationEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class ManufactureEvent(Event):
    """
    Manufacture event of a manifestation. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country where the labratory is located. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.7
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/d714eff2626e41e41e78'}},
         'close_mappings': ['fiaf:ManufactureEvent'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 14,
         'slot_usage': {'has_activity': {'in_subset': ['TypeRegistrySubset'],
                                         'name': 'has_activity',
                                         'range': 'LaboratoryActivity'},
                        'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'ManufactureEventTypeEnum'}}})

    type: Optional[ManufactureEventTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    has_activity: Optional[List[LaboratoryActivity]] = Field(default=None, description="""Associate activity (and subsequently agents) with event""", json_schema_extra = { "linkml_meta": {'alias': 'has_activity',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 8} })
    has_date: Optional[str] = Field(default=None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See type ISODate definition for details""", json_schema_extra = { "linkml_meta": {'alias': 'has_date',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'notes': ['https://www.w3.org/TR/xmlschema11-2/#date'],
         'rank': 7} })
    located_in: Optional[List[GeographicName]] = Field(default=None, description="""Location associated with an event, e.g. the country where the principal offices or production facilities of the production company are located should be associated with the production event""", json_schema_extra = { "linkml_meta": {'alias': 'located_in',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 7} })
    category: Literal["https://av-efi.net/av-efi-schema/ManufactureEvent","avefi:ManufactureEvent"] = Field(default="avefi:ManufactureEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class RightsCopyrightRegistrationEvent(Event):
    """
    Copyright and related rights registration event of a manifestation or possibly of a work/variant. Always specify date via has_date. Specify located_in as appropriate, e.g. the country where the copyright was registered. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.4
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/87d9e566e2a5a6a9d1d6'}},
         'close_mappings': ['fiaf:RightsCopyrightRegistrationEvent'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 14,
         'slot_usage': {'has_activity': {'in_subset': ['TypeRegistrySubset'],
                                         'name': 'has_activity',
                                         'range': 'CopyrightAndDistributionActivity',
                                         'required': True}},
         'structured_aliases': {'Rechte': {'in_language': 'de',
                                           'literal_form': 'Rechte'},
                                'Rights': {'in_language': 'en',
                                           'literal_form': 'Rights'}}})

    has_activity: List[CopyrightAndDistributionActivity] = Field(default=..., description="""Associate activity (and subsequently agents) with event""", json_schema_extra = { "linkml_meta": {'alias': 'has_activity',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 8} })
    has_date: Optional[str] = Field(default=None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See type ISODate definition for details""", json_schema_extra = { "linkml_meta": {'alias': 'has_date',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'notes': ['https://www.w3.org/TR/xmlschema11-2/#date'],
         'rank': 7} })
    located_in: Optional[List[GeographicName]] = Field(default=None, description="""Location associated with an event, e.g. the country where the principal offices or production facilities of the production company are located should be associated with the production event""", json_schema_extra = { "linkml_meta": {'alias': 'located_in',
         'domain_of': ['Event'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 7} })
    category: Literal["https://av-efi.net/av-efi-schema/RightsCopyrightRegistrationEvent","avefi:RightsCopyrightRegistrationEvent"] = Field(default="avefi:RightsCopyrightRegistrationEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Title(ConfiguredBaseModel):
    """
    FIAF Moving Image Cataloguing Manual 1.3.2, 2.3.2, 3.1.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/768e0c1c69573fb588f6'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 11,
         'slot_usage': {'has_name': {'close_mappings': ['fiaf:hasTitleValue',
                                                        'schema:name'],
                                     'in_subset': ['TypeRegistrySubset'],
                                     'name': 'has_name'},
                        'type': {'description': 'FIAF Moving Image Cataloguing Manual '
                                                'A.2',
                                 'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'TitleTypeEnum',
                                 'required': True}}})

    has_name: str = Field(default=..., description="""Human-readable name for a thing. This is to be treated as the preferred display label in a UI context, whereas has_alternate_name can provide additional terms, e.g. for matching in search operations""", json_schema_extra = { "linkml_meta": {'alias': 'has_name',
         'close_mappings': ['fiaf:hasTitleValue', 'schema:name'],
         'domain_of': ['GeographicName', 'Genre', 'Subject', 'Agent', 'Title'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 4,
         'slot_uri': 'schema:name'} })
    has_ordering_name: Optional[str] = Field(default=None, description="""Provide normalised form, e.g. for sorting by title. Only use this slot if value actually if different from has_name""", json_schema_extra = { "linkml_meta": {'alias': 'has_ordering_name',
         'domain_of': ['Title'],
         'examples': [{'description': 'For display title: An American in Paris',
                       'value': 'American in Paris, An'},
                      {'description': 'For display title: Star Wars: Episode IX – Der '
                                      'Aufstieg Skywalkers',
                       'value': 'Star Wars: Episode 9 – Der Aufstieg Skywalkers'}],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 4} })
    type: TitleTypeEnum = Field(default=..., description="""FIAF Moving Image Cataloguing Manual A.2""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })


class ManifestationOrItem(MovingImageRecord):
    """
    Base class defining common slots for manifestations and items
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/b4db4a39a902f7abed4f'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model'})

    has_colour_type: Optional[ColourTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.4, 3.1.5.6, D.7.11""", json_schema_extra = { "linkml_meta": {'alias': 'has_colour_type',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 27} })
    has_duration: Optional[Duration] = Field(default=None, description="""Total running time of the described object in ISO 8601 duration format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11""", json_schema_extra = { "linkml_meta": {'alias': 'has_duration',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 24} })
    has_extent: Optional[Extent] = Field(default=None, description="""Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8""", json_schema_extra = { "linkml_meta": {'alias': 'has_extent',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 24} })
    has_format: Optional[List[Union[Format,Audio,DigitalFile,DigitalFileEncoding,Film,Optical,Video]]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.1, 3.1.5.1""", json_schema_extra = { "linkml_meta": {'alias': 'has_format',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 23} })
    has_note: Optional[List[str]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual Appendix B""", json_schema_extra = { "linkml_meta": {'alias': 'has_note',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 29} })
    has_sound_type: Optional[SoundTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.3, 3.1.5.3, D.7.4""", json_schema_extra = { "linkml_meta": {'alias': 'has_sound_type',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 27} })
    has_webresource: Optional[List[str]] = Field(default=None, description="""Link to data provider's own presentation of manifestation or item on the web""", json_schema_extra = { "linkml_meta": {'alias': 'has_webresource',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 28} })
    in_language: Optional[List[Language]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""", json_schema_extra = { "linkml_meta": {'alias': 'in_language',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 11,
         'related_mappings': ['fiaf:hasLanguage', 'schema:inLanguage']} })
    described_by: Optional[DescriptionResource] = Field(default=None, description="""Also record some metadata about the PID itself rather than the identified object""", json_schema_extra = { "linkml_meta": {'alias': 'described_by',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'slot_uri': 'wdrs:describedby'} })
    has_alternative_title: Optional[List[Title]] = Field(default=None, description="""Additional title(s) associated with the work / variant, manifestation, or item.""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternative_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 3} })
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default=None, description="""Associate event(s) with a moving image record""", json_schema_extra = { "linkml_meta": {'alias': 'has_event',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 6} })
    has_identifier: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Record PID in this slot when exporting data from the PID system. Use local identifiers instead when PIDs have not been registered yet. The latter is suitable for transferring data to the agent responsible for registering PIDs""", json_schema_extra = { "linkml_meta": {'alias': 'has_identifier', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    has_primary_title: Optional[Title] = Field(default=None, description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""", json_schema_extra = { "linkml_meta": {'alias': 'has_primary_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 2} })
    has_source_key: Optional[List[str]] = Field(default=None, description="""Indicate a dataset this record has been generated or derived from. For example, a converter generating AVefi moving image records from data in some other schema may record the original identifier here.""", json_schema_extra = { "linkml_meta": {'alias': 'has_source_key', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/ManifestationOrItem","avefi:ManifestationOrItem"] = Field(default="avefi:ManifestationOrItem", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Duration(ConfiguredBaseModel):
    """
    Total running time of the described object in ISO 8601 duration format. Check has_value slot range documentation for examples of permissible values. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/df7f2b4d340532f48431'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 33,
         'slot_usage': {'has_value': {'in_subset': ['TypeRegistrySubset'],
                                      'name': 'has_value',
                                      'range': 'ISODurationInHours'}},
         'structured_aliases': {'Abspieldauer': {'in_language': 'de',
                                                 'literal_form': 'Abspieldauer'},
                                'Running Time': {'in_language': 'en',
                                                 'literal_form': 'Running Time'}}})

    has_value: str = Field(default=..., description="""Value of some quantity""", json_schema_extra = { "linkml_meta": {'alias': 'has_value',
         'domain_of': ['Duration', 'Extent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 25} })
    has_precision: Optional[PrecisionEnum] = Field(default=None, description="""Qualifier indicating the precision of an extent value or duration""", json_schema_extra = { "linkml_meta": {'alias': 'has_precision',
         'domain_of': ['Duration', 'Extent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 26} })


class Extent(ConfiguredBaseModel):
    """
    Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/9e169a9a3af6df0758ed'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 35,
         'structured_aliases': {'Extent': {'in_language': 'en',
                                           'literal_form': 'Extent'},
                                'Länge / Größe': {'in_language': 'de',
                                                  'literal_form': 'Länge / Größe'}}})

    has_unit: UnitEnum = Field(default=..., description="""Unit of some quantity""", json_schema_extra = { "linkml_meta": {'alias': 'has_unit',
         'domain_of': ['Extent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 26} })
    has_value: Decimal = Field(default=..., description="""Value of some quantity""", json_schema_extra = { "linkml_meta": {'alias': 'has_value',
         'domain_of': ['Duration', 'Extent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 25} })
    has_precision: Optional[PrecisionEnum] = Field(default=None, description="""Qualifier indicating the precision of an extent value or duration""", json_schema_extra = { "linkml_meta": {'alias': 'has_precision',
         'domain_of': ['Duration', 'Extent'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 26} })


class Format(CategorizedThing):
    """
    FIAF Moving Image Cataloguing Manual 2.3.4.1, 3.1.5.1
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/9f6ce2fc052b3ae49a80'},
                         'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/d3869bbc9a1b9f1a0fd1'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'rank': 31})

    type: Optional[str] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Format","avefi:Format"] = Field(default="avefi:Format", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Audio(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/5d0612962482536035d7'}},
         'close_mappings': ['fiaf:Audio'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 32,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'FormatAudioTypeEnum'}},
         'structured_aliases': {'Audio': {'in_language': 'default',
                                          'literal_form': 'Audio'}}})

    type: Optional[FormatAudioTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Audio","avefi:Audio"] = Field(default="avefi:Audio", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class DigitalFile(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/f24e4ac9459b80d59472'}},
         'close_mappings': ['fiaf:DigitalFile'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 32,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'FormatDigitalFileTypeEnum'}},
         'structured_aliases': {'Datei': {'in_language': 'de', 'literal_form': 'Datei'},
                                'Digital File': {'in_language': 'en',
                                                 'literal_form': 'Digital File'}}})

    type: Optional[FormatDigitalFileTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/DigitalFile","avefi:DigitalFile"] = Field(default="avefi:DigitalFile", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class DigitalFileEncoding(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/7838de709db400991647'}},
         'close_mappings': ['fiaf:DigitalFileEncoding'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 32,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'FormatDigitalFileEncodingTypeEnum'}},
         'structured_aliases': {'Encoding': {'in_language': 'de',
                                             'literal_form': 'Encoding'},
                                'File Encoding': {'in_language': 'en',
                                                  'literal_form': 'File Encoding'}}})

    type: Optional[FormatDigitalFileEncodingTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/DigitalFileEncoding","avefi:DigitalFileEncoding"] = Field(default="avefi:DigitalFileEncoding", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Film(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/80d81e2684b42bb72bc0'}},
         'close_mappings': ['fiaf:Film'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 32,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'FormatFilmTypeEnum'}},
         'structured_aliases': {'Film': {'in_language': 'default',
                                         'literal_form': 'Film'}}})

    type: Optional[FormatFilmTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Film","avefi:Film"] = Field(default="avefi:Film", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Optical(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/8492e19b115e84682060'}},
         'close_mappings': ['fiaf:Optical'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 32,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'FormatOpticalTypeEnum'}},
         'structured_aliases': {'Optical': {'in_language': 'en',
                                            'literal_form': 'Optical'},
                                'Optisch': {'in_language': 'de',
                                            'literal_form': 'Optisch'}}})

    type: Optional[FormatOpticalTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Optical","avefi:Optical"] = Field(default="avefi:Optical", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Video(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/4df1c81c76d3c72a9538'}},
         'close_mappings': ['fiaf:Video'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 32,
         'slot_usage': {'type': {'in_subset': ['TypeRegistrySubset'],
                                 'name': 'type',
                                 'range': 'FormatVideoTypeEnum'}},
         'structured_aliases': {'Video': {'in_language': 'default',
                                          'literal_form': 'Video'}}})

    type: Optional[FormatVideoTypeEnum] = Field(default=None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['WorkVariant',
                       'Activity',
                       'Agent',
                       'ProductionEvent',
                       'PreservationEvent',
                       'PublicationEvent',
                       'ManufactureEvent',
                       'Title',
                       'Format'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Video","avefi:Video"] = Field(default="avefi:Video", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Manifestation(ManifestationOrItem):
    """
    Manifestation as defined in FIAF Moving Image Cataloguing Manual 2.0. Note that manifestation type is recorded as publication event type
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/f3bf8470b8d25586300c'}},
         'close_mappings': ['fiaf:Manifestation'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 2,
         'slot_usage': {'same_as': {'annotations': {'pid': {'tag': 'pid',
                                                            'value': '21.T11969/3b99e7540cf4f5f55cac'}},
                                    'any_of': [{'range': 'MovingImageResource'},
                                               {'range': 'EIDRResource'}],
                                    'description': 'Link to AVefi resource registered '
                                                   'by another data provider '
                                                   'indicating that the two '
                                                   'manifestations are known to be the '
                                                   'same. Use this, for instance, when '
                                                   'you have cooperated in making a '
                                                   'digital restoration of some film '
                                                   'work',
                                    'in_subset': ['TypeRegistrySubset'],
                                    'name': 'same_as'}},
         'structured_aliases': {'Manifestation': {'in_language': 'default',
                                                  'literal_form': 'Manifestation'}}})

    has_item: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Indicate AVefi Items the institution has registered as part of the manifestation""", json_schema_extra = { "linkml_meta": {'alias': 'has_item',
         'domain_of': ['Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 22} })
    is_manifestation_of: List[Union[MovingImageResource,AVefiResource,LocalResource]] = Field(default=..., description="""Indicate AVefi WorkVariant (possibly more but no less than one) that is subject of the manifestation""", json_schema_extra = { "linkml_meta": {'alias': 'is_manifestation_of',
         'domain_of': ['Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 21} })
    same_as: Optional[List[Union[EIDRResource, Union[MovingImageResource,AVefiResource,LocalResource]]]] = Field(default=None, description="""Link to AVefi resource registered by another data provider indicating that the two manifestations are known to be the same. Use this, for instance, when you have cooperated in making a digital restoration of some film work""", json_schema_extra = { "linkml_meta": {'alias': 'same_as',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/3b99e7540cf4f5f55cac'}},
         'any_of': [{'range': 'MovingImageResource'}, {'range': 'EIDRResource'}],
         'domain_of': ['WorkVariant',
                       'GeographicName',
                       'Genre',
                       'Subject',
                       'Agent',
                       'Manifestation'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    has_colour_type: Optional[ColourTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.4, 3.1.5.6, D.7.11""", json_schema_extra = { "linkml_meta": {'alias': 'has_colour_type',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 27} })
    has_duration: Optional[Duration] = Field(default=None, description="""Total running time of the described object in ISO 8601 duration format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11""", json_schema_extra = { "linkml_meta": {'alias': 'has_duration',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 24} })
    has_extent: Optional[Extent] = Field(default=None, description="""Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8""", json_schema_extra = { "linkml_meta": {'alias': 'has_extent',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 24} })
    has_format: Optional[List[Union[Format,Audio,DigitalFile,DigitalFileEncoding,Film,Optical,Video]]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.1, 3.1.5.1""", json_schema_extra = { "linkml_meta": {'alias': 'has_format',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 23} })
    has_note: Optional[List[str]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual Appendix B""", json_schema_extra = { "linkml_meta": {'alias': 'has_note',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 29} })
    has_sound_type: Optional[SoundTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.3, 3.1.5.3, D.7.4""", json_schema_extra = { "linkml_meta": {'alias': 'has_sound_type',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 27} })
    has_webresource: Optional[List[str]] = Field(default=None, description="""Link to data provider's own presentation of manifestation or item on the web""", json_schema_extra = { "linkml_meta": {'alias': 'has_webresource',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 28} })
    in_language: Optional[List[Language]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""", json_schema_extra = { "linkml_meta": {'alias': 'in_language',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 11,
         'related_mappings': ['fiaf:hasLanguage', 'schema:inLanguage']} })
    described_by: Optional[DescriptionResource] = Field(default=None, description="""Also record some metadata about the PID itself rather than the identified object""", json_schema_extra = { "linkml_meta": {'alias': 'described_by',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'slot_uri': 'wdrs:describedby'} })
    has_alternative_title: Optional[List[Title]] = Field(default=None, description="""Additional title(s) associated with the work / variant, manifestation, or item.""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternative_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 3} })
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default=None, description="""Associate event(s) with a moving image record""", json_schema_extra = { "linkml_meta": {'alias': 'has_event',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 6} })
    has_identifier: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Record PID in this slot when exporting data from the PID system. Use local identifiers instead when PIDs have not been registered yet. The latter is suitable for transferring data to the agent responsible for registering PIDs""", json_schema_extra = { "linkml_meta": {'alias': 'has_identifier', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    has_primary_title: Optional[Title] = Field(default=None, description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""", json_schema_extra = { "linkml_meta": {'alias': 'has_primary_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 2} })
    has_source_key: Optional[List[str]] = Field(default=None, description="""Indicate a dataset this record has been generated or derived from. For example, a converter generating AVefi moving image records from data in some other schema may record the original identifier here.""", json_schema_extra = { "linkml_meta": {'alias': 'has_source_key', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Manifestation","avefi:Manifestation"] = Field(default="avefi:Manifestation", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class Language(ConfiguredBaseModel):
    """
    Provide language code from ISO 639-2 (Part 2: Alpha-3) and a list of language usage terms from our controlled vocabulary. See also: FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/ea0bf80a52047e9d46f5'}},
         'examples': [{'description': 'English', 'value': 'eng'},
                      {'description': 'German', 'value': 'deu'},
                      {'description': 'Arabic', 'value': 'ara'}],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 21,
         'structured_aliases': {'Language': {'in_language': 'en',
                                             'literal_form': 'Language'},
                                'Sprache': {'in_language': 'de',
                                            'literal_form': 'Sprache'}}})

    code: Optional[LanguageCodeEnum] = Field(default=None, description="""[ISO 639-2 code](https://id.loc.gov/vocabulary/iso639-2.html) for the Representation of Names of Languages (Part 2: Alpha-3)""", json_schema_extra = { "linkml_meta": {'alias': 'code',
         'domain_of': ['Language'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 12,
         'see_also': ['https://id.loc.gov/vocabulary/iso639-2.html']} })
    usage: List[LanguageUsageEnum] = Field(default=..., description="""FIAF Moving Image Cataloguing Manual 2.3.3.2""", json_schema_extra = { "linkml_meta": {'alias': 'usage',
         'domain_of': ['Language'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 12} })


class Item(ManifestationOrItem):
    """
    FIAF Moving Image Cataloguing Manual 3.0
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/e8fb4f7dbead9e73589d'}},
         'broad_mappings': ['fiaf:Item'],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 3,
         'structured_aliases': {'Exemplar': {'in_language': 'de',
                                             'literal_form': 'Exemplar'},
                                'Item': {'in_language': 'en', 'literal_form': 'Item'}}})

    element_type: Optional[ItemElementTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual D.7.8""", json_schema_extra = { "linkml_meta": {'alias': 'element_type',
         'domain_of': ['Item'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 33} })
    has_access_status: Optional[ItemAccessStatusEnum] = Field(default=None, description="""Status of item determining access conditions. See also FIAF Moving Image Cataloguing Manual D.7.1""", json_schema_extra = { "linkml_meta": {'alias': 'has_access_status',
         'domain_of': ['Item'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 36} })
    has_frame_rate: Optional[FrameRateEnum] = Field(default=None, description="""Frame Rate describes the number of frames per second of an item. See also: FIAF Moving Image Cataloguing Manual 3.1.5.12.""", json_schema_extra = { "linkml_meta": {'alias': 'has_frame_rate',
         'domain_of': ['Item'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 36} })
    is_copy_of: Optional[List[Union[DOIResource, Union[MovingImageResource,AVefiResource,LocalResource]]]] = Field(default=None, description="""Link to AVefi item registered by another institution indicating that the two are known to be copies of each other""", json_schema_extra = { "linkml_meta": {'alias': 'is_copy_of',
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/4e81c9e20d5eba03f957'}},
         'any_of': [{'range': 'DOIResource'}, {'range': 'MovingImageResource'}],
         'domain_of': ['Item'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 39} })
    is_derivative_of: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Link to AVefi item from which this one has been derived in whole or in part, e.g. as a result of a restoration or digitasation project""", json_schema_extra = { "linkml_meta": {'alias': 'is_derivative_of',
         'domain_of': ['Item'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 39} })
    is_item_of: Union[MovingImageResource,AVefiResource,LocalResource] = Field(default=..., description="""Indicate AVefi Manifestation the item belongs to. Every item must be associated with a manifestation from the same data provider""", json_schema_extra = { "linkml_meta": {'alias': 'is_item_of',
         'domain_of': ['Item'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 31} })
    has_colour_type: Optional[ColourTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.4, 3.1.5.6, D.7.11""", json_schema_extra = { "linkml_meta": {'alias': 'has_colour_type',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 27} })
    has_duration: Optional[Duration] = Field(default=None, description="""Total running time of the described object in ISO 8601 duration format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11""", json_schema_extra = { "linkml_meta": {'alias': 'has_duration',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 24} })
    has_extent: Optional[Extent] = Field(default=None, description="""Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8""", json_schema_extra = { "linkml_meta": {'alias': 'has_extent',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 24} })
    has_format: Optional[List[Union[Format,Audio,DigitalFile,DigitalFileEncoding,Film,Optical,Video]]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.1, 3.1.5.1""", json_schema_extra = { "linkml_meta": {'alias': 'has_format',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 23} })
    has_note: Optional[List[str]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual Appendix B""", json_schema_extra = { "linkml_meta": {'alias': 'has_note',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 29} })
    has_sound_type: Optional[SoundTypeEnum] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.3, 3.1.5.3, D.7.4""", json_schema_extra = { "linkml_meta": {'alias': 'has_sound_type',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 27} })
    has_webresource: Optional[List[str]] = Field(default=None, description="""Link to data provider's own presentation of manifestation or item on the web""", json_schema_extra = { "linkml_meta": {'alias': 'has_webresource',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 28} })
    in_language: Optional[List[Language]] = Field(default=None, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""", json_schema_extra = { "linkml_meta": {'alias': 'in_language',
         'domain_of': ['ManifestationOrItem'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 11,
         'related_mappings': ['fiaf:hasLanguage', 'schema:inLanguage']} })
    described_by: Optional[DescriptionResource] = Field(default=None, description="""Also record some metadata about the PID itself rather than the identified object""", json_schema_extra = { "linkml_meta": {'alias': 'described_by',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'slot_uri': 'wdrs:describedby'} })
    has_alternative_title: Optional[List[Title]] = Field(default=None, description="""Additional title(s) associated with the work / variant, manifestation, or item.""", json_schema_extra = { "linkml_meta": {'alias': 'has_alternative_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 3} })
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default=None, description="""Associate event(s) with a moving image record""", json_schema_extra = { "linkml_meta": {'alias': 'has_event',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 6} })
    has_identifier: Optional[List[Union[MovingImageResource,AVefiResource,LocalResource]]] = Field(default=None, description="""Record PID in this slot when exporting data from the PID system. Use local identifiers instead when PIDs have not been registered yet. The latter is suitable for transferring data to the agent responsible for registering PIDs""", json_schema_extra = { "linkml_meta": {'alias': 'has_identifier', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    has_primary_title: Optional[Title] = Field(default=None, description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""", json_schema_extra = { "linkml_meta": {'alias': 'has_primary_title',
         'domain_of': ['MovingImageRecord'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 2} })
    has_source_key: Optional[List[str]] = Field(default=None, description="""Indicate a dataset this record has been generated or derived from. For example, a converter generating AVefi moving image records from data in some other schema may record the original identifier here.""", json_schema_extra = { "linkml_meta": {'alias': 'has_source_key', 'domain_of': ['MovingImageRecord'], 'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/Item","avefi:Item"] = Field(default="avefi:Item", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class MovingImageRecordContainer(ConfiguredBaseModel):
    """
    A holder for MovingImageRecord objects
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/873d5c9f6ebbffecf1df'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 100,
         'tree_root': True})

    has_record: Union[MovingImageRecord,WorkVariant,ManifestationOrItem,Manifestation,Item] = Field(default=..., description="""Root slot holding the moving image metadata record, i.e. metadata describing a work/variant, manifestation or item. See also the Introduction of the FIAF Moving Image Cataloguing Manual""", json_schema_extra = { "linkml_meta": {'alias': 'has_record',
         'domain_of': ['MovingImageRecordContainer'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1} })


class AuthorityResource(CategorizedThing):
    """
    Root class for all identifiers from some kind of authority or public register widely accepted in the community
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/a170a3147e7ef872d701'},
                         'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/899f581d3d58acc1918d'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'required': True}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/AuthorityResource","avefi:AuthorityResource"] = Field(default="avefi:AuthorityResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class MovingImageResource(AuthorityResource):
    """
    Either a persistent or local identifier for AVefi compliant moving image records. See subclasses for details
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'annotations': {'pid': {'tag': 'pid',
                                 'value': '21.T11969/efb65a41ee9d746a5e69'},
                         'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/e15fa59d1733320642b6'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model'})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/MovingImageResource","avefi:MovingImageResource"] = Field(default="avefi:MovingImageResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class AVefiResource(MovingImageResource):
    """
    Handle with the prefix allocated for AVefi (eventually). Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'https://hdl.handle.net/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/ab7fbf47063917f34150'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'AVefi'}},
         'structured_aliases': {'AVefi': {'in_language': 'default',
                                          'literal_form': 'AVefi'}},
         'todos': ['Possibly change formatter URIs/URLs to the av-efi.net domain when '
                   'the details have been sorted out']})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/AVefiResource","avefi:AVefiResource"] = Field(default="avefi:AVefiResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class DOIResource(AuthorityResource):
    """
    Digital Object Identifier maintained by the DOI Foundation and commonly used for scientific publications including films. Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'http://dx.doi.org/$1'},
                         'formatter_url_for_web_resource': {'tag': 'formatter_url_for_web_resource',
                                                            'value': 'https://doi.org/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/eba491f4edadbea9133c'},
                         'provides': {'tag': 'provides', 'value': ['ItemIdentifier']},
                         'trunk_pid': {'tag': 'trunk_pid',
                                       'value': '21.T11969/3118e53a91b1a64b2d8c'}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'see_also': ['https://dx.doi.org/',
                      'https://www.wikidata.org/wiki/Property:P356'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'DOI'}},
         'structured_aliases': {'DOI': {'in_language': 'default',
                                        'literal_form': 'DOI'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/DOIResource","avefi:DOIResource"] = Field(default="avefi:DOIResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class EIDRResource(AuthorityResource):
    """
    Entertainment Identifier Registry ID. Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'http://dx.doi.org/$1'},
                         'formatter_url_for_web_resource': {'tag': 'formatter_url_for_web_resource',
                                                            'value': 'https://doi.org/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/8f381d5d7eec3f90d236'},
                         'provides': {'tag': 'provides',
                                      'value': ['CreativeWorkIdentifier']}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'see_also': ['https://www.eidr.org/',
                      'https://www.wikidata.org/wiki/Property:P2704'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'EIDR'}},
         'structured_aliases': {'EIDR': {'in_language': 'default',
                                         'literal_form': 'EIDR'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/EIDRResource","avefi:EIDRResource"] = Field(default="avefi:EIDRResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class FilmportalResource(AuthorityResource):
    """
    Identifier of the German Filmportal.de. Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'https://www.filmportal.de/$1'},
                         'formatter_uri_for_web_resource': {'tag': 'formatter_uri_for_web_resource',
                                                            'value': 'https://www.filmportal.de/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/03890667c65c11066ac2'},
                         'provides': {'tag': 'provides',
                                      'value': ['CreativeWorkIdentifier',
                                                'PersonIdentifier']}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'see_also': ['https://www.filmportal.de/',
                      'https://www.wikidata.org/entity/P2639'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'FilmportalID'}},
         'structured_aliases': {'Filmportal': {'in_language': 'default',
                                               'literal_form': 'Filmportal'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/FilmportalResource","avefi:FilmportalResource"] = Field(default="avefi:FilmportalResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class GNDResource(AuthorityResource):
    """
    Gemeinsame Normdatei (GND) identifier maintained by Deutsche Nationalbibliothek (German National Library)
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'alternative_web_resource': {'tag': 'alternative_web_resource',
                                                      'value': 'https://explore.gnd.network/gnd/$1/relations'},
                         'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'https://d-nb.info/gnd/$1'},
                         'formatter_url_for_web_resource': {'tag': 'formatter_url_for_web_resource',
                                                            'value': 'https://d-nb.info/gnd/$1'},
                         'other_resources': {'tag': 'other_resources',
                                             'value': ['https://d-nb.info/gnd/$1/about/lds',
                                                       'https://hub.culturegraph.org/entityfacts/$1',
                                                       'https://lobid.org/gnd/$1']},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/1e67c576c1bdc5229b7a'},
                         'provides': {'tag': 'provides',
                                      'value': ['CreativeWorkIdentifier',
                                                'PlaceIdentifier',
                                                'OrganizationIdentifier',
                                                'PersonIdentifier',
                                                'SubjectHeadingIdentifier']}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'notes': ['API documentation including auto-complete suggestions at '
                   'https://lobid.org/gnd/api'],
         'rank': 51,
         'see_also': ['https://www.wikidata.org/entity/P227'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'GNDID'}},
         'structured_aliases': {'GND': {'in_language': 'default',
                                        'literal_form': 'GND'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/GNDResource","avefi:GNDResource"] = Field(default="avefi:GNDResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class ISILResource(AuthorityResource):
    """
    International Standard Identifier for Libraries and Related Organizations including (film) archives. Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_url_for_web_resource': {'tag': 'formatter_url_for_web_resource',
                                                            'value': 'https://w3id.org/isil/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/6a4cf32fdb37e46b2a3c'},
                         'provides': {'tag': 'provides',
                                      'value': ['OrganizationIdentifier']}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'see_also': ['https://biblstandard.dk/isil/index.htm',
                      'https://www.wikidata.org/wiki/Property:P791'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'ISIL'}},
         'structured_aliases': {'ISIL': {'in_language': 'default',
                                         'literal_form': 'ISIL'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/ISILResource","avefi:ISILResource"] = Field(default="avefi:ISILResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class LocalResource(MovingImageResource):
    """
    Some identifier used by data provider to represent relations between work/variant, manifestation and item when PIDs have not been assigned yet. On ingest into AVefi, these identifiers will be replaced by the generated PIDs
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'examples': [{'description': 'Local / temporary identifier for work record',
                       'value': 'some_fairly/arbitrary-string%for+1.work'},
                      {'description': 'Local / temporary identifier for manifestation '
                                      'record',
                       'value': 'id_for_manifestation'}],
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'notes': ['Not to be implemented in DTR'],
         'rank': 51})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/LocalResource","avefi:LocalResource"] = Field(default="avefi:LocalResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class TGNResource(AuthorityResource):
    """
    Getty Thesaurus of Geographic Names ID. Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'http://vocab.getty.edu/tgn/$1'},
                         'formatter_url_for_web_resource': {'tag': 'formatter_url_for_web_resource',
                                                            'value': 'https://vocab.getty.edu/page/tgn/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/2296a5d6afe67e99fe50'},
                         'provides': {'tag': 'provides', 'value': ['PlaceIdentifier']}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'see_also': ['https://www.getty.edu/research/tools/vocabularies/tgn/index.html',
                      'https://vocab.getty.edu/resource?uri=http://vocab.getty.edu/dataset/tgn',
                      'https://www.wikidata.org/wiki/Property:P1667'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'TGNID'}},
         'structured_aliases': {'TGN': {'in_language': 'default',
                                        'literal_form': 'TGN'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/TGNResource","avefi:TGNResource"] = Field(default="avefi:TGNResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class VIAFResource(AuthorityResource):
    """
    Virtual International Authority File identifier hosted by OCLC. The data is accumulated from various well established authority files from different parts of the world. Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'http://viaf.org/viaf/$1'},
                         'formatter_url_for_web_resource': {'tag': 'formatter_url_for_web_resource',
                                                            'value': 'https://viaf.org/viaf/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/b149c96db85b995926fa'},
                         'provides': {'tag': 'provides',
                                      'value': ['CreativeWorkIdentifier',
                                                'PlaceIdentifier',
                                                'OrganizationIdentifier',
                                                'PersonIdentifier']}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'see_also': ['https://viaf.org/', 'https://www.wikidata.org/entity/P214'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'VIAFID'}},
         'structured_aliases': {'VIAF': {'in_language': 'default',
                                         'literal_form': 'VIAF'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/VIAFResource","avefi:VIAFResource"] = Field(default="avefi:VIAFResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


class WikidataResource(AuthorityResource):
    """
    Identifier for Wikidata entities. Check id slot range documentation for examples
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'annotations': {'formatter_uri_for_rdf_resource': {'tag': 'formatter_uri_for_rdf_resource',
                                                            'value': 'https://www.wikidata.org/entity/$1'},
                         'formatter_url_for_web_resource': {'tag': 'formatter_url_for_web_resource',
                                                            'value': 'https://www.wikidata.org/entity/$1'},
                         'pid': {'tag': 'pid',
                                 'value': '21.T11969/1c463f1c2cf1187356d8'},
                         'provides': {'tag': 'provides',
                                      'value': ['CreativeWorkIdentifier',
                                                'PlaceIdentifier',
                                                'OrganizationIdentifier',
                                                'PersonIdentifier',
                                                'SubjectHeadingIdentifier']}},
         'from_schema': 'https://av-efi.github.io/av-efi-schema/model',
         'in_subset': ['TypeRegistrySubset'],
         'rank': 51,
         'see_also': ['https://www.wikidata.org/wiki/Wikidata:Identifiers'],
         'slot_usage': {'id': {'in_subset': ['TypeRegistrySubset'],
                               'name': 'id',
                               'range': 'WikidataID'}},
         'structured_aliases': {'Wikidata': {'in_language': 'default',
                                             'literal_form': 'Wikidata'}}})

    id: str = Field(default=..., description="""A unique identifier for a thing""", json_schema_extra = { "linkml_meta": {'alias': 'id',
         'domain_of': ['AuthorityResource'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 5} })
    category: Literal["https://av-efi.net/av-efi-schema/WikidataResource","avefi:WikidataResource"] = Field(default="avefi:WikidataResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""", json_schema_extra = { "linkml_meta": {'alias': 'category',
         'designates_type': True,
         'domain_of': ['CategorizedThing'],
         'in_subset': ['TypeRegistrySubset'],
         'rank': 1,
         'slot_uri': 'rdf:type'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
CategorizedThing.model_rebuild()
MovingImageRecord.model_rebuild()
DescriptionResource.model_rebuild()
WorkVariant.model_rebuild()
GeographicName.model_rebuild()
Genre.model_rebuild()
Subject.model_rebuild()
Activity.model_rebuild()
AnimationActivity.model_rebuild()
CastActivity.model_rebuild()
CensorshipActivity.model_rebuild()
CinematographyActivity.model_rebuild()
CopyrightAndDistributionActivity.model_rebuild()
DirectingActivity.model_rebuild()
EditingActivity.model_rebuild()
LaboratoryActivity.model_rebuild()
MusicActivity.model_rebuild()
ProducingActivity.model_rebuild()
ProductionDesignActivity.model_rebuild()
PuppetActivity.model_rebuild()
SoundActivity.model_rebuild()
SpecialEffectsActivity.model_rebuild()
WritingActivity.model_rebuild()
ManifestationActivity.model_rebuild()
Agent.model_rebuild()
Event.model_rebuild()
ProductionEvent.model_rebuild()
PreservationEvent.model_rebuild()
PublicationEvent.model_rebuild()
ManufactureEvent.model_rebuild()
RightsCopyrightRegistrationEvent.model_rebuild()
Title.model_rebuild()
ManifestationOrItem.model_rebuild()
Duration.model_rebuild()
Extent.model_rebuild()
Format.model_rebuild()
Audio.model_rebuild()
DigitalFile.model_rebuild()
DigitalFileEncoding.model_rebuild()
Film.model_rebuild()
Optical.model_rebuild()
Video.model_rebuild()
Manifestation.model_rebuild()
Language.model_rebuild()
Item.model_rebuild()
MovingImageRecordContainer.model_rebuild()
AuthorityResource.model_rebuild()
MovingImageResource.model_rebuild()
AVefiResource.model_rebuild()
DOIResource.model_rebuild()
EIDRResource.model_rebuild()
FilmportalResource.model_rebuild()
GNDResource.model_rebuild()
ISILResource.model_rebuild()
LocalResource.model_rebuild()
TGNResource.model_rebuild()
VIAFResource.model_rebuild()
WikidataResource.model_rebuild()
