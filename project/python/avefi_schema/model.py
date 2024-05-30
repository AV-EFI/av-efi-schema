# Auto generated from model.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-05-30T08:48:37
# Schema: model
#
# id: https://github.io/av-efi-schema/model
# description: Metadata schema for persistent film identifiers developed in the
#   AVefi project. See also the corresponding [Entity relation
#   diagram](https://github.com/AV-EFI/av-efi-schema/blob/main/avefi_er_diagram.md).
#   Additionally, consult the [FIAF Moving Image Cataloguing
#   Manual](https://www.fiafnet.org/pages/E-Resources/Cataloguing-Manual.html)
#   and the [FIAF Glossary of Filmographic
#   Terms](https://www.fiafnet.org/images/tinyUpload/E-Resources/Reports-Glossaries-And-Papers/GlossaryMasterCombo19.htm)
#   as indicated in the documentation below for definitions, usage
#   instructions and best practices
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from datetime import date, datetime
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Datetime, Decimal, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Decimal, URI, URIorCURIE, XSDDateTime

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
AVEFI = CurieNamespace('avefi', 'https://av-efi.net/av-efi-schema/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
FIAF = CurieNamespace('fiaf', 'https://fiafcore.org/ontology/')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
UNIT = CurieNamespace('unit', 'http://qudt.org/vocab/unit/')
WDRS = CurieNamespace('wdrs', 'http://www.w3.org/2007/05/powder-s#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = AVEFI


# Types

# Class references



@dataclass
class CategorizedThing(YAMLRoot):
    """
    Root for all classes with subclasses in this schema
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["CategorizedThing"]
    class_class_curie: ClassVar[str] = "avefi:CategorizedThing"
    class_name: ClassVar[str] = "CategorizedThing"
    class_model_uri: ClassVar[URIRef] = AVEFI.CategorizedThing

    category: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self.category = str(self.class_class_curie)

        super().__post_init__(**kwargs)


    def __new__(cls, *args, **kwargs):

        type_designator = "category"
        if not type_designator in kwargs:
            return super().__new__(cls,*args,**kwargs)
        else:
            type_designator_value = kwargs[type_designator]
            target_cls = cls._class_for("class_class_curie", type_designator_value)


            if target_cls is None:
                target_cls = cls._class_for("class_class_uri", type_designator_value)


            if target_cls is None:
                target_cls = cls._class_for("class_model_uri", type_designator_value)


            if target_cls is None:
                raise ValueError(f"Wrong type designator value: class {cls.__name__} "
                                 f"has no subclass with ['class_class_curie', 'class_class_uri', 'class_model_uri']='{kwargs[type_designator]}'")
            return super().__new__(target_cls,*args,**kwargs)



@dataclass
class PIDRecord(CategorizedThing):
    """
    Grouping for all entities that represent a PID metadata record
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["PIDRecord"]
    class_class_curie: ClassVar[str] = "avefi:PIDRecord"
    class_name: ClassVar[str] = "PIDRecord"
    class_model_uri: ClassVar[URIRef] = AVEFI.PIDRecord

    id: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.id is not None and not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class MovingImageRecord(PIDRecord):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["MovingImageRecord"]
    class_class_curie: ClassVar[str] = "avefi:MovingImageRecord"
    class_name: ClassVar[str] = "MovingImageRecord"
    class_model_uri: ClassVar[URIRef] = AVEFI.MovingImageRecord

    has_primary_title: Union[dict, "Title"] = None
    described_by: Optional[Union[dict, "DescriptionResource"]] = None
    has_event: Optional[Union[Union[dict, "Event"], List[Union[dict, "Event"]]]] = empty_list()
    in_language: Optional[Union[Union[dict, "Language"], List[Union[dict, "Language"]]]] = empty_list()
    has_alternative_title: Optional[Union[Union[dict, "Title"], List[Union[dict, "Title"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_primary_title):
            self.MissingRequiredField("has_primary_title")
        if not isinstance(self.has_primary_title, Title):
            self.has_primary_title = Title(**as_dict(self.has_primary_title))

        if self.described_by is not None and not isinstance(self.described_by, DescriptionResource):
            self.described_by = DescriptionResource(**as_dict(self.described_by))

        if not isinstance(self.has_event, list):
            self.has_event = [self.has_event] if self.has_event is not None else []
        self.has_event = [v if isinstance(v, Event) else Event(**as_dict(v)) for v in self.has_event]

        if not isinstance(self.in_language, list):
            self.in_language = [self.in_language] if self.in_language is not None else []
        self.in_language = [v if isinstance(v, Language) else Language(**as_dict(v)) for v in self.in_language]

        if not isinstance(self.has_alternative_title, list):
            self.has_alternative_title = [self.has_alternative_title] if self.has_alternative_title is not None else []
        self.has_alternative_title = [v if isinstance(v, Title) else Title(**as_dict(v)) for v in self.has_alternative_title]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class DescriptionResource(YAMLRoot):
    """
    Metadata about the PID rather than the identified object, i.e. who modified the PID metadata record when, making
    what changes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["DescriptionResource"]
    class_class_curie: ClassVar[str] = "avefi:DescriptionResource"
    class_name: ClassVar[str] = "DescriptionResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.DescriptionResource

    has_issuer_id: Union[str, URI] = None
    has_issuer_name: str = None
    last_modified: Union[str, XSDDateTime] = None
    has_history: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_issuer_id):
            self.MissingRequiredField("has_issuer_id")
        if not isinstance(self.has_issuer_id, URI):
            self.has_issuer_id = URI(self.has_issuer_id)

        if self._is_empty(self.has_issuer_name):
            self.MissingRequiredField("has_issuer_name")
        if not isinstance(self.has_issuer_name, str):
            self.has_issuer_name = str(self.has_issuer_name)

        if self._is_empty(self.last_modified):
            self.MissingRequiredField("last_modified")
        if not isinstance(self.last_modified, XSDDateTime):
            self.last_modified = XSDDateTime(self.last_modified)

        if self.has_history is not None and not isinstance(self.has_history, URI):
            self.has_history = URI(self.has_history)

        super().__post_init__(**kwargs)


@dataclass
class WorkVariant(MovingImageRecord):
    """
    FIAF Moving Image Cataloguing Manual 1.0
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["WorkVariant"]
    class_class_curie: ClassVar[str] = "avefi:WorkVariant"
    class_name: ClassVar[str] = "WorkVariant"
    class_model_uri: ClassVar[URIRef] = AVEFI.WorkVariant

    has_primary_title: Union[dict, "Title"] = None
    type: Union[str, "WorkVariantTypeEnum"] = None
    has_form: Optional[Union[Union[str, "WorkFormEnum"], List[Union[str, "WorkFormEnum"]]]] = empty_list()
    has_genre: Optional[Union[Union[dict, "Genre"], List[Union[dict, "Genre"]]]] = empty_list()
    has_subject: Optional[Union[Union[dict, "Subject"], List[Union[dict, "Subject"]]]] = empty_list()
    is_part_of: Optional[Union[Union[dict, "AVefiResource"], List[Union[dict, "AVefiResource"]]]] = empty_list()
    is_variant_of: Optional[Union[dict, "AVefiResource"]] = None
    same_as: Optional[Union[Union[dict, "AuthorityResource"], List[Union[dict, "AuthorityResource"]]]] = empty_list()
    variant_type: Optional[Union[str, "VariantTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, WorkVariantTypeEnum):
            self.type = WorkVariantTypeEnum(self.type)

        if not isinstance(self.has_form, list):
            self.has_form = [self.has_form] if self.has_form is not None else []
        self.has_form = [v if isinstance(v, WorkFormEnum) else WorkFormEnum(v) for v in self.has_form]

        if not isinstance(self.has_genre, list):
            self.has_genre = [self.has_genre] if self.has_genre is not None else []
        self.has_genre = [v if isinstance(v, Genre) else Genre(**as_dict(v)) for v in self.has_genre]

        if not isinstance(self.has_subject, list):
            self.has_subject = [self.has_subject] if self.has_subject is not None else []
        self.has_subject = [v if isinstance(v, Subject) else Subject(**as_dict(v)) for v in self.has_subject]

        if not isinstance(self.is_part_of, list):
            self.is_part_of = [self.is_part_of] if self.is_part_of is not None else []
        self.is_part_of = [v if isinstance(v, AVefiResource) else AVefiResource(**as_dict(v)) for v in self.is_part_of]

        if self.is_variant_of is not None and not isinstance(self.is_variant_of, AVefiResource):
            self.is_variant_of = AVefiResource(**as_dict(self.is_variant_of))

        if not isinstance(self.same_as, list):
            self.same_as = [self.same_as] if self.same_as is not None else []
        self.same_as = [v if isinstance(v, AuthorityResource) else AuthorityResource(**as_dict(v)) for v in self.same_as]

        if self.variant_type is not None and not isinstance(self.variant_type, VariantTypeEnum):
            self.variant_type = VariantTypeEnum(self.variant_type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class GeographicName(YAMLRoot):
    """
    Name of country, region or other location. Names should be taken from appropriate authorities (e.g. GND) and
    recorded as a human readable string in the name attribute and as linked data in the same_as attribute. See also:
    FIAF Moving Image Cataloguing Manual 1.3.3, D.4
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["GeographicName"]
    class_class_curie: ClassVar[str] = "avefi:GeographicName"
    class_name: ClassVar[str] = "GeographicName"
    class_model_uri: ClassVar[URIRef] = AVEFI.GeographicName

    has_name: str = None
    has_alternate_name: Optional[Union[str, List[str]]] = empty_list()
    same_as: Optional[Union[Union[dict, "AuthorityResource"], List[Union[dict, "AuthorityResource"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_name):
            self.MissingRequiredField("has_name")
        if not isinstance(self.has_name, str):
            self.has_name = str(self.has_name)

        if not isinstance(self.has_alternate_name, list):
            self.has_alternate_name = [self.has_alternate_name] if self.has_alternate_name is not None else []
        self.has_alternate_name = [v if isinstance(v, str) else str(v) for v in self.has_alternate_name]

        if not isinstance(self.same_as, list):
            self.same_as = [self.same_as] if self.same_as is not None else []
        self.same_as = [v if isinstance(v, AuthorityResource) else AuthorityResource(**as_dict(v)) for v in self.same_as]

        super().__post_init__(**kwargs)


@dataclass
class Genre(YAMLRoot):
    """
    Genre describes categories of Works, characterized by similar plots, themes, settings, situations, and characters.
    Examples of genres are “westerns” and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF
    Glossary of Filmographic Terms D.2.1
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Genre"]
    class_class_curie: ClassVar[str] = "avefi:Genre"
    class_name: ClassVar[str] = "Genre"
    class_model_uri: ClassVar[URIRef] = AVEFI.Genre

    has_name: str = None
    has_alternate_name: Optional[Union[str, List[str]]] = empty_list()
    same_as: Optional[Union[Union[dict, "GNDResource"], List[Union[dict, "GNDResource"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_name):
            self.MissingRequiredField("has_name")
        if not isinstance(self.has_name, str):
            self.has_name = str(self.has_name)

        if not isinstance(self.has_alternate_name, list):
            self.has_alternate_name = [self.has_alternate_name] if self.has_alternate_name is not None else []
        self.has_alternate_name = [v if isinstance(v, str) else str(v) for v in self.has_alternate_name]

        if not isinstance(self.same_as, list):
            self.same_as = [self.same_as] if self.same_as is not None else []
        self.same_as = [v if isinstance(v, GNDResource) else GNDResource(**as_dict(v)) for v in self.same_as]

        super().__post_init__(**kwargs)


@dataclass
class Subject(YAMLRoot):
    """
    Subject descriptor terms for the content of a film specifying its period, themes, locations, etc. Not to be
    confused with Genre. Provide name and if at all possible identifier(s) from supported authorities in the same_as
    slot. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.3
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Subject"]
    class_class_curie: ClassVar[str] = "avefi:Subject"
    class_name: ClassVar[str] = "Subject"
    class_model_uri: ClassVar[URIRef] = AVEFI.Subject

    has_name: str = None
    has_alternate_name: Optional[Union[str, List[str]]] = empty_list()
    same_as: Optional[Union[Union[dict, "AuthorityResource"], List[Union[dict, "AuthorityResource"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_name):
            self.MissingRequiredField("has_name")
        if not isinstance(self.has_name, str):
            self.has_name = str(self.has_name)

        if not isinstance(self.has_alternate_name, list):
            self.has_alternate_name = [self.has_alternate_name] if self.has_alternate_name is not None else []
        self.has_alternate_name = [v if isinstance(v, str) else str(v) for v in self.has_alternate_name]

        if not isinstance(self.same_as, list):
            self.same_as = [self.same_as] if self.same_as is not None else []
        self.same_as = [v if isinstance(v, AuthorityResource) else AuthorityResource(**as_dict(v)) for v in self.same_as]

        super().__post_init__(**kwargs)


@dataclass
class Activity(CategorizedThing):
    """
    FIAF Moving Image Cataloguing Manual 1.4.1.1
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Activity"]
    class_class_curie: ClassVar[str] = "avefi:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = AVEFI.Activity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_agent):
            self.MissingRequiredField("has_agent")
        if not isinstance(self.has_agent, list):
            self.has_agent = [self.has_agent] if self.has_agent is not None else []
        self.has_agent = [v if isinstance(v, Agent) else Agent(**as_dict(v)) for v in self.has_agent]

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class AnimationActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.13
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["AnimationActivity"]
    class_class_curie: ClassVar[str] = "avefi:AnimationActivity"
    class_name: ClassVar[str] = "AnimationActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.AnimationActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "AnimationActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, AnimationActivityTypeEnum):
            self.type = AnimationActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class CastActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.7
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["CastActivity"]
    class_class_curie: ClassVar[str] = "avefi:CastActivity"
    class_name: ClassVar[str] = "CastActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.CastActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "CastActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, CastActivityTypeEnum):
            self.type = CastActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class CensorshipActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.1
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["CensorshipActivity"]
    class_class_curie: ClassVar[str] = "avefi:CensorshipActivity"
    class_name: ClassVar[str] = "CensorshipActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.CensorshipActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "CensorshipActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, CensorshipActivityTypeEnum):
            self.type = CensorshipActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class CinematographyActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.5
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["CinematographyActivity"]
    class_class_curie: ClassVar[str] = "avefi:CinematographyActivity"
    class_name: ClassVar[str] = "CinematographyActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.CinematographyActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "CinematographyActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, CinematographyActivityTypeEnum):
            self.type = CinematographyActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class CopyrightAndDistributionActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["CopyrightAndDistributionActivity"]
    class_class_curie: ClassVar[str] = "avefi:CopyrightAndDistributionActivity"
    class_name: ClassVar[str] = "CopyrightAndDistributionActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.CopyrightAndDistributionActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "CopyrightAndDistributionActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, CopyrightAndDistributionActivityTypeEnum):
            self.type = CopyrightAndDistributionActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class DirectingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.3
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["DirectingActivity"]
    class_class_curie: ClassVar[str] = "avefi:DirectingActivity"
    class_name: ClassVar[str] = "DirectingActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.DirectingActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "DirectingActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, DirectingActivityTypeEnum):
            self.type = DirectingActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class EditingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.10
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["EditingActivity"]
    class_class_curie: ClassVar[str] = "avefi:EditingActivity"
    class_name: ClassVar[str] = "EditingActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.EditingActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "EditingActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, EditingActivityTypeEnum):
            self.type = EditingActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class LaboratoryActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.12
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["LaboratoryActivity"]
    class_class_curie: ClassVar[str] = "avefi:LaboratoryActivity"
    class_name: ClassVar[str] = "LaboratoryActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.LaboratoryActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "LaboratoryActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, LaboratoryActivityTypeEnum):
            self.type = LaboratoryActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class MusicActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.11
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["MusicActivity"]
    class_class_curie: ClassVar[str] = "avefi:MusicActivity"
    class_name: ClassVar[str] = "MusicActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.MusicActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "MusicActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, MusicActivityTypeEnum):
            self.type = MusicActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class ProducingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["ProducingActivity"]
    class_class_curie: ClassVar[str] = "avefi:ProducingActivity"
    class_name: ClassVar[str] = "ProducingActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.ProducingActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "ProducingActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, ProducingActivityTypeEnum):
            self.type = ProducingActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class ProductionDesignActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.6
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["ProductionDesignActivity"]
    class_class_curie: ClassVar[str] = "avefi:ProductionDesignActivity"
    class_name: ClassVar[str] = "ProductionDesignActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.ProductionDesignActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "ProductionDesignActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, ProductionDesignActivityTypeEnum):
            self.type = ProductionDesignActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class PuppetActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.14
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["PuppetActivity"]
    class_class_curie: ClassVar[str] = "avefi:PuppetActivity"
    class_name: ClassVar[str] = "PuppetActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.PuppetActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "PuppetActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, PuppetActivityTypeEnum):
            self.type = PuppetActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class SoundActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.9
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["SoundActivity"]
    class_class_curie: ClassVar[str] = "avefi:SoundActivity"
    class_name: ClassVar[str] = "SoundActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.SoundActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "SoundActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, SoundActivityTypeEnum):
            self.type = SoundActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class SpecialEffectsActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.8
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["SpecialEffectsActivity"]
    class_class_curie: ClassVar[str] = "avefi:SpecialEffectsActivity"
    class_name: ClassVar[str] = "SpecialEffectsActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.SpecialEffectsActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "SpecialEffectsActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, SpecialEffectsActivityTypeEnum):
            self.type = SpecialEffectsActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class WritingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.4
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["WritingActivity"]
    class_class_curie: ClassVar[str] = "avefi:WritingActivity"
    class_name: ClassVar[str] = "WritingActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.WritingActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "WritingActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, WritingActivityTypeEnum):
            self.type = WritingActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class ManifestationActivity(Activity):
    """
    Activity types / roles. See also: FIAF Moving Image Cataloguing Manual 2.4.1.1, D.8
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["ManifestationActivity"]
    class_class_curie: ClassVar[str] = "avefi:ManifestationActivity"
    class_name: ClassVar[str] = "ManifestationActivity"
    class_model_uri: ClassVar[URIRef] = AVEFI.ManifestationActivity

    has_agent: Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]] = None
    type: Union[str, "ManifestationActivityTypeEnum"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, ManifestationActivityTypeEnum):
            self.type = ManifestationActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Agent(YAMLRoot):
    """
    Agent involved in some activity related to the moving image resource. For agents of type "Person" specify name
    according to the convention "family name, given name"
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Agent"]
    class_class_curie: ClassVar[str] = "avefi:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = AVEFI.Agent

    has_name: str = None
    type: Union[str, "AgentTypeEnum"] = None
    has_alternate_name: Optional[Union[str, List[str]]] = empty_list()
    same_as: Optional[Union[Union[dict, "AuthorityResource"], List[Union[dict, "AuthorityResource"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_name):
            self.MissingRequiredField("has_name")
        if not isinstance(self.has_name, str):
            self.has_name = str(self.has_name)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, AgentTypeEnum):
            self.type = AgentTypeEnum(self.type)

        if not isinstance(self.has_alternate_name, list):
            self.has_alternate_name = [self.has_alternate_name] if self.has_alternate_name is not None else []
        self.has_alternate_name = [v if isinstance(v, str) else str(v) for v in self.has_alternate_name]

        if not isinstance(self.same_as, list):
            self.same_as = [self.same_as] if self.same_as is not None else []
        self.same_as = [v if isinstance(v, AuthorityResource) else AuthorityResource(**as_dict(v)) for v in self.same_as]

        super().__post_init__(**kwargs)


@dataclass
class Event(CategorizedThing):
    """
    Significant event in the lifecycle of moving image work / variant, manifestation or item. Always specify the type
    of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the
    country where the principal offices or production facilities of the production company are located for a
    production event. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image
    Cataloguing Manual 1.4.2, 2.4.2, 3.3.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Event"]
    class_class_curie: ClassVar[str] = "avefi:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = AVEFI.Event

    has_activity: Optional[Union[Union[dict, Activity], List[Union[dict, Activity]]]] = empty_list()
    has_date: Optional[str] = None
    located_in: Optional[Union[Union[dict, GeographicName], List[Union[dict, GeographicName]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_activity, list):
            self.has_activity = [self.has_activity] if self.has_activity is not None else []
        self.has_activity = [v if isinstance(v, Activity) else Activity(**as_dict(v)) for v in self.has_activity]

        if self.has_date is not None and not isinstance(self.has_date, str):
            self.has_date = str(self.has_date)

        if not isinstance(self.located_in, list):
            self.located_in = [self.located_in] if self.located_in is not None else []
        self.located_in = [v if isinstance(v, GeographicName) else GeographicName(**as_dict(v)) for v in self.located_in]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class ProductionEvent(Event):
    """
    Production event of a work/variant (or manifestation produced as a restoration). Provide a date or a period of
    time via has_date and specify located_in as appropriate, e.g. the country where the principal offices or
    production facilities of the production company are located. Involved parties in various roles can be linked via
    has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.3
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["ProductionEvent"]
    class_class_curie: ClassVar[str] = "avefi:ProductionEvent"
    class_name: ClassVar[str] = "ProductionEvent"
    class_model_uri: ClassVar[URIRef] = AVEFI.ProductionEvent

    type: Optional[Union[str, "ProductionEventTypeEnum"]] = None
    has_activity: Optional[Union[Union[dict, Activity], List[Union[dict, Activity]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, ProductionEventTypeEnum):
            self.type = ProductionEventTypeEnum(self.type)

        if not isinstance(self.has_activity, list):
            self.has_activity = [self.has_activity] if self.has_activity is not None else []
        self.has_activity = [v if isinstance(v, Activity) else Activity(**as_dict(v)) for v in self.has_activity]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class PreservationEvent(Event):
    """
    Preservation event originating a manifestation or possibly a vaniant. Always specify the type of event and if
    possible a date or a period of time via has_date. Specify located_in as appropriate. Involved parties in various
    roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.5
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["PreservationEvent"]
    class_class_curie: ClassVar[str] = "avefi:PreservationEvent"
    class_name: ClassVar[str] = "PreservationEvent"
    class_model_uri: ClassVar[URIRef] = AVEFI.PreservationEvent

    type: Union[str, "PreservationEventTypeEnum"] = None
    has_activity: Union[Union[dict, ManifestationActivity], List[Union[dict, ManifestationActivity]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, PreservationEventTypeEnum):
            self.type = PreservationEventTypeEnum(self.type)

        if self._is_empty(self.has_activity):
            self.MissingRequiredField("has_activity")
        if not isinstance(self.has_activity, list):
            self.has_activity = [self.has_activity] if self.has_activity is not None else []
        self.has_activity = [v if isinstance(v, ManifestationActivity) else ManifestationActivity(**as_dict(v)) for v in self.has_activity]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class PublicationEvent(Event):
    """
    Publication event of a manifestation or possibly the first known publication of a work. Always specify the type of
    event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country
    where the manifestation was published. Involved parties in various roles can be linked via has_activity. See also:
    FIAF Moving Image Cataloguing Manual D.4.1
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["PublicationEvent"]
    class_class_curie: ClassVar[str] = "avefi:PublicationEvent"
    class_name: ClassVar[str] = "PublicationEvent"
    class_model_uri: ClassVar[URIRef] = AVEFI.PublicationEvent

    type: Union[str, "PublicationEventTypeEnum"] = None
    has_activity: Optional[Union[Union[dict, ManifestationActivity], List[Union[dict, ManifestationActivity]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, PublicationEventTypeEnum):
            self.type = PublicationEventTypeEnum(self.type)

        if not isinstance(self.has_activity, list):
            self.has_activity = [self.has_activity] if self.has_activity is not None else []
        self.has_activity = [v if isinstance(v, ManifestationActivity) else ManifestationActivity(**as_dict(v)) for v in self.has_activity]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class ManufactureEvent(Event):
    """
    Manufacture event of a manifestation. Always specify the type of event and if possible a date or a period of time
    via has_date. Specify located_in as appropriate, e.g. the country where the labratory is located. Involved parties
    in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.7
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["ManufactureEvent"]
    class_class_curie: ClassVar[str] = "avefi:ManufactureEvent"
    class_name: ClassVar[str] = "ManufactureEvent"
    class_model_uri: ClassVar[URIRef] = AVEFI.ManufactureEvent

    type: Union[str, "ManufactureEventTypeEnum"] = None
    has_activity: Union[Union[dict, LaboratoryActivity], List[Union[dict, LaboratoryActivity]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, ManufactureEventTypeEnum):
            self.type = ManufactureEventTypeEnum(self.type)

        if self._is_empty(self.has_activity):
            self.MissingRequiredField("has_activity")
        if not isinstance(self.has_activity, list):
            self.has_activity = [self.has_activity] if self.has_activity is not None else []
        self.has_activity = [v if isinstance(v, LaboratoryActivity) else LaboratoryActivity(**as_dict(v)) for v in self.has_activity]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class RightsCopyrightRegistrationEvent(Event):
    """
    Copyright and related rights registration event of a manifestation or possibly of a work/variant. Always specify
    date via has_date. Specify located_in as appropriate, e.g. the country where the copyright was registered.
    Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual
    D.4.4
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["RightsCopyrightRegistrationEvent"]
    class_class_curie: ClassVar[str] = "avefi:RightsCopyrightRegistrationEvent"
    class_name: ClassVar[str] = "RightsCopyrightRegistrationEvent"
    class_model_uri: ClassVar[URIRef] = AVEFI.RightsCopyrightRegistrationEvent

    has_activity: Union[Union[dict, CopyrightAndDistributionActivity], List[Union[dict, CopyrightAndDistributionActivity]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_activity):
            self.MissingRequiredField("has_activity")
        if not isinstance(self.has_activity, list):
            self.has_activity = [self.has_activity] if self.has_activity is not None else []
        self.has_activity = [v if isinstance(v, CopyrightAndDistributionActivity) else CopyrightAndDistributionActivity(**as_dict(v)) for v in self.has_activity]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Title(YAMLRoot):
    """
    FIAF Moving Image Cataloguing Manual 1.3.2, 2.3.2, 3.1.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Title"]
    class_class_curie: ClassVar[str] = "avefi:Title"
    class_name: ClassVar[str] = "Title"
    class_model_uri: ClassVar[URIRef] = AVEFI.Title

    has_name: str = None
    type: Union[str, "TitleTypeEnum"] = None
    has_ordering_name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_name):
            self.MissingRequiredField("has_name")
        if not isinstance(self.has_name, str):
            self.has_name = str(self.has_name)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, TitleTypeEnum):
            self.type = TitleTypeEnum(self.type)

        if self.has_ordering_name is not None and not isinstance(self.has_ordering_name, str):
            self.has_ordering_name = str(self.has_ordering_name)

        super().__post_init__(**kwargs)


@dataclass
class ManifestationOrItem(MovingImageRecord):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["ManifestationOrItem"]
    class_class_curie: ClassVar[str] = "avefi:ManifestationOrItem"
    class_name: ClassVar[str] = "ManifestationOrItem"
    class_model_uri: ClassVar[URIRef] = AVEFI.ManifestationOrItem

    has_primary_title: Union[dict, Title] = None
    has_duration: Optional[Union[dict, "Duration"]] = None
    has_extent: Optional[Union[dict, "Extent"]] = None
    has_format: Optional[Union[Union[dict, "Format"], List[Union[dict, "Format"]]]] = empty_list()
    has_note: Optional[Union[str, List[str]]] = empty_list()
    has_webresource: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_duration is not None and not isinstance(self.has_duration, Duration):
            self.has_duration = Duration(**as_dict(self.has_duration))

        if self.has_extent is not None and not isinstance(self.has_extent, Extent):
            self.has_extent = Extent(**as_dict(self.has_extent))

        if not isinstance(self.has_format, list):
            self.has_format = [self.has_format] if self.has_format is not None else []
        self.has_format = [v if isinstance(v, Format) else Format(**as_dict(v)) for v in self.has_format]

        if not isinstance(self.has_note, list):
            self.has_note = [self.has_note] if self.has_note is not None else []
        self.has_note = [v if isinstance(v, str) else str(v) for v in self.has_note]

        if self.has_webresource is not None and not isinstance(self.has_webresource, URI):
            self.has_webresource = URI(self.has_webresource)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Duration(YAMLRoot):
    """
    Total running time of the described object in ISO 8601 duration format. The examples section lists possible values
    for the has_value slot. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Duration"]
    class_class_curie: ClassVar[str] = "avefi:Duration"
    class_name: ClassVar[str] = "Duration"
    class_model_uri: ClassVar[URIRef] = AVEFI.Duration

    has_value: Optional[str] = None
    has_precision: Optional[Union[str, "PrecisionEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_value is not None and not isinstance(self.has_value, str):
            self.has_value = str(self.has_value)

        if self.has_precision is not None and not isinstance(self.has_precision, PrecisionEnum):
            self.has_precision = PrecisionEnum(self.has_precision)

        super().__post_init__(**kwargs)


@dataclass
class Extent(YAMLRoot):
    """
    Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Extent"]
    class_class_curie: ClassVar[str] = "avefi:Extent"
    class_name: ClassVar[str] = "Extent"
    class_model_uri: ClassVar[URIRef] = AVEFI.Extent

    has_unit: Optional[Union[str, "UnitEnum"]] = None
    has_value: Optional[Decimal] = None
    has_precision: Optional[Union[str, "PrecisionEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_unit is not None and not isinstance(self.has_unit, UnitEnum):
            self.has_unit = UnitEnum(self.has_unit)

        if self.has_value is not None and not isinstance(self.has_value, Decimal):
            self.has_value = Decimal(self.has_value)

        if self.has_precision is not None and not isinstance(self.has_precision, PrecisionEnum):
            self.has_precision = PrecisionEnum(self.has_precision)

        super().__post_init__(**kwargs)


@dataclass
class Format(CategorizedThing):
    """
    FIAF Moving Image Cataloguing Manual 2.3.4.1, 3.1.5.1
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Format"]
    class_class_curie: ClassVar[str] = "avefi:Format"
    class_name: ClassVar[str] = "Format"
    class_model_uri: ClassVar[URIRef] = AVEFI.Format

    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Audio(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Audio"]
    class_class_curie: ClassVar[str] = "avefi:Audio"
    class_name: ClassVar[str] = "Audio"
    class_model_uri: ClassVar[URIRef] = AVEFI.Audio

    type: Optional[Union[str, "FormatAudioTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, FormatAudioTypeEnum):
            self.type = FormatAudioTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class DigitalFile(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["DigitalFile"]
    class_class_curie: ClassVar[str] = "avefi:DigitalFile"
    class_name: ClassVar[str] = "DigitalFile"
    class_model_uri: ClassVar[URIRef] = AVEFI.DigitalFile

    type: Optional[Union[str, "FormatDigitalFileTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, FormatDigitalFileTypeEnum):
            self.type = FormatDigitalFileTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class DigitalFileEncoding(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["DigitalFileEncoding"]
    class_class_curie: ClassVar[str] = "avefi:DigitalFileEncoding"
    class_name: ClassVar[str] = "DigitalFileEncoding"
    class_model_uri: ClassVar[URIRef] = AVEFI.DigitalFileEncoding

    type: Optional[Union[str, "FormatDigitalFileEncodingTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, FormatDigitalFileEncodingTypeEnum):
            self.type = FormatDigitalFileEncodingTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Film(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Film"]
    class_class_curie: ClassVar[str] = "avefi:Film"
    class_name: ClassVar[str] = "Film"
    class_model_uri: ClassVar[URIRef] = AVEFI.Film

    type: Optional[Union[str, "FormatFilmTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, FormatFilmTypeEnum):
            self.type = FormatFilmTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Optical(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Optical"]
    class_class_curie: ClassVar[str] = "avefi:Optical"
    class_name: ClassVar[str] = "Optical"
    class_model_uri: ClassVar[URIRef] = AVEFI.Optical

    type: Optional[Union[str, "FormatOpticalTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, FormatOpticalTypeEnum):
            self.type = FormatOpticalTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Video(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Video"]
    class_class_curie: ClassVar[str] = "avefi:Video"
    class_name: ClassVar[str] = "Video"
    class_model_uri: ClassVar[URIRef] = AVEFI.Video

    type: Optional[Union[str, "FormatVideoTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, FormatVideoTypeEnum):
            self.type = FormatVideoTypeEnum(self.type)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Manifestation(ManifestationOrItem):
    """
    Manifestation as defined in FIAF Moving Image Cataloguing Manual 2.0. Note that manifestation type is recorded as
    publication event type
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Manifestation"]
    class_class_curie: ClassVar[str] = "avefi:Manifestation"
    class_name: ClassVar[str] = "Manifestation"
    class_model_uri: ClassVar[URIRef] = AVEFI.Manifestation

    has_primary_title: Union[dict, Title] = None
    is_manifestation_of: Union[Union[dict, "AVefiResource"], List[Union[dict, "AVefiResource"]]] = None
    has_colour_type: Optional[Union[str, "ColourTypeEnum"]] = None
    has_item: Optional[Union[Union[dict, "AVefiResource"], List[Union[dict, "AVefiResource"]]]] = empty_list()
    has_sound_type: Optional[Union[str, "SoundTypeEnum"]] = None
    same_as: Optional[Union[Union[dict, "AVefiResource"], List[Union[dict, "AVefiResource"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.is_manifestation_of):
            self.MissingRequiredField("is_manifestation_of")
        if not isinstance(self.is_manifestation_of, list):
            self.is_manifestation_of = [self.is_manifestation_of] if self.is_manifestation_of is not None else []
        self.is_manifestation_of = [v if isinstance(v, AVefiResource) else AVefiResource(**as_dict(v)) for v in self.is_manifestation_of]

        if self.has_colour_type is not None and not isinstance(self.has_colour_type, ColourTypeEnum):
            self.has_colour_type = ColourTypeEnum(self.has_colour_type)

        if not isinstance(self.has_item, list):
            self.has_item = [self.has_item] if self.has_item is not None else []
        self.has_item = [v if isinstance(v, AVefiResource) else AVefiResource(**as_dict(v)) for v in self.has_item]

        if self.has_sound_type is not None and not isinstance(self.has_sound_type, SoundTypeEnum):
            self.has_sound_type = SoundTypeEnum(self.has_sound_type)

        if not isinstance(self.same_as, list):
            self.same_as = [self.same_as] if self.same_as is not None else []
        self.same_as = [v if isinstance(v, AVefiResource) else AVefiResource(**as_dict(v)) for v in self.same_as]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class Language(YAMLRoot):
    """
    Provide language code from ISO 639-2 (Part 2: Alpha-3) and a list of language usage terms from our controlled
    vocabulary. See also: FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Language"]
    class_class_curie: ClassVar[str] = "avefi:Language"
    class_name: ClassVar[str] = "Language"
    class_model_uri: ClassVar[URIRef] = AVEFI.Language

    code: str = None
    usage: Union[Union[str, "LanguageUsageEnum"], List[Union[str, "LanguageUsageEnum"]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.code):
            self.MissingRequiredField("code")
        if not isinstance(self.code, str):
            self.code = str(self.code)

        if self._is_empty(self.usage):
            self.MissingRequiredField("usage")
        if not isinstance(self.usage, list):
            self.usage = [self.usage] if self.usage is not None else []
        self.usage = [v if isinstance(v, LanguageUsageEnum) else LanguageUsageEnum(v) for v in self.usage]

        super().__post_init__(**kwargs)


@dataclass
class Item(ManifestationOrItem):
    """
    FIAF Moving Image Cataloguing Manual 3.0
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["Item"]
    class_class_curie: ClassVar[str] = "avefi:Item"
    class_name: ClassVar[str] = "Item"
    class_model_uri: ClassVar[URIRef] = AVEFI.Item

    has_primary_title: Union[dict, Title] = None
    is_item_of: Union[dict, "AVefiResource"] = None
    element_type: Optional[Union[str, "ItemElementTypeEnum"]] = None
    has_access_status: Optional[Union[str, "ItemAccessStatusEnum"]] = None
    is_copy_of: Optional[Union[Union[dict, "AVefiResource"], List[Union[dict, "AVefiResource"]]]] = empty_list()
    is_derivative_of: Optional[Union[Union[dict, "AVefiResource"], List[Union[dict, "AVefiResource"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.is_item_of):
            self.MissingRequiredField("is_item_of")
        if not isinstance(self.is_item_of, AVefiResource):
            self.is_item_of = AVefiResource(**as_dict(self.is_item_of))

        if self.element_type is not None and not isinstance(self.element_type, ItemElementTypeEnum):
            self.element_type = ItemElementTypeEnum(self.element_type)

        if self.has_access_status is not None and not isinstance(self.has_access_status, ItemAccessStatusEnum):
            self.has_access_status = ItemAccessStatusEnum(self.has_access_status)

        if not isinstance(self.is_copy_of, list):
            self.is_copy_of = [self.is_copy_of] if self.is_copy_of is not None else []
        self.is_copy_of = [v if isinstance(v, AVefiResource) else AVefiResource(**as_dict(v)) for v in self.is_copy_of]

        if not isinstance(self.is_derivative_of, list):
            self.is_derivative_of = [self.is_derivative_of] if self.is_derivative_of is not None else []
        self.is_derivative_of = [v if isinstance(v, AVefiResource) else AVefiResource(**as_dict(v)) for v in self.is_derivative_of]

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class MovingImageRecordContainer(YAMLRoot):
    """
    A holder for MovingImageRecord objects
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["MovingImageRecordContainer"]
    class_class_curie: ClassVar[str] = "avefi:MovingImageRecordContainer"
    class_name: ClassVar[str] = "MovingImageRecordContainer"
    class_model_uri: ClassVar[URIRef] = AVEFI.MovingImageRecordContainer

    has_record: Optional[Union[dict, MovingImageRecord]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_record is not None and not isinstance(self.has_record, MovingImageRecord):
            self.has_record = MovingImageRecord(**as_dict(self.has_record))

        super().__post_init__(**kwargs)


@dataclass
class AuthorityResource(CategorizedThing):
    """
    Root class for all identifiers from some kind of authority or public register widely accepted in the community
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["AuthorityResource"]
    class_class_curie: ClassVar[str] = "avefi:AuthorityResource"
    class_name: ClassVar[str] = "AuthorityResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.AuthorityResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class AVefiResource(AuthorityResource):
    """
    Handle with the prefix allocated for AVefi (eventually)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["AVefiResource"]
    class_class_curie: ClassVar[str] = "avefi:AVefiResource"
    class_name: ClassVar[str] = "AVefiResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.AVefiResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class DOIResource(AuthorityResource):
    """
    Digital Object Identifier maintained by the DOI Foundation and commonly used for scientific publications including
    films.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["DOIResource"]
    class_class_curie: ClassVar[str] = "avefi:DOIResource"
    class_name: ClassVar[str] = "DOIResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.DOIResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class FilmportalResource(AuthorityResource):
    """
    Identifier of the German Filmportal.de
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["FilmportalResource"]
    class_class_curie: ClassVar[str] = "avefi:FilmportalResource"
    class_name: ClassVar[str] = "FilmportalResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.FilmportalResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class GNDResource(AuthorityResource):
    """
    Gemeinsame Normdatei (GND) identifier maintained by Deutsche Nationalbibliothek (German National Library)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["GNDResource"]
    class_class_curie: ClassVar[str] = "avefi:GNDResource"
    class_name: ClassVar[str] = "GNDResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.GNDResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class ISILResource(AuthorityResource):
    """
    International Standard Identifier for Libraries and Related Organizations including (film) archives
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["ISILResource"]
    class_class_curie: ClassVar[str] = "avefi:ISILResource"
    class_name: ClassVar[str] = "ISILResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.ISILResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class TGNResource(AuthorityResource):
    """
    Getty Thesaurus of Geographic Names ID
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["TGNResource"]
    class_class_curie: ClassVar[str] = "avefi:TGNResource"
    class_name: ClassVar[str] = "TGNResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.TGNResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class VIAFResource(AuthorityResource):
    """
    Virtual International Authority File identifier hosted by OCLC. The data is accumulated from various well
    established authority files from different parts of the world
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["VIAFResource"]
    class_class_curie: ClassVar[str] = "avefi:VIAFResource"
    class_name: ClassVar[str] = "VIAFResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.VIAFResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


@dataclass
class WikidataResource(AuthorityResource):
    """
    Identifier for Wikidata entities
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = AVEFI["WikidataResource"]
    class_class_curie: ClassVar[str] = "avefi:WikidataResource"
    class_name: ClassVar[str] = "WikidataResource"
    class_model_uri: ClassVar[URIRef] = AVEFI.WikidataResource

    id: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, str):
            self.id = str(self.id)

        super().__post_init__(**kwargs)
        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        self.category = str(self.class_class_curie)


# Enumerations
class AnimationActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.13
    """
    Animation = PermissibleValue(
        text="Animation",
        description="FIAF Glossary of Filmographic Terms B.13.1",
        meaning=FIAF["Animation"])
    AnimationDirector = PermissibleValue(
        text="AnimationDirector",
        description="FIAF Glossary of Filmographic Terms B.13.9",
        meaning=FIAF["AnimationDirector"])
    AnimationLighter = PermissibleValue(
        text="AnimationLighter",
        description="FIAF Glossary of Filmographic Terms B.13.19",
        meaning=FIAF["AnimationLighter"])
    Animator = PermissibleValue(
        text="Animator",
        description="FIAF Glossary of Filmographic Terms B.13.11",
        meaning=FIAF["Animator"])
    CharacterDesigner = PermissibleValue(
        text="CharacterDesigner",
        description="FIAF Glossary of Filmographic Terms B.13.14",
        meaning=FIAF["CharacterDesigner"])
    Cleanup = PermissibleValue(
        text="Cleanup",
        description="FIAF Glossary of Filmographic Terms B.13.15",
        meaning=FIAF["Cleanup"])
    LeadAnimator = PermissibleValue(
        text="LeadAnimator",
        description="FIAF Glossary of Filmographic Terms B.13.10",
        meaning=FIAF["LeadAnimator"])
    ModelMaker = PermissibleValue(
        text="ModelMaker",
        description="FIAF Glossary of Filmographic Terms B.13.17",
        meaning=FIAF["ModelMaker"])

    _defn = EnumDefinition(
        name="AnimationActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.13",
    )

class CastActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.7
    """
    AnimalTrainer = PermissibleValue(
        text="AnimalTrainer",
        description="FIAF Glossary of Filmographic Terms B.7.12",
        meaning=FIAF["AnimalTrainer"])
    CastMember = PermissibleValue(
        text="CastMember",
        description="FIAF Glossary of Filmographic Terms B.7.1",
        meaning=FIAF["CastMember"])
    Dancer = PermissibleValue(
        text="Dancer",
        description="FIAF Glossary of Filmographic Terms B.7.5",
        meaning=FIAF["Dancer"])
    DialogueCoach = PermissibleValue(
        text="DialogueCoach",
        description="FIAF Glossary of Filmographic Terms B.7.8",
        meaning=FIAF["DialogueCoach"])
    Double = PermissibleValue(
        text="Double",
        description="FIAF Glossary of Filmographic Terms B.7.2",
        meaning=FIAF["Double"])
    Extra = PermissibleValue(
        text="Extra",
        description="FIAF Glossary of Filmographic Terms B.7.4",
        meaning=FIAF["Extra"])
    Interviewer = PermissibleValue(
        text="Interviewer",
        description="FIAF Glossary of Filmographic Terms B.7.9",
        meaning=FIAF["Interviewer"])
    Narrator = PermissibleValue(
        text="Narrator",
        description="FIAF Glossary of Filmographic Terms B.7.10",
        meaning=FIAF["Narrator"])
    Singer = PermissibleValue(
        text="Singer",
        description="FIAF Glossary of Filmographic Terms B.7.6",
        meaning=FIAF["Singer"])
    StandIn = PermissibleValue(
        text="StandIn",
        description="FIAF Glossary of Filmographic Terms B.7.3",
        meaning=FIAF["StandIn"])
    StuntPerformer = PermissibleValue(
        text="StuntPerformer",
        description="FIAF Glossary of Filmographic Terms B.7.11",
        meaning=FIAF["StuntPerformer"])
    Voices = PermissibleValue(
        text="Voices",
        description="FIAF Glossary of Filmographic Terms B.7.7",
        meaning=FIAF["Voices"])
    Wrangler = PermissibleValue(
        text="Wrangler",
        description="FIAF Glossary of Filmographic Terms B.7.13",
        meaning=FIAF["Wrangler"])

    _defn = EnumDefinition(
        name="CastActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.7",
    )

class CensorshipActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.1
    """
    Censor = PermissibleValue(
        text="Censor",
        description="FIAF Glossary of Filmographic Terms C.1.1",
        meaning=FIAF["Censor"])

    _defn = EnumDefinition(
        name="CensorshipActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.1",
    )

class CinematographyActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.5
    """
    AerialPhotography = PermissibleValue(
        text="AerialPhotography",
        description="FIAF Glossary of Filmographic Terms B.5.4",
        meaning=FIAF["AerialPhotography"])
    BestBoy = PermissibleValue(
        text="BestBoy",
        description="FIAF Glossary of Filmographic Terms B.5.12",
        meaning=FIAF["BestBoy"])
    CameraAssistant = PermissibleValue(
        text="CameraAssistant",
        description="FIAF Glossary of Filmographic Terms B.5.7",
        meaning=FIAF["CameraAssistant"])
    CameraOperator = PermissibleValue(
        text="CameraOperator",
        description="FIAF Glossary of Filmographic Terms B.5.3",
        meaning=FIAF["CameraOperator"])
    Cinematographer = PermissibleValue(
        text="Cinematographer",
        description="FIAF Glossary of Filmographic Terms B.5.1",
        meaning=FIAF["Cinematographer"])
    ColorConsultant = PermissibleValue(
        text="ColorConsultant",
        description="FIAF Glossary of Filmographic Terms B.5.19",
        meaning=FIAF["ColorConsultant"])
    CraneOperator = PermissibleValue(
        text="CraneOperator",
        description="FIAF Glossary of Filmographic Terms B.5.16",
        meaning=FIAF["CraneOperator"])
    DollyGrip = PermissibleValue(
        text="DollyGrip",
        description="FIAF Glossary of Filmographic Terms B.5.15",
        meaning=FIAF["DollyGrip"])
    Electrician = PermissibleValue(
        text="Electrician",
        description="FIAF Glossary of Filmographic Terms B.5.13",
        meaning=FIAF["Electrician"])
    FocusPuller = PermissibleValue(
        text="FocusPuller",
        description="FIAF Glossary of Filmographic Terms B.5.8",
        meaning=FIAF["FocusPuller"])
    GafferLighting = PermissibleValue(
        text="GafferLighting",
        description="FIAF Glossary of Filmographic Terms B.5.11",
        meaning=FIAF["GafferLighting"])
    GeneratorOperator = PermissibleValue(
        text="GeneratorOperator",
        description="FIAF Glossary of Filmographic Terms B.5.17",
        meaning=FIAF["GeneratorOperator"])
    Grip = PermissibleValue(
        text="Grip",
        description="FIAF Glossary of Filmographic Terms B.5.14",
        meaning=FIAF["Grip"])
    Lenses = PermissibleValue(
        text="Lenses",
        description="FIAF Glossary of Filmographic Terms B.5.20",
        meaning=FIAF["Lenses"])
    LoaderClapper = PermissibleValue(
        text="LoaderClapper",
        description="FIAF Glossary of Filmographic Terms B.5.9",
        meaning=FIAF["LoaderClapper"])
    SecondUnitDirectorofPhotography = PermissibleValue(
        text="SecondUnitDirectorofPhotography",
        description="FIAF Glossary of Filmographic Terms B.5.2",
        meaning=FIAF["SecondUnitDirectorofPhotography"])
    SteadicamOperator = PermissibleValue(
        text="SteadicamOperator",
        description="FIAF Glossary of Filmographic Terms B.5.6",
        meaning=FIAF["SteadicamOperator"])
    StillPhotographer = PermissibleValue(
        text="StillPhotographer",
        description="FIAF Glossary of Filmographic Terms B.5.18",
        meaning=FIAF["StillPhotographer"])
    UnderwaterPhotography = PermissibleValue(
        text="UnderwaterPhotography",
        description="FIAF Glossary of Filmographic Terms B.5.5",
        meaning=FIAF["UnderwaterPhotography"])
    VideoAssist = PermissibleValue(
        text="VideoAssist",
        description="FIAF Glossary of Filmographic Terms B.5.10",
        meaning=FIAF["VideoAssist"])

    _defn = EnumDefinition(
        name="CinematographyActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.5",
    )

class CopyrightAndDistributionActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.2
    """
    Distributor = PermissibleValue(
        text="Distributor",
        description="FIAF Glossary of Filmographic Terms C.2.3",
        meaning=FIAF["Distributor"])
    NationalDistributor = PermissibleValue(
        text="NationalDistributor",
        description="FIAF Glossary of Filmographic Terms C.2.6",
        meaning=FIAF["NationalDistributor"])
    OriginalCopyrightOwner = PermissibleValue(
        text="OriginalCopyrightOwner",
        description="FIAF Glossary of Filmographic Terms C.2.1",
        meaning=FIAF["OriginalCopyrightOwner"])
    OriginalDistributor = PermissibleValue(
        text="OriginalDistributor",
        description="FIAF Glossary of Filmographic Terms C.2.4",
        meaning=FIAF["OriginalDistributor"])
    PresentCopyrightOwner = PermissibleValue(
        text="PresentCopyrightOwner",
        description="FIAF Glossary of Filmographic Terms C.2.2",
        meaning=FIAF["PresentCopyrightOwner"])
    RegionalDistributor = PermissibleValue(
        text="RegionalDistributor",
        description="FIAF Glossary of Filmographic Terms C.2.7",
        meaning=FIAF["RegionalDistributor"])
    WorldDistributor = PermissibleValue(
        text="WorldDistributor",
        description="FIAF Glossary of Filmographic Terms C.2.5",
        meaning=FIAF["WorldDistributor"])

    _defn = EnumDefinition(
        name="CopyrightAndDistributionActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.2",
    )

class DirectingActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.3
    """
    AssistantDirector = PermissibleValue(
        text="AssistantDirector",
        description="FIAF Glossary of Filmographic Terms B.3.2",
        meaning=FIAF["AssistantDirector"])
    CastingDirector = PermissibleValue(
        text="CastingDirector",
        description="FIAF Glossary of Filmographic Terms B.3.4",
        meaning=FIAF["CastingDirector"])
    Continuity = PermissibleValue(
        text="Continuity",
        description="FIAF Glossary of Filmographic Terms B.3.5",
        meaning=FIAF["Continuity"])
    Director = PermissibleValue(
        text="Director",
        description="FIAF Glossary of Filmographic Terms B.3.1",
        meaning=FIAF["Director"])
    FightArranger = PermissibleValue(
        text="FightArranger",
        description="FIAF Glossary of Filmographic Terms B.3.7",
        meaning=FIAF["FightArranger"])
    SecondUnitDirector = PermissibleValue(
        text="SecondUnitDirector",
        description="FIAF Glossary of Filmographic Terms B.3.3",
        meaning=FIAF["SecondUnitDirector"])
    StuntArranger = PermissibleValue(
        text="StuntArranger",
        description="FIAF Glossary of Filmographic Terms B.3.6",
        meaning=FIAF["StuntArranger"])

    _defn = EnumDefinition(
        name="DirectingActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.3",
    )

class EditingActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.10
    """
    AssistantFilmEditor = PermissibleValue(
        text="AssistantFilmEditor",
        description="FIAF Glossary of Filmographic Terms B.10.2",
        meaning=FIAF["AssistantFilmEditor"])
    FilmEditor = PermissibleValue(
        text="FilmEditor",
        description="FIAF Glossary of Filmographic Terms B.10.1",
        meaning=FIAF["FilmEditor"])

    _defn = EnumDefinition(
        name="EditingActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.10",
    )

class LaboratoryActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.12
    """
    Colorist = PermissibleValue(
        text="Colorist",
        description="FIAF Glossary of Filmographic Terms B.12.4",
        meaning=FIAF["Colorist"])
    Laboratory = PermissibleValue(
        text="Laboratory",
        description="FIAF Glossary of Filmographic Terms B.12.1",
        meaning=FIAF["Laboratory"])
    LaboratoryTechnician = PermissibleValue(
        text="LaboratoryTechnician",
        description="FIAF Glossary of Filmographic Terms B.12.2",
        meaning=FIAF["LaboratoryTechnician"])
    NegativeCutter = PermissibleValue(
        text="NegativeCutter",
        description="FIAF Glossary of Filmographic Terms B.12.3",
        meaning=FIAF["NegativeCutter"])

    _defn = EnumDefinition(
        name="LaboratoryActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.12",
    )

class MusicActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.11
    """
    Choreographer = PermissibleValue(
        text="Choreographer",
        description="FIAF Glossary of Filmographic Terms B.11.15",
        meaning=FIAF["Choreographer"])
    Composer = PermissibleValue(
        text="Composer",
        description="FIAF Glossary of Filmographic Terms B.11.1",
        meaning=FIAF["Composer"])
    Lyricist = PermissibleValue(
        text="Lyricist",
        description="FIAF Glossary of Filmographic Terms B.11.13",
        meaning=FIAF["Lyricist"])
    MusicArranger = PermissibleValue(
        text="MusicArranger",
        description="FIAF Glossary of Filmographic Terms B.11.4",
        meaning=FIAF["MusicArranger"])
    MusicConductor = PermissibleValue(
        text="MusicConductor",
        description="FIAF Glossary of Filmographic Terms B.11.6",
        meaning=FIAF["MusicConductor"])
    MusicContractor = PermissibleValue(
        text="MusicContractor",
        description="FIAF Glossary of Filmographic Terms B.11.9",
        meaning=FIAF["MusicContractor"])
    MusicEditor = PermissibleValue(
        text="MusicEditor",
        description="FIAF Glossary of Filmographic Terms B.11.14",
        meaning=FIAF["MusicEditor"])
    MusicPerformer = PermissibleValue(
        text="MusicPerformer",
        description="FIAF Glossary of Filmographic Terms B.11.7",
        meaning=FIAF["MusicPerformer"])
    MusicSupervisor = PermissibleValue(
        text="MusicSupervisor",
        description="FIAF Glossary of Filmographic Terms B.11.3",
        meaning=FIAF["MusicSupervisor"])
    SingingVoice = PermissibleValue(
        text="SingingVoice",
        description="FIAF Glossary of Filmographic Terms B.11.8",
        meaning=FIAF["SingingVoice"])
    SongComposer = PermissibleValue(
        text="SongComposer",
        description="FIAF Glossary of Filmographic Terms B.11.12",
        meaning=FIAF["SongComposer"])

    _defn = EnumDefinition(
        name="MusicActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.11",
    )

class ProducingActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.2
    """
    Advisor = PermissibleValue(
        text="Advisor",
        description="FIAF Glossary of Filmographic Terms B.2.19",
        meaning=FIAF["Advisor"])
    AssistantProducer = PermissibleValue(
        text="AssistantProducer",
        description="FIAF Glossary of Filmographic Terms B.2.8",
        meaning=FIAF["AssistantProducer"])
    AssociateProducer = PermissibleValue(
        text="AssociateProducer",
        description="FIAF Glossary of Filmographic Terms B.2.6",
        meaning=FIAF["AssociateProducer"])
    Cooperation = PermissibleValue(
        text="Cooperation",
        description="FIAF Glossary of Filmographic Terms B.2.22",
        meaning=FIAF["Cooperation"])
    Coproducer = PermissibleValue(
        text="Coproducer",
        description="FIAF Glossary of Filmographic Terms B.2.5",
        meaning=FIAF["Coproducer"])
    ExecutiveProducer = PermissibleValue(
        text="ExecutiveProducer",
        description="FIAF Glossary of Filmographic Terms B.2.4",
        meaning=FIAF["ExecutiveProducer"])
    LineProducer = PermissibleValue(
        text="LineProducer",
        description="FIAF Glossary of Filmographic Terms B.2.7",
        meaning=FIAF["LineProducer"])
    LocationManager = PermissibleValue(
        text="LocationManager",
        description="FIAF Glossary of Filmographic Terms B.2.12",
        meaning=FIAF["LocationManager"])
    PostProductionSupervisor = PermissibleValue(
        text="PostProductionSupervisor",
        description="FIAF Glossary of Filmographic Terms B.2.15",
        meaning=FIAF["PostProductionSupervisor"])
    Presenter = PermissibleValue(
        text="Presenter",
        description="FIAF Glossary of Filmographic Terms B.2.21",
        meaning=FIAF["Presenter"])
    Producer = PermissibleValue(
        text="Producer",
        description="FIAF Glossary of Filmographic Terms B.2.3",
        meaning=FIAF["Producer"])
    ProductionAccountant = PermissibleValue(
        text="ProductionAccountant",
        description="FIAF Glossary of Filmographic Terms B.2.11",
        meaning=FIAF["ProductionAccountant"])
    ProductionAssistant = PermissibleValue(
        text="ProductionAssistant",
        description="FIAF Glossary of Filmographic Terms B.2.14",
        meaning=FIAF["ProductionAssistant"])
    ProductionCompany = PermissibleValue(
        text="ProductionCompany",
        description="FIAF Glossary of Filmographic Terms B.2.1",
        meaning=FIAF["ProductionCompany"])
    ProductionCoordinator = PermissibleValue(
        text="ProductionCoordinator",
        description="FIAF Glossary of Filmographic Terms B.2.10",
        meaning=FIAF["ProductionCoordinator"])
    ProductionManager = PermissibleValue(
        text="ProductionManager",
        description="FIAF Glossary of Filmographic Terms B.2.9",
        meaning=FIAF["ProductionManager"])
    Publicist = PermissibleValue(
        text="Publicist",
        description="FIAF Glossary of Filmographic Terms B.2.16",
        meaning=FIAF["Publicist"])
    SeriesProducer = PermissibleValue(
        text="SeriesProducer",
        description="FIAF Glossary of Filmographic Terms B.2.17",
        meaning=FIAF["SeriesProducer"])
    Sponsor = PermissibleValue(
        text="Sponsor",
        description="FIAF Glossary of Filmographic Terms B.2.20",
        meaning=FIAF["Sponsor"])
    Studio = PermissibleValue(
        text="Studio",
        description="FIAF Glossary of Filmographic Terms B.2.23",
        meaning=FIAF["Studio"])
    TransportationManager = PermissibleValue(
        text="TransportationManager",
        description="FIAF Glossary of Filmographic Terms B.2.13",
        meaning=FIAF["TransportationManager"])

    _defn = EnumDefinition(
        name="ProducingActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.2",
    )

class ProductionDesignActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.6
    """
    ArtDirector = PermissibleValue(
        text="ArtDirector",
        description="FIAF Glossary of Filmographic Terms B.6.2",
        meaning=FIAF["ArtDirector"])
    AssistantArtDirector = PermissibleValue(
        text="AssistantArtDirector",
        description="FIAF Glossary of Filmographic Terms B.6.3",
        meaning=FIAF["AssistantArtDirector"])
    ConstructionCoordinator = PermissibleValue(
        text="ConstructionCoordinator",
        description="FIAF Glossary of Filmographic Terms B.6.8",
        meaning=FIAF["ConstructionCoordinator"])
    CostumeDesigner = PermissibleValue(
        text="CostumeDesigner",
        description="FIAF Glossary of Filmographic Terms B.6.12",
        meaning=FIAF["CostumeDesigner"])
    CostumeMaker = PermissibleValue(
        text="CostumeMaker",
        description="FIAF Glossary of Filmographic Terms B.6.17",
        meaning=FIAF["CostumeMaker"])
    CostumeSupervisor = PermissibleValue(
        text="CostumeSupervisor",
        description="FIAF Glossary of Filmographic Terms B.6.13",
        meaning=FIAF["CostumeSupervisor"])
    CostumeSupplier = PermissibleValue(
        text="CostumeSupplier",
        description="FIAF Glossary of Filmographic Terms B.6.18",
        meaning=FIAF["CostumeSupplier"])
    Costumer = PermissibleValue(
        text="Costumer",
        description="FIAF Glossary of Filmographic Terms B.6.14",
        meaning=FIAF["Costumer"])
    Gowns = PermissibleValue(
        text="Gowns",
        description="FIAF Glossary of Filmographic Terms B.6.16",
        meaning=FIAF["Gowns"])
    Greensperson = PermissibleValue(
        text="Greensperson",
        description="FIAF Glossary of Filmographic Terms B.6.11",
        meaning=FIAF["Greensperson"])
    HairStylist = PermissibleValue(
        text="HairStylist",
        description="FIAF Glossary of Filmographic Terms B.6.20",
        meaning=FIAF["HairStylist"])
    LeadPerson = PermissibleValue(
        text="LeadPerson",
        description="FIAF Glossary of Filmographic Terms B.6.9",
        meaning=FIAF["LeadPerson"])
    MakeUpArtist = PermissibleValue(
        text="MakeUpArtist",
        description="FIAF Glossary of Filmographic Terms B.6.19",
        meaning=FIAF["MakeUpArtist"])
    ProductionDesigner = PermissibleValue(
        text="ProductionDesigner",
        description="FIAF Glossary of Filmographic Terms B.6.1",
        meaning=FIAF["ProductionDesigner"])
    PropertyMaster = PermissibleValue(
        text="PropertyMaster",
        description="FIAF Glossary of Filmographic Terms B.6.7",
        meaning=FIAF["PropertyMaster"])
    ScenicArtist = PermissibleValue(
        text="ScenicArtist",
        description="FIAF Glossary of Filmographic Terms B.6.10",
        meaning=FIAF["ScenicArtist"])
    SetDecorator = PermissibleValue(
        text="SetDecorator",
        description="FIAF Glossary of Filmographic Terms B.6.6",
        meaning=FIAF["SetDecorator"])
    SetDesigner = PermissibleValue(
        text="SetDesigner",
        description="FIAF Glossary of Filmographic Terms B.6.5",
        meaning=FIAF["SetDesigner"])
    StoryboardArtist = PermissibleValue(
        text="StoryboardArtist",
        description="FIAF Glossary of Filmographic Terms B.6.4",
        meaning=FIAF["StoryboardArtist"])
    TitleDesigner = PermissibleValue(
        text="TitleDesigner",
        description="FIAF Glossary of Filmographic Terms B.6.21",
        meaning=FIAF["TitleDesigner"])
    WardrobeSupervisor = PermissibleValue(
        text="WardrobeSupervisor",
        description="FIAF Glossary of Filmographic Terms B.6.15",
        meaning=FIAF["WardrobeSupervisor"])

    _defn = EnumDefinition(
        name="ProductionDesignActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.6",
    )

class PuppetActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.14
    """
    Puppeteer = PermissibleValue(
        text="Puppeteer",
        description="FIAF Glossary of Filmographic Terms B.14.7",
        meaning=FIAF["Puppeteer"])

    _defn = EnumDefinition(
        name="PuppetActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.14",
    )

class SoundActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.9
    """
    BoomOperator = PermissibleValue(
        text="BoomOperator",
        description="FIAF Glossary of Filmographic Terms B.9.4",
        meaning=FIAF["BoomOperator"])
    DialogueEditor = PermissibleValue(
        text="DialogueEditor",
        description="FIAF Glossary of Filmographic Terms B.9.8",
        meaning=FIAF["DialogueEditor"])
    DubbingDirector = PermissibleValue(
        text="DubbingDirector",
        description="FIAF Glossary of Filmographic Terms B.9.13",
        meaning=FIAF["DubbingDirector"])
    DubbingEditor = PermissibleValue(
        text="DubbingEditor",
        description="FIAF Glossary of Filmographic Terms B.9.14",
        meaning=FIAF["DubbingEditor"])
    DubbingMixer = PermissibleValue(
        text="DubbingMixer",
        description="FIAF Glossary of Filmographic Terms B.9.11",
        meaning=FIAF["DubbingMixer"])
    DubbingSpeaker = PermissibleValue(
        text="DubbingSpeaker",
        description="FIAF Glossary of Filmographic Terms B.9.15",
        meaning=FIAF["DubbingSpeaker"])
    FoleyArtist = PermissibleValue(
        text="FoleyArtist",
        description="FIAF Glossary of Filmographic Terms B.9.9",
        meaning=FIAF["FoleyArtist"])
    SoundDesigner = PermissibleValue(
        text="SoundDesigner",
        description="FIAF Glossary of Filmographic Terms B.9.1",
        meaning=FIAF["SoundDesigner"])
    SoundEditor = PermissibleValue(
        text="SoundEditor",
        description="FIAF Glossary of Filmographic Terms B.9.7",
        meaning=FIAF["SoundEditor"])
    SoundEngineer = PermissibleValue(
        text="SoundEngineer",
        description="FIAF Glossary of Filmographic Terms B.9.5",
        meaning=FIAF["SoundEngineer"])
    SoundRecorderMixer = PermissibleValue(
        text="SoundRecorderMixer",
        description="FIAF Glossary of Filmographic Terms B.9.3",
        meaning=FIAF["SoundRecorderMixer"])
    SoundSupervisor = PermissibleValue(
        text="SoundSupervisor",
        description="FIAF Glossary of Filmographic Terms B.9.2",
        meaning=FIAF["SoundSupervisor"])
    SupervisingSoundEditor = PermissibleValue(
        text="SupervisingSoundEditor",
        description="FIAF Glossary of Filmographic Terms B.9.6",
        meaning=FIAF["SupervisingSoundEditor"])

    _defn = EnumDefinition(
        name="SoundActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.9",
    )

class SpecialEffectsActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.8
    """
    Animatronics = PermissibleValue(
        text="Animatronics",
        description="FIAF Glossary of Filmographic Terms B.8.4",
        meaning=FIAF["Animatronics"])
    Armorer = PermissibleValue(
        text="Armorer",
        description="FIAF Glossary of Filmographic Terms B.8.7",
        meaning=FIAF["Armorer"])
    CGIArtist = PermissibleValue(
        text="CGIArtist",
        description="FIAF Glossary of Filmographic Terms B.8.12",
        meaning=FIAF["CGIArtist"])
    Compositor = PermissibleValue(
        text="Compositor",
        description="FIAF Glossary of Filmographic Terms B.8.10",
        meaning=FIAF["Compositor"])
    MatteArtist = PermissibleValue(
        text="MatteArtist",
        description="FIAF Glossary of Filmographic Terms B.8.8",
        meaning=FIAF["MatteArtist"])
    MechanicalEffects = PermissibleValue(
        text="MechanicalEffects",
        description="FIAF Glossary of Filmographic Terms B.8.3",
        meaning=FIAF["MechanicalEffects"])
    MotionCapture = PermissibleValue(
        text="MotionCapture",
        description="FIAF Glossary of Filmographic Terms B.8.13",
        meaning=FIAF["MotionCapture"])
    Prosthetics = PermissibleValue(
        text="Prosthetics",
        description="FIAF Glossary of Filmographic Terms B.8.5",
        meaning=FIAF["Prosthetics"])
    Pyrotechnics = PermissibleValue(
        text="Pyrotechnics",
        description="FIAF Glossary of Filmographic Terms B.8.6",
        meaning=FIAF["Pyrotechnics"])
    RotoscopeArtist = PermissibleValue(
        text="RotoscopeArtist",
        description="FIAF Glossary of Filmographic Terms B.8.9",
        meaning=FIAF["RotoscopeArtist"])
    SpecialEffects = PermissibleValue(
        text="SpecialEffects",
        description="FIAF Glossary of Filmographic Terms B.8.1",
        meaning=FIAF["SpecialEffects"])
    VisualEffects = PermissibleValue(
        text="VisualEffects",
        description="FIAF Glossary of Filmographic Terms B.8.2",
        meaning=FIAF["VisualEffects"])

    _defn = EnumDefinition(
        name="SpecialEffectsActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.8",
    )

class WritingActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.4
    """
    Adaptation = PermissibleValue(
        text="Adaptation",
        description="FIAF Glossary of Filmographic Terms B.4.11",
        meaning=FIAF["Adaptation"])
    BasedonCharactersCreatedby = PermissibleValue(
        text="BasedonCharactersCreatedby",
        description="FIAF Glossary of Filmographic Terms B.4.5",
        meaning=FIAF["BasedonCharactersCreatedby"])
    Idea = PermissibleValue(
        text="Idea",
        description="FIAF Glossary of Filmographic Terms B.4.6",
        meaning=FIAF["Idea"])
    NarrationWriter = PermissibleValue(
        text="NarrationWriter",
        description="FIAF Glossary of Filmographic Terms B.4.15",
        meaning=FIAF["NarrationWriter"])
    Research = PermissibleValue(
        text="Research",
        description="FIAF Glossary of Filmographic Terms B.4.16",
        meaning=FIAF["Research"])
    ScreenStory = PermissibleValue(
        text="ScreenStory",
        description="FIAF Glossary of Filmographic Terms B.4.3",
        meaning=FIAF["ScreenStory"])
    SeriesCreatedby = PermissibleValue(
        text="SeriesCreatedby",
        description="FIAF Glossary of Filmographic Terms B.4.7",
        meaning=FIAF["SeriesCreatedby"])
    SourceMaterial = PermissibleValue(
        text="SourceMaterial",
        description="FIAF Glossary of Filmographic Terms B.4.4",
        meaning=FIAF["SourceMaterial"])
    Stagedby = PermissibleValue(
        text="Stagedby",
        description="FIAF Glossary of Filmographic Terms B.4.8",
        meaning=FIAF["Stagedby"])
    Writer = PermissibleValue(
        text="Writer",
        description="FIAF Glossary of Filmographic Terms B.4.2",
        meaning=FIAF["Writer"])

    _defn = EnumDefinition(
        name="WritingActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.4",
    )

class ManifestationActivityTypeEnum(EnumDefinitionImpl):
    """
    Activity types / roles. See also: FIAF Moving Image Cataloguing Manual 2.4.1.1, D.8
    """
    AgentNotIdentified = PermissibleValue(
        text="AgentNotIdentified",
        description="FIAF Moving Image Cataloguing Manual D.8.11",
        meaning=FIAF["AgentNotIdentified"])
    AgentResponsibleForPreservation = PermissibleValue(
        text="AgentResponsibleForPreservation",
        description="FIAF Moving Image Cataloguing Manual D.8.6",
        meaning=FIAF["AgentResponsibleForPreservation"])
    AgentResponsibleForReproductionOrTransfer = PermissibleValue(
        text="AgentResponsibleForReproductionOrTransfer",
        description="FIAF Moving Image Cataloguing Manual D.8.7",
        meaning=FIAF["AgentResponsibleForReproductionOrTransfer"])
    AgentResponsibleForTheArchivalAvailability = PermissibleValue(
        text="AgentResponsibleForTheArchivalAvailability",
        description="FIAF Moving Image Cataloguing Manual D.8.8",
        meaning=FIAF["AgentResponsibleForTheArchivalAvailability"])
    AgentResponsibleForTheMereAvailability = PermissibleValue(
        text="AgentResponsibleForTheMereAvailability",
        description="FIAF Moving Image Cataloguing Manual D.8.9",
        meaning=FIAF["AgentResponsibleForTheMereAvailability"])
    AgentUnclearOrUndetermined = PermissibleValue(
        text="AgentUnclearOrUndetermined",
        description="FIAF Moving Image Cataloguing Manual D.8.10",
        meaning=FIAF["AgentUnclearOrUndetermined"])
    Broadcaster = PermissibleValue(
        text="Broadcaster",
        description="FIAF Moving Image Cataloguing Manual D.8.3",
        meaning=FIAF["Broadcaster"])
    DistributorNonTheatrical = PermissibleValue(
        text="DistributorNonTheatrical",
        description="FIAF Moving Image Cataloguing Manual D.8.2",
        meaning=FIAF["DistributorNonTheatrical"])
    DistributorTheatrical = PermissibleValue(
        text="DistributorTheatrical",
        description="FIAF Moving Image Cataloguing Manual D.8.1",
        meaning=FIAF["DistributorTheatrical"])
    Manufacturer = PermissibleValue(
        text="Manufacturer",
        description="FIAF Moving Image Cataloguing Manual D.8.5",
        meaning=FIAF["Manufacturer"])
    Publisher = PermissibleValue(
        text="Publisher",
        description="FIAF Moving Image Cataloguing Manual D.8.4",
        meaning=FIAF["Publisher"])
    UnknownActivity = PermissibleValue(
        text="UnknownActivity",
        description="FIAF Moving Image Cataloguing Manual 1.4.1.1, 2.4.1.1, 3.3.1.1")

    _defn = EnumDefinition(
        name="ManifestationActivityTypeEnum",
        description="Activity types / roles. See also: FIAF Moving Image Cataloguing Manual 2.4.1.1, D.8",
    )

class AgentTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual 1.4.1
    """
    CorporateBody = PermissibleValue(
        text="CorporateBody",
        meaning=FIAF["CorporateBody"])
    Family = PermissibleValue(
        text="Family",
        meaning=FIAF["Family"])
    Person = PermissibleValue(
        text="Person",
        meaning=FIAF["Person"])
    PersonGroup = PermissibleValue(
        text="PersonGroup",
        meaning=FIAF["PersonGroup"])

    _defn = EnumDefinition(
        name="AgentTypeEnum",
        description="FIAF Moving Image Cataloguing Manual 1.4.1",
    )

class ColourTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual 2.3.4.4, 3.1.5.6, D.7.11
    """
    BlackAndWhite = PermissibleValue(
        text="BlackAndWhite",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["BlackAndWhite"])
    BlackAndWhiteTinted = PermissibleValue(
        text="BlackAndWhiteTinted",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["BlackAndWhiteTinted"])
    BlackAndWhiteTintedAndToned = PermissibleValue(
        text="BlackAndWhiteTintedAndToned",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["BlackAndWhiteTintedAndToned"])
    BlackAndWhiteToned = PermissibleValue(
        text="BlackAndWhiteToned",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["BlackAndWhiteToned"])
    Colour = PermissibleValue(
        text="Colour",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["Colour"])
    ColourBlackAndWhite = PermissibleValue(
        text="ColourBlackAndWhite",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["ColourBlackAndWhite"])
    Sepia = PermissibleValue(
        text="Sepia",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["Sepia"])
    Tinted = PermissibleValue(
        text="Tinted",
        description="FIAF Moving Image Cataloguing Manual D.7.11",
        meaning=FIAF["Tinted"])

    _defn = EnumDefinition(
        name="ColourTypeEnum",
        description="FIAF Moving Image Cataloguing Manual 2.3.4.4, 3.1.5.6, D.7.11",
    )

class ManufactureEventTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.4.7, D.14
    """
    FilmPrintingEvent = PermissibleValue(
        text="FilmPrintingEvent",
        description="FIAF Moving Image Cataloguing Manual D.14",
        meaning=FIAF["FilmPrintingEvent"])
    MasteringEvent = PermissibleValue(
        text="MasteringEvent",
        description="FIAF Moving Image Cataloguing Manual D.14",
        meaning=FIAF["MasteringEvent"])
    ScanningEvent = PermissibleValue(
        text="ScanningEvent",
        description="FIAF Moving Image Cataloguing Manual D.14",
        meaning=FIAF["ScanningEvent"])
    TelecineEvent = PermissibleValue(
        text="TelecineEvent",
        description="FIAF Moving Image Cataloguing Manual D.14",
        meaning=FIAF["TelecineEvent"])
    UploadingEvent = PermissibleValue(
        text="UploadingEvent",
        description="FIAF Moving Image Cataloguing Manual D.14",
        meaning=FIAF["UploadingEvent"])
    VideoCopyingEvent = PermissibleValue(
        text="VideoCopyingEvent",
        description="FIAF Moving Image Cataloguing Manual D.14",
        meaning=FIAF["VideoCopyingEvent"])

    _defn = EnumDefinition(
        name="ManufactureEventTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.4.7, D.14",
    )

class PreservationEventTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.4.5
    """
    DigitisationEvent = PermissibleValue(
        text="DigitisationEvent",
        description="FIAF Moving Image Cataloguing Manual D.12",
        meaning=FIAF["DigitisationEvent"])
    DuplicationEvent = PermissibleValue(
        text="DuplicationEvent",
        description="FIAF Moving Image Cataloguing Manual D.12",
        meaning=FIAF["DuplicationEvent"])
    ReproductionEvent = PermissibleValue(
        text="ReproductionEvent",
        description="FIAF Moving Image Cataloguing Manual D.12",
        meaning=FIAF["ReproductionEvent"])
    TransferEvent = PermissibleValue(
        text="TransferEvent",
        description="FIAF Moving Image Cataloguing Manual D.12",
        meaning=FIAF["TransferEvent"])

    _defn = EnumDefinition(
        name="PreservationEventTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.4.5",
    )

class ProductionEventTypeEnum(EnumDefinitionImpl):
    """
    Leave unset for main production event, otherwise see FIAF Moving Image Cataloguing Manual D.4.3, D.11
    """
    CastingEvent = PermissibleValue(
        text="CastingEvent",
        description="FIAF Moving Image Cataloguing Manual D.11",
        meaning=FIAF["CastingEvent"])
    IndoorShootingEvent = PermissibleValue(
        text="IndoorShootingEvent",
        description="FIAF Moving Image Cataloguing Manual D.11",
        meaning=FIAF["IndoorShootingEvent"])
    OutdoorShootingEvent = PermissibleValue(
        text="OutdoorShootingEvent",
        description="FIAF Moving Image Cataloguing Manual D.11",
        meaning=FIAF["OutdoorShootingEvent"])
    PostProductionEvent = PermissibleValue(
        text="PostProductionEvent",
        description="FIAF Moving Image Cataloguing Manual D.11",
        meaning=FIAF["PostProductionEvent"])

    _defn = EnumDefinition(
        name="ProductionEventTypeEnum",
        description="""Leave unset for main production event, otherwise see FIAF Moving Image Cataloguing Manual D.4.3, D.11""",
    )

class PublicationEventTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.4.1, D.10
    """
    BroadcastEvent = PermissibleValue(
        text="BroadcastEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["BroadcastEvent"])
    DistributionEvent = PermissibleValue(
        text="DistributionEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["DistributionEvent"])
    HomeVideoPublicationEvent = PermissibleValue(
        text="HomeVideoPublicationEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["HomeVideoPublicationEvent"])
    NonTheatricalDistributionEvent = PermissibleValue(
        text="NonTheatricalDistributionEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["NonTheatricalDistributionEvent"])
    NotForReleaseEvent = PermissibleValue(
        text="NotForReleaseEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["NotForReleaseEvent"])
    OnlineTransmissionEvent = PermissibleValue(
        text="OnlineTransmissionEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["OnlineTransmissionEvent"])
    PreReleaseEvent = PermissibleValue(
        text="PreReleaseEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["PreReleaseEvent"])
    ReleaseEvent = PermissibleValue(
        text="ReleaseEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["ReleaseEvent"])
    TheatricalDistributionEvent = PermissibleValue(
        text="TheatricalDistributionEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["TheatricalDistributionEvent"])
    UnknownEvent = PermissibleValue(
        text="UnknownEvent",
        description="FIAF Moving Image Cataloguing Manual D.10",
        meaning=FIAF["UnknownEvent"])

    _defn = EnumDefinition(
        name="PublicationEventTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.4.1, D.10",
    )

class FormatAudioTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    Audiocassette = PermissibleValue(
        text="Audiocassette",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["Audiocassette"])
    HalfInchAudioReel = PermissibleValue(
        text="HalfInchAudioReel",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["HalfInchAudioReel"])
    OneInchAudioReel = PermissibleValue(
        text="OneInchAudioReel",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["OneInchAudioReel"])
    QuarterInchAudioReel = PermissibleValue(
        text="QuarterInchAudioReel",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["QuarterInchAudioReel"])
    TwoInchAudioReel = PermissibleValue(
        text="TwoInchAudioReel",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["TwoInchAudioReel"])

    _defn = EnumDefinition(
        name="FormatAudioTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "16mmMagneticTrack",
            PermissibleValue(
                text="16mmMagneticTrack",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["16mmMagneticTrack"]))
        setattr(cls, "35mmMagneticTrack",
            PermissibleValue(
                text="35mmMagneticTrack",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["35mmMagneticTrack"]))

class FormatDigitalFileEncodingTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    MPEG4 = PermissibleValue(
        text="MPEG4",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["MPEG4"])
    Quicktime = PermissibleValue(
        text="Quicktime",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["Quicktime"])
    RealVideo = PermissibleValue(
        text="RealVideo",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["RealVideo"])
    SVCD = PermissibleValue(
        text="SVCD",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["SVCD"])
    VCD = PermissibleValue(
        text="VCD",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["VCD"])
    WindowsMedia = PermissibleValue(
        text="WindowsMedia",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["WindowsMedia"])

    _defn = EnumDefinition(
        name="FormatDigitalFileEncodingTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
    )

class FormatDigitalFileTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    AVI = PermissibleValue(
        text="AVI",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["AVI"])
    DPX = PermissibleValue(
        text="DPX",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["DPX"])
    MOV = PermissibleValue(
        text="MOV",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["MOV"])
    MP4 = PermissibleValue(
        text="MP4",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["MP4"])
    MXF = PermissibleValue(
        text="MXF",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["MXF"])

    _defn = EnumDefinition(
        name="FormatDigitalFileTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
    )

class FormatFilmTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    Super16mmFilm = PermissibleValue(
        text="Super16mmFilm",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["Super16mmFilm"])
    Super8mmFilm = PermissibleValue(
        text="Super8mmFilm",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["Super8mmFilm"])

    _defn = EnumDefinition(
        name="FormatFilmTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "16mmFilm",
            PermissibleValue(
                text="16mmFilm",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["16mmFilm"]))
        setattr(cls, "17.5mmFilm",
            PermissibleValue(
                text="17.5mmFilm",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["17.5mmFilm"]))
        setattr(cls, "35mmFilm",
            PermissibleValue(
                text="35mmFilm",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["35mmFilm"]))
        setattr(cls, "70mmFilm",
            PermissibleValue(
                text="70mmFilm",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["70mmFilm"]))
        setattr(cls, "8mmFilm",
            PermissibleValue(
                text="8mmFilm",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["8mmFilm"]))
        setattr(cls, "9.5mmFilm",
            PermissibleValue(
                text="9.5mmFilm",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["9.5mmFilm"]))

class FormatOpticalTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    BluRay = PermissibleValue(
        text="BluRay",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["BluRay"])
    CD = PermissibleValue(
        text="CD",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["CD"])
    DVD = PermissibleValue(
        text="DVD",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["DVD"])
    LaserDisc = PermissibleValue(
        text="LaserDisc",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["LaserDisc"])

    _defn = EnumDefinition(
        name="FormatOpticalTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
    )

class FormatVideoTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    BetacamSP = PermissibleValue(
        text="BetacamSP",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["BetacamSP"])
    D1 = PermissibleValue(
        text="D1",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["D1"])
    D5 = PermissibleValue(
        text="D5",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["D5"])
    DVCPROHD = PermissibleValue(
        text="DVCPROHD",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["DVCPROHD"])
    DigitalBetacam = PermissibleValue(
        text="DigitalBetacam",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["DigitalBetacam"])
    HDCAMSR = PermissibleValue(
        text="HDCAMSR",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
        meaning=FIAF["HDCAMSR"])

    _defn = EnumDefinition(
        name="FormatVideoTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.2",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "1InchCFormat",
            PermissibleValue(
                text="1InchCFormat",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["1InchCFormat"]))
        setattr(cls, "2InchQuadruplex",
            PermissibleValue(
                text="2InchQuadruplex",
                description="FIAF Moving Image Cataloguing Manual D.7.2",
                meaning=FIAF["2InchQuadruplex"]))

class ItemAccessStatusEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.3
    """
    Archive = PermissibleValue(text="Archive")
    Distribution = PermissibleValue(text="Distribution")
    Master = PermissibleValue(
        text="Master",
        description="FIAF Moving Image Cataloguing Manual D.7.3",
        meaning=FIAF["Master"])
    Removed = PermissibleValue(
        text="Removed",
        description="FIAF Moving Image Cataloguing Manual D.7.3",
        meaning=FIAF["Removed"])
    Viewing = PermissibleValue(
        text="Viewing",
        description="FIAF Moving Image Cataloguing Manual D.7.3",
        meaning=FIAF["Viewing"])

    _defn = EnumDefinition(
        name="ItemAccessStatusEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.3",
    )

class ItemElementTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.7.8
    """
    ColourNegative = PermissibleValue(
        text="ColourNegative",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["ColourNegative"])
    ColourPositive = PermissibleValue(
        text="ColourPositive",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["ColourPositive"])
    CopperTonedPositive = PermissibleValue(
        text="CopperTonedPositive",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["CopperTonedPositive"])
    CyanMatrix = PermissibleValue(
        text="CyanMatrix",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["CyanMatrix"])
    DCP = PermissibleValue(
        text="DCP",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["DCP"])
    DirectBWPositive = PermissibleValue(
        text="DirectBWPositive",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["DirectBWPositive"])
    DuplicateNegative = PermissibleValue(
        text="DuplicateNegative",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["DuplicateNegative"])
    DuplicatePositive = PermissibleValue(
        text="DuplicatePositive",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["DuplicatePositive"])
    ImageNegative = PermissibleValue(
        text="ImageNegative",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["ImageNegative"])
    Lavender = PermissibleValue(
        text="Lavender",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["Lavender"])
    OriginalNegative = PermissibleValue(
        text="OriginalNegative",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["OriginalNegative"])
    OriginalPositiveReversalFilm = PermissibleValue(
        text="OriginalPositiveReversalFilm",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["OriginalPositiveReversalFilm"])
    Positive = PermissibleValue(
        text="Positive",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["Positive"])
    SoundNegative = PermissibleValue(
        text="SoundNegative",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
        meaning=FIAF["SoundNegative"])

    _defn = EnumDefinition(
        name="ItemElementTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.7.8",
    )

class LanguageUsageEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual 2.3.3, D.6
    """
    AudioDescription = PermissibleValue(
        text="AudioDescription",
        description="Audio description for the visually impaired")
    Captions = PermissibleValue(
        text="Captions",
        description="FIAF Moving Image Cataloguing Manual D.6",
        meaning=FIAF["Captions"])
    ClosingCredits = PermissibleValue(text="ClosingCredits")
    Dubbed = PermissibleValue(
        text="Dubbed",
        description="FIAF Moving Image Cataloguing Manual 2.3.3")
    Intertitles = PermissibleValue(
        text="Intertitles",
        description="FIAF Moving Image Cataloguing Manual D.6",
        meaning=FIAF["Intertitles"])
    NoDialogue = PermissibleValue(
        text="NoDialogue",
        description="FIAF Moving Image Cataloguing Manual D.6",
        meaning=FIAF["NoDialogue"])
    OpeningCredits = PermissibleValue(text="OpeningCredits")
    SDHSubtitles = PermissibleValue(
        text="SDHSubtitles",
        description="Subtitles for the Deaf and Hard of hearing")
    SignedLanguage = PermissibleValue(
        text="SignedLanguage",
        description="FIAF Moving Image Cataloguing Manual D.6",
        meaning=FIAF["SignedLanguage"])
    SpokenLanguage = PermissibleValue(
        text="SpokenLanguage",
        description="FIAF Moving Image Cataloguing Manual D.6",
        meaning=FIAF["SpokenLanguage"])
    Subtitles = PermissibleValue(
        text="Subtitles",
        description="FIAF Moving Image Cataloguing Manual D.6",
        meaning=FIAF["Subtitles"])
    SungLanguage = PermissibleValue(
        text="SungLanguage",
        description="FIAF Moving Image Cataloguing Manual D.6",
        meaning=FIAF["SungLanguage"])
    VoiceOver = PermissibleValue(text="VoiceOver")

    _defn = EnumDefinition(
        name="LanguageUsageEnum",
        description="FIAF Moving Image Cataloguing Manual 2.3.3, D.6",
    )

class PrecisionEnum(EnumDefinitionImpl):
    """
    Qualifier indicating the precision of an extent value or duration
    """
    Approximate = PermissibleValue(
        text="Approximate",
        description="Value may be inaccurate but is regarded to be close to the real thing")
    Uncertain = PermissibleValue(
        text="Uncertain",
        description="Sources for the given value are deemed unreliable, so it may as well be off the mark")

    _defn = EnumDefinition(
        name="PrecisionEnum",
        description="Qualifier indicating the precision of an extent value or duration",
    )

class SoundTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual 2.3.4.3, 3.1.5.3, D.7.4
    """
    Combined = PermissibleValue(
        text="Combined",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["Combined"])
    CombinedAsMute = PermissibleValue(
        text="CombinedAsMute",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["CombinedAsMute"])
    CombinedAsSound = PermissibleValue(
        text="CombinedAsSound",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["CombinedAsSound"])
    MixedSound = PermissibleValue(
        text="MixedSound",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["MixedSound"])
    Mute = PermissibleValue(
        text="Mute",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["Mute"])
    Silent = PermissibleValue(
        text="Silent",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["Silent"])
    Sound = PermissibleValue(
        text="Sound",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["Sound"])
    Temporary = PermissibleValue(
        text="Temporary",
        description="FIAF Moving Image Cataloguing Manual D.7.4",
        meaning=FIAF["Temporary"])

    _defn = EnumDefinition(
        name="SoundTypeEnum",
        description="FIAF Moving Image Cataloguing Manual 2.3.4.3, 3.1.5.3, D.7.4",
    )

class TitleTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual A.2
    """
    AbbreviatedTitle = PermissibleValue(
        text="AbbreviatedTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["AbbreviatedTitle"])
    AcquisitionTitle = PermissibleValue(
        text="AcquisitionTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["AcquisitionTitle"])
    AlternativeTitle = PermissibleValue(
        text="AlternativeTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4",
        meaning=FIAF["AlternativeTitle"])
    CorrectedTitle = PermissibleValue(
        text="CorrectedTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["CorrectedTitle"])
    PreReleaseTitle = PermissibleValue(
        text="PreReleaseTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["PreReleaseTitle"])
    PreferredTitle = PermissibleValue(
        text="PreferredTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.0",
        meaning=FIAF["PreferredTitle"])
    SearchTitle = PermissibleValue(
        text="SearchTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["SearchTitle"])
    SeriesTitle = PermissibleValue(
        text="SeriesTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["SeriesTitle"])
    SuppliedDevisedTitle = PermissibleValue(
        text="SuppliedDevisedTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.5",
        meaning=FIAF["SuppliedDevisedTitle"])
    TitleProper = PermissibleValue(
        text="TitleProper",
        description="FIAF Moving Image Cataloguing Manual A.2.2",
        meaning=FIAF["TitleProper"])
    TranslatedTitle = PermissibleValue(
        text="TranslatedTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["TranslatedTitle"])
    TransliteratedTitle = PermissibleValue(
        text="TransliteratedTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["TransliteratedTitle"])
    WorkingTitle = PermissibleValue(
        text="WorkingTitle",
        description="FIAF Moving Image Cataloguing Manual A.2.4.1",
        meaning=FIAF["WorkingTitle"])

    _defn = EnumDefinition(
        name="TitleTypeEnum",
        description="FIAF Moving Image Cataloguing Manual A.2",
    )

class UnitEnum(EnumDefinitionImpl):
    """
    Units of measurement. Definitions are taken from the Quantities, Units, Dimensions and Data Types Ontologies (QUDT)
    """
    Feet = PermissibleValue(
        text="Feet",
        description="Unit of length defined as being 0.3048 metres",
        meaning=UNIT["FT"])
    GigaByte = PermissibleValue(
        text="GigaByte",
        description="Unit for digital information equivalent to 1000 megabytes",
        meaning=UNIT["GigaBYTE"])
    KiloByte = PermissibleValue(
        text="KiloByte",
        description="Unit for digital information equivalent to 1000 bytes",
        meaning=UNIT["KiloBYTE"])
    Metre = PermissibleValue(
        text="Metre",
        description="Metric and SI base unit of distance",
        meaning=UNIT["M"])
    MegaByte = PermissibleValue(
        text="MegaByte",
        description="Unit for digital information equivalent to 1000 kilobytes",
        meaning=UNIT["MegaBYTE"])
    TeraByte = PermissibleValue(
        text="TeraByte",
        description="Unit for digital information equivalent to 1000 gigabytes",
        meaning=UNIT["TeraBYTE"])

    _defn = EnumDefinition(
        name="UnitEnum",
        description="""Units of measurement. Definitions are taken from the Quantities, Units, Dimensions and Data Types Ontologies (QUDT)""",
    )

class VariantTypeEnum(EnumDefinitionImpl):
    """
    FIAF Moving Image Cataloguing Manual D.2
    """
    AbridgedCondensed = PermissibleValue(
        text="AbridgedCondensed",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["AbridgedCondensed"])
    Augmented = PermissibleValue(
        text="Augmented",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["Augmented"])
    BlackAndWhiteCopyOfWorkOriginallyIssuedInColour = PermissibleValue(
        text="BlackAndWhiteCopyOfWorkOriginallyIssuedInColour",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["BlackAndWhiteCopyOfWorkOriginallyIssuedInColour"])
    Censored = PermissibleValue(
        text="Censored",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["Censored"])
    Colourized = PermissibleValue(
        text="Colourized",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["Colourized"])
    DifferentSoundTrack = PermissibleValue(
        text="DifferentSoundTrack",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["DifferentSoundTrack"])
    Dubbed = PermissibleValue(
        text="Dubbed",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["Dubbed"])
    PreservationRestoration = PermissibleValue(
        text="PreservationRestoration",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["PreservationRestoration"])
    Sonorized = PermissibleValue(
        text="Sonorized",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["Sonorized"])
    Subtitled = PermissibleValue(
        text="Subtitled",
        description="FIAF Moving Image Cataloguing Manual D.2",
        meaning=FIAF["Subtitled"])

    _defn = EnumDefinition(
        name="VariantTypeEnum",
        description="FIAF Moving Image Cataloguing Manual D.2",
    )

class WorkVariantTypeEnum(EnumDefinitionImpl):
    """
    Work/Variant description type. See also: FIAF Moving Image Cataloguing Manual 1.2.1, D.1
    """
    Analytic = PermissibleValue(
        text="Analytic",
        description="Content that is contained in another content",
        meaning=FIAF["Analytic"])
    Collection = PermissibleValue(
        text="Collection",
        description="""Content issued in several independent parts; an ‘umbrella’ work title covering a number of different Works/Variants/Manifestations""",
        meaning=FIAF["Collection"])
    Monographic = PermissibleValue(
        text="Monographic",
        description="Complete content in one part or intended to be completed in a finite number of parts",
        meaning=FIAF["Monographic"])
    Serial = PermissibleValue(
        text="Serial",
        description="""Content issued in successive parts and intended to be continued indefinitely, or across a span of time. A Work record for a television series is catalogued as a “Serial”, individual episodes may be catalogued as a Monographic record""",
        meaning=FIAF["Serial"])

    _defn = EnumDefinition(
        name="WorkVariantTypeEnum",
        description="Work/Variant description type. See also: FIAF Moving Image Cataloguing Manual 1.2.1, D.1",
    )

class WorkFormEnum(EnumDefinitionImpl):
    """
    FIAF Glossary of Filmographic Terms D.1.9
    """
    AmateurFilm = PermissibleValue(
        text="AmateurFilm",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["AmateurFilm"])
    Compilation = PermissibleValue(
        text="Compilation",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Compilation"])
    Excerpt = PermissibleValue(
        text="Excerpt",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Excerpt"])
    Feature = PermissibleValue(
        text="Feature",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Feature"])
    Featurette = PermissibleValue(
        text="Featurette",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Featurette"])
    HomeMovie = PermissibleValue(
        text="HomeMovie",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["HomeMovie"])
    Outtake = PermissibleValue(
        text="Outtake",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Outtake"])
    ScreenTest = PermissibleValue(
        text="ScreenTest",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["ScreenTest"])
    Series = PermissibleValue(
        text="Series",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Series"])
    Short = PermissibleValue(
        text="Short",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Short"])
    StockFootage = PermissibleValue(
        text="StockFootage",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["StockFootage"])
    Trailer = PermissibleValue(
        text="Trailer",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["Trailer"])
    UneditedFootage = PermissibleValue(
        text="UneditedFootage",
        description="FIAF Glossary of Filmographic Terms D.1.9",
        meaning=FIAF["UneditedFootage"])
    AnthologyFilm = PermissibleValue(
        text="AnthologyFilm",
        description="FIAF Moving Image Cataloguing Manual E.2.2")
    Commercial = PermissibleValue(
        text="Commercial",
        description="FIAF Moving Image Cataloguing Manual E.2.2")
    EducationalFilm = PermissibleValue(
        text="EducationalFilm",
        description="FIAF Moving Image Cataloguing Manual 0.1.2, D.5.3")
    EssayFilm = PermissibleValue(
        text="EssayFilm",
        description="FIAF Moving Image Cataloguing Manual 0.1.2")
    ExperimentalFilm = PermissibleValue(
        text="ExperimentalFilm",
        description="FIAF Moving Image Cataloguing Manual 0.1.2")
    IndustrialFilm = PermissibleValue(
        text="IndustrialFilm",
        description="FIAF Moving Image Cataloguing Manual D.5.3")
    MusicVideo = PermissibleValue(
        text="MusicVideo",
        description="FIAF Moving Image Cataloguing Manual D.18")
    Newsreel = PermissibleValue(
        text="Newsreel",
        description="http://www.screenonline.org.uk/film/id/476463/index.html")

    _defn = EnumDefinition(
        name="WorkFormEnum",
        description="FIAF Glossary of Filmographic Terms D.1.9",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=AVEFI.id, name="id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.id, domain=None, range=Optional[str])

slots.has_name = Slot(uri=SCHEMA.name, name="has_name", curie=SCHEMA.curie('name'),
                   model_uri=AVEFI.has_name, domain=None, range=str)

slots.has_alternate_name = Slot(uri=SCHEMA.alternateName, name="has_alternate_name", curie=SCHEMA.curie('alternateName'),
                   model_uri=AVEFI.has_alternate_name, domain=None, range=Optional[Union[str, List[str]]])

slots.has_ordering_name = Slot(uri=AVEFI.has_ordering_name, name="has_ordering_name", curie=AVEFI.curie('has_ordering_name'),
                   model_uri=AVEFI.has_ordering_name, domain=None, range=Optional[str])

slots.has_record = Slot(uri=AVEFI.has_record, name="has_record", curie=AVEFI.curie('has_record'),
                   model_uri=AVEFI.has_record, domain=None, range=Optional[Union[dict, MovingImageRecord]])

slots.type = Slot(uri=AVEFI.type, name="type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.type, domain=None, range=Optional[str])

slots.category = Slot(uri=RDF.type, name="category", curie=RDF.curie('type'),
                   model_uri=AVEFI.category, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.same_as = Slot(uri=AVEFI.same_as, name="same_as", curie=AVEFI.curie('same_as'),
                   model_uri=AVEFI.same_as, domain=None, range=Optional[Union[Union[dict, AuthorityResource], List[Union[dict, AuthorityResource]]]])

slots.described_by = Slot(uri=WDRS.describedby, name="described_by", curie=WDRS.curie('describedby'),
                   model_uri=AVEFI.described_by, domain=None, range=Optional[Union[dict, DescriptionResource]])

slots.has_history = Slot(uri=AVEFI.has_history, name="has_history", curie=AVEFI.curie('has_history'),
                   model_uri=AVEFI.has_history, domain=None, range=Optional[Union[str, URI]],
                   pattern=re.compile(r'^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$'))

slots.has_issuer_id = Slot(uri=WDRS.issuedby, name="has_issuer_id", curie=WDRS.curie('issuedby'),
                   model_uri=AVEFI.has_issuer_id, domain=None, range=Union[str, URI],
                   pattern=re.compile(r'^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$'))

slots.has_issuer_name = Slot(uri=DCTERMS.contributor, name="has_issuer_name", curie=DCTERMS.curie('contributor'),
                   model_uri=AVEFI.has_issuer_name, domain=None, range=str)

slots.last_modified = Slot(uri=DCTERMS.modified, name="last_modified", curie=DCTERMS.curie('modified'),
                   model_uri=AVEFI.last_modified, domain=None, range=Union[str, XSDDateTime],
                   pattern=re.compile(r'^2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|\+00:00)$'))

slots.has_event = Slot(uri=AVEFI.has_event, name="has_event", curie=AVEFI.curie('has_event'),
                   model_uri=AVEFI.has_event, domain=None, range=Optional[Union[Union[dict, Event], List[Union[dict, Event]]]])

slots.has_date = Slot(uri=AVEFI.has_date, name="has_date", curie=AVEFI.curie('has_date'),
                   model_uri=AVEFI.has_date, domain=None, range=Optional[str],
                   pattern=re.compile(r'^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$'))

slots.has_activity = Slot(uri=AVEFI.has_activity, name="has_activity", curie=AVEFI.curie('has_activity'),
                   model_uri=AVEFI.has_activity, domain=None, range=Optional[Union[Union[dict, Activity], List[Union[dict, Activity]]]])

slots.has_agent = Slot(uri=AVEFI.has_agent, name="has_agent", curie=AVEFI.curie('has_agent'),
                   model_uri=AVEFI.has_agent, domain=None, range=Union[Union[dict, Agent], List[Union[dict, Agent]]])

slots.located_in = Slot(uri=AVEFI.located_in, name="located_in", curie=AVEFI.curie('located_in'),
                   model_uri=AVEFI.located_in, domain=None, range=Optional[Union[Union[dict, GeographicName], List[Union[dict, GeographicName]]]])

slots.has_duration = Slot(uri=AVEFI.has_duration, name="has_duration", curie=AVEFI.curie('has_duration'),
                   model_uri=AVEFI.has_duration, domain=None, range=Optional[Union[dict, Duration]])

slots.has_extent = Slot(uri=AVEFI.has_extent, name="has_extent", curie=AVEFI.curie('has_extent'),
                   model_uri=AVEFI.has_extent, domain=None, range=Optional[Union[dict, Extent]])

slots.has_unit = Slot(uri=AVEFI.has_unit, name="has_unit", curie=AVEFI.curie('has_unit'),
                   model_uri=AVEFI.has_unit, domain=None, range=Optional[Union[str, "UnitEnum"]])

slots.has_value = Slot(uri=AVEFI.has_value, name="has_value", curie=AVEFI.curie('has_value'),
                   model_uri=AVEFI.has_value, domain=None, range=Optional[Decimal])

slots.has_precision = Slot(uri=AVEFI.has_precision, name="has_precision", curie=AVEFI.curie('has_precision'),
                   model_uri=AVEFI.has_precision, domain=None, range=Optional[Union[str, "PrecisionEnum"]])

slots.has_form = Slot(uri=AVEFI.has_form, name="has_form", curie=AVEFI.curie('has_form'),
                   model_uri=AVEFI.has_form, domain=None, range=Optional[Union[Union[str, "WorkFormEnum"], List[Union[str, "WorkFormEnum"]]]])

slots.has_genre = Slot(uri=AVEFI.has_genre, name="has_genre", curie=AVEFI.curie('has_genre'),
                   model_uri=AVEFI.has_genre, domain=None, range=Optional[Union[Union[dict, Genre], List[Union[dict, Genre]]]])

slots.has_subject = Slot(uri=AVEFI.has_subject, name="has_subject", curie=AVEFI.curie('has_subject'),
                   model_uri=AVEFI.has_subject, domain=None, range=Optional[Union[Union[dict, Subject], List[Union[dict, Subject]]]])

slots.is_variant_of = Slot(uri=AVEFI.is_variant_of, name="is_variant_of", curie=AVEFI.curie('is_variant_of'),
                   model_uri=AVEFI.is_variant_of, domain=None, range=Optional[Union[dict, AVefiResource]])

slots.is_part_of = Slot(uri=AVEFI.is_part_of, name="is_part_of", curie=AVEFI.curie('is_part_of'),
                   model_uri=AVEFI.is_part_of, domain=None, range=Optional[Union[Union[dict, AVefiResource], List[Union[dict, AVefiResource]]]])

slots.variant_type = Slot(uri=AVEFI.variant_type, name="variant_type", curie=AVEFI.curie('variant_type'),
                   model_uri=AVEFI.variant_type, domain=None, range=Optional[Union[str, "VariantTypeEnum"]])

slots.has_colour_type = Slot(uri=AVEFI.has_colour_type, name="has_colour_type", curie=AVEFI.curie('has_colour_type'),
                   model_uri=AVEFI.has_colour_type, domain=None, range=Optional[Union[str, "ColourTypeEnum"]])

slots.has_format = Slot(uri=AVEFI.has_format, name="has_format", curie=AVEFI.curie('has_format'),
                   model_uri=AVEFI.has_format, domain=None, range=Optional[Union[Union[dict, Format], List[Union[dict, Format]]]])

slots.has_item = Slot(uri=AVEFI.has_item, name="has_item", curie=AVEFI.curie('has_item'),
                   model_uri=AVEFI.has_item, domain=None, range=Optional[Union[Union[dict, AVefiResource], List[Union[dict, AVefiResource]]]])

slots.has_note = Slot(uri=AVEFI.has_note, name="has_note", curie=AVEFI.curie('has_note'),
                   model_uri=AVEFI.has_note, domain=None, range=Optional[Union[str, List[str]]])

slots.has_sound_type = Slot(uri=AVEFI.has_sound_type, name="has_sound_type", curie=AVEFI.curie('has_sound_type'),
                   model_uri=AVEFI.has_sound_type, domain=None, range=Optional[Union[str, "SoundTypeEnum"]])

slots.has_webresource = Slot(uri=AVEFI.has_webresource, name="has_webresource", curie=AVEFI.curie('has_webresource'),
                   model_uri=AVEFI.has_webresource, domain=None, range=Optional[Union[str, URI]],
                   pattern=re.compile(r'^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$'))

slots.is_manifestation_of = Slot(uri=AVEFI.is_manifestation_of, name="is_manifestation_of", curie=AVEFI.curie('is_manifestation_of'),
                   model_uri=AVEFI.is_manifestation_of, domain=None, range=Union[Union[dict, AVefiResource], List[Union[dict, AVefiResource]]])

slots.in_language = Slot(uri=AVEFI.in_language, name="in_language", curie=AVEFI.curie('in_language'),
                   model_uri=AVEFI.in_language, domain=None, range=Optional[Union[Union[dict, Language], List[Union[dict, Language]]]])

slots.is_item_of = Slot(uri=AVEFI.is_item_of, name="is_item_of", curie=AVEFI.curie('is_item_of'),
                   model_uri=AVEFI.is_item_of, domain=None, range=Union[dict, AVefiResource])

slots.has_access_status = Slot(uri=AVEFI.has_access_status, name="has_access_status", curie=AVEFI.curie('has_access_status'),
                   model_uri=AVEFI.has_access_status, domain=None, range=Optional[Union[str, "ItemAccessStatusEnum"]])

slots.is_copy_of = Slot(uri=AVEFI.is_copy_of, name="is_copy_of", curie=AVEFI.curie('is_copy_of'),
                   model_uri=AVEFI.is_copy_of, domain=None, range=Optional[Union[Union[dict, AVefiResource], List[Union[dict, AVefiResource]]]])

slots.is_derivative_of = Slot(uri=AVEFI.is_derivative_of, name="is_derivative_of", curie=AVEFI.curie('is_derivative_of'),
                   model_uri=AVEFI.is_derivative_of, domain=None, range=Optional[Union[Union[dict, AVefiResource], List[Union[dict, AVefiResource]]]])

slots.element_type = Slot(uri=AVEFI.element_type, name="element_type", curie=AVEFI.curie('element_type'),
                   model_uri=AVEFI.element_type, domain=None, range=Optional[Union[str, "ItemElementTypeEnum"]])

slots.movingImageRecord__has_alternative_title = Slot(uri=AVEFI.has_alternative_title, name="movingImageRecord__has_alternative_title", curie=AVEFI.curie('has_alternative_title'),
                   model_uri=AVEFI.movingImageRecord__has_alternative_title, domain=None, range=Optional[Union[Union[dict, Title], List[Union[dict, Title]]]])

slots.movingImageRecord__has_primary_title = Slot(uri=AVEFI.has_primary_title, name="movingImageRecord__has_primary_title", curie=AVEFI.curie('has_primary_title'),
                   model_uri=AVEFI.movingImageRecord__has_primary_title, domain=None, range=Union[dict, Title])

slots.language__code = Slot(uri=AVEFI.code, name="language__code", curie=AVEFI.curie('code'),
                   model_uri=AVEFI.language__code, domain=None, range=str,
                   pattern=re.compile(r'^[a-z]{3}$'))

slots.language__usage = Slot(uri=AVEFI.usage, name="language__usage", curie=AVEFI.curie('usage'),
                   model_uri=AVEFI.language__usage, domain=None, range=Union[Union[str, "LanguageUsageEnum"], List[Union[str, "LanguageUsageEnum"]]])

slots.WorkVariant_type = Slot(uri=AVEFI.type, name="WorkVariant_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.WorkVariant_type, domain=WorkVariant, range=Union[str, "WorkVariantTypeEnum"])

slots.Genre_same_as = Slot(uri=AVEFI.same_as, name="Genre_same_as", curie=AVEFI.curie('same_as'),
                   model_uri=AVEFI.Genre_same_as, domain=Genre, range=Optional[Union[Union[dict, "GNDResource"], List[Union[dict, "GNDResource"]]]])

slots.Activity_type = Slot(uri=AVEFI.type, name="Activity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.Activity_type, domain=Activity, range=str)

slots.AnimationActivity_type = Slot(uri=AVEFI.type, name="AnimationActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.AnimationActivity_type, domain=AnimationActivity, range=Union[str, "AnimationActivityTypeEnum"])

slots.CastActivity_type = Slot(uri=AVEFI.type, name="CastActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.CastActivity_type, domain=CastActivity, range=Union[str, "CastActivityTypeEnum"])

slots.CensorshipActivity_type = Slot(uri=AVEFI.type, name="CensorshipActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.CensorshipActivity_type, domain=CensorshipActivity, range=Union[str, "CensorshipActivityTypeEnum"])

slots.CinematographyActivity_type = Slot(uri=AVEFI.type, name="CinematographyActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.CinematographyActivity_type, domain=CinematographyActivity, range=Union[str, "CinematographyActivityTypeEnum"])

slots.CopyrightAndDistributionActivity_type = Slot(uri=AVEFI.type, name="CopyrightAndDistributionActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.CopyrightAndDistributionActivity_type, domain=CopyrightAndDistributionActivity, range=Union[str, "CopyrightAndDistributionActivityTypeEnum"])

slots.DirectingActivity_type = Slot(uri=AVEFI.type, name="DirectingActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.DirectingActivity_type, domain=DirectingActivity, range=Union[str, "DirectingActivityTypeEnum"])

slots.EditingActivity_type = Slot(uri=AVEFI.type, name="EditingActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.EditingActivity_type, domain=EditingActivity, range=Union[str, "EditingActivityTypeEnum"])

slots.LaboratoryActivity_type = Slot(uri=AVEFI.type, name="LaboratoryActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.LaboratoryActivity_type, domain=LaboratoryActivity, range=Union[str, "LaboratoryActivityTypeEnum"])

slots.MusicActivity_type = Slot(uri=AVEFI.type, name="MusicActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.MusicActivity_type, domain=MusicActivity, range=Union[str, "MusicActivityTypeEnum"])

slots.ProducingActivity_type = Slot(uri=AVEFI.type, name="ProducingActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.ProducingActivity_type, domain=ProducingActivity, range=Union[str, "ProducingActivityTypeEnum"])

slots.ProductionDesignActivity_type = Slot(uri=AVEFI.type, name="ProductionDesignActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.ProductionDesignActivity_type, domain=ProductionDesignActivity, range=Union[str, "ProductionDesignActivityTypeEnum"])

slots.PuppetActivity_type = Slot(uri=AVEFI.type, name="PuppetActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.PuppetActivity_type, domain=PuppetActivity, range=Union[str, "PuppetActivityTypeEnum"])

slots.SoundActivity_type = Slot(uri=AVEFI.type, name="SoundActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.SoundActivity_type, domain=SoundActivity, range=Union[str, "SoundActivityTypeEnum"])

slots.SpecialEffectsActivity_type = Slot(uri=AVEFI.type, name="SpecialEffectsActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.SpecialEffectsActivity_type, domain=SpecialEffectsActivity, range=Union[str, "SpecialEffectsActivityTypeEnum"])

slots.WritingActivity_type = Slot(uri=AVEFI.type, name="WritingActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.WritingActivity_type, domain=WritingActivity, range=Union[str, "WritingActivityTypeEnum"])

slots.ManifestationActivity_type = Slot(uri=AVEFI.type, name="ManifestationActivity_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.ManifestationActivity_type, domain=ManifestationActivity, range=Union[str, "ManifestationActivityTypeEnum"])

slots.Agent_has_name = Slot(uri=SCHEMA.name, name="Agent_has_name", curie=SCHEMA.curie('name'),
                   model_uri=AVEFI.Agent_has_name, domain=Agent, range=str)

slots.Agent_type = Slot(uri=AVEFI.type, name="Agent_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.Agent_type, domain=Agent, range=Union[str, "AgentTypeEnum"])

slots.ProductionEvent_has_activity = Slot(uri=AVEFI.has_activity, name="ProductionEvent_has_activity", curie=AVEFI.curie('has_activity'),
                   model_uri=AVEFI.ProductionEvent_has_activity, domain=ProductionEvent, range=Optional[Union[Union[dict, Activity], List[Union[dict, Activity]]]])

slots.ProductionEvent_type = Slot(uri=AVEFI.type, name="ProductionEvent_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.ProductionEvent_type, domain=ProductionEvent, range=Optional[Union[str, "ProductionEventTypeEnum"]])

slots.PreservationEvent_has_activity = Slot(uri=AVEFI.has_activity, name="PreservationEvent_has_activity", curie=AVEFI.curie('has_activity'),
                   model_uri=AVEFI.PreservationEvent_has_activity, domain=PreservationEvent, range=Union[Union[dict, ManifestationActivity], List[Union[dict, ManifestationActivity]]])

slots.PreservationEvent_type = Slot(uri=AVEFI.type, name="PreservationEvent_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.PreservationEvent_type, domain=PreservationEvent, range=Union[str, "PreservationEventTypeEnum"])

slots.PublicationEvent_has_activity = Slot(uri=AVEFI.has_activity, name="PublicationEvent_has_activity", curie=AVEFI.curie('has_activity'),
                   model_uri=AVEFI.PublicationEvent_has_activity, domain=PublicationEvent, range=Optional[Union[Union[dict, ManifestationActivity], List[Union[dict, ManifestationActivity]]]])

slots.PublicationEvent_type = Slot(uri=AVEFI.type, name="PublicationEvent_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.PublicationEvent_type, domain=PublicationEvent, range=Union[str, "PublicationEventTypeEnum"])

slots.ManufactureEvent_has_activity = Slot(uri=AVEFI.has_activity, name="ManufactureEvent_has_activity", curie=AVEFI.curie('has_activity'),
                   model_uri=AVEFI.ManufactureEvent_has_activity, domain=ManufactureEvent, range=Union[Union[dict, LaboratoryActivity], List[Union[dict, LaboratoryActivity]]])

slots.ManufactureEvent_type = Slot(uri=AVEFI.type, name="ManufactureEvent_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.ManufactureEvent_type, domain=ManufactureEvent, range=Union[str, "ManufactureEventTypeEnum"])

slots.RightsCopyrightRegistrationEvent_has_activity = Slot(uri=AVEFI.has_activity, name="RightsCopyrightRegistrationEvent_has_activity", curie=AVEFI.curie('has_activity'),
                   model_uri=AVEFI.RightsCopyrightRegistrationEvent_has_activity, domain=RightsCopyrightRegistrationEvent, range=Union[Union[dict, CopyrightAndDistributionActivity], List[Union[dict, CopyrightAndDistributionActivity]]])

slots.Title_has_name = Slot(uri=SCHEMA.name, name="Title_has_name", curie=SCHEMA.curie('name'),
                   model_uri=AVEFI.Title_has_name, domain=Title, range=str)

slots.Title_type = Slot(uri=AVEFI.type, name="Title_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.Title_type, domain=Title, range=Union[str, "TitleTypeEnum"])

slots.Duration_has_value = Slot(uri=AVEFI.has_value, name="Duration_has_value", curie=AVEFI.curie('has_value'),
                   model_uri=AVEFI.Duration_has_value, domain=Duration, range=Optional[str],
                   pattern=re.compile(r'^PT(([1-9][0-9]*H)?(([1-5][0-9]|[1-9])M)?([1-5][0-9]|[1-9])S|([1-9][0-9]*H)?([1-5][0-9]|[1-9])M|[1-9][0-9]*H)$'))

slots.Audio_type = Slot(uri=AVEFI.type, name="Audio_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.Audio_type, domain=Audio, range=Optional[Union[str, "FormatAudioTypeEnum"]])

slots.DigitalFile_type = Slot(uri=AVEFI.type, name="DigitalFile_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.DigitalFile_type, domain=DigitalFile, range=Optional[Union[str, "FormatDigitalFileTypeEnum"]])

slots.DigitalFileEncoding_type = Slot(uri=AVEFI.type, name="DigitalFileEncoding_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.DigitalFileEncoding_type, domain=DigitalFileEncoding, range=Optional[Union[str, "FormatDigitalFileEncodingTypeEnum"]])

slots.Film_type = Slot(uri=AVEFI.type, name="Film_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.Film_type, domain=Film, range=Optional[Union[str, "FormatFilmTypeEnum"]])

slots.Optical_type = Slot(uri=AVEFI.type, name="Optical_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.Optical_type, domain=Optical, range=Optional[Union[str, "FormatOpticalTypeEnum"]])

slots.Video_type = Slot(uri=AVEFI.type, name="Video_type", curie=AVEFI.curie('type'),
                   model_uri=AVEFI.Video_type, domain=Video, range=Optional[Union[str, "FormatVideoTypeEnum"]])

slots.Manifestation_same_as = Slot(uri=AVEFI.same_as, name="Manifestation_same_as", curie=AVEFI.curie('same_as'),
                   model_uri=AVEFI.Manifestation_same_as, domain=Manifestation, range=Optional[Union[Union[dict, "AVefiResource"], List[Union[dict, "AVefiResource"]]]])

slots.AuthorityResource_id = Slot(uri=AVEFI.id, name="AuthorityResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.AuthorityResource_id, domain=AuthorityResource, range=str)

slots.AVefiResource_id = Slot(uri=AVEFI.id, name="AVefiResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.AVefiResource_id, domain=AVefiResource, range=str,
                   pattern=re.compile(r'^21(\.([0-9A-Za-z])+)*/[!-~]+$'))

slots.DOIResource_id = Slot(uri=AVEFI.id, name="DOIResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.DOIResource_id, domain=DOIResource, range=str,
                   pattern=re.compile(r'^10\.[0-9]{4,9}(\.[0-9]+)*(/|%2F)((?![\"&\'])\S)+$'))

slots.FilmportalResource_id = Slot(uri=AVEFI.id, name="FilmportalResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.FilmportalResource_id, domain=FilmportalResource, range=str,
                   pattern=re.compile(r'^[\da-f]{32}$'))

slots.GNDResource_id = Slot(uri=AVEFI.id, name="GNDResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.GNDResource_id, domain=GNDResource, range=str,
                   pattern=re.compile(r'^[-\dX]+$'))

slots.ISILResource_id = Slot(uri=AVEFI.id, name="ISILResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.ISILResource_id, domain=ISILResource, range=str,
                   pattern=re.compile(r'^[A-Z]{2}-[A-Za-z\-0-9:/]{1,15}$'))

slots.TGNResource_id = Slot(uri=AVEFI.id, name="TGNResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.TGNResource_id, domain=TGNResource, range=str,
                   pattern=re.compile(r'^[1-9][0-9]{6}$'))

slots.VIAFResource_id = Slot(uri=AVEFI.id, name="VIAFResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.VIAFResource_id, domain=VIAFResource, range=str,
                   pattern=re.compile(r'^\d+$'))

slots.WikidataResource_id = Slot(uri=AVEFI.id, name="WikidataResource_id", curie=AVEFI.curie('id'),
                   model_uri=AVEFI.WikidataResource_id, domain=WikidataResource, range=str,
                   pattern=re.compile(r'^[LPQ]\d+$'))