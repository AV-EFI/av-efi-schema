# Auto generated from av_efi_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-03-13T09:00:33
# Schema: av-efi-schema
#
# id: https://av-efi.net/schema/av-efi-schema
# description: Metadata schema for persistent film identifiers developed in the
#   AVefi project
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
EFI = CurieNamespace('efi', 'https://av-efi.net/schema/av-efi-schema/')
FIAF = CurieNamespace('fiaf', 'https://fiafcore.org/ontology/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = EFI


# Types

# Class references



@dataclass
class Entity(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["Entity"]
    class_class_curie: ClassVar[str] = "efi:Entity"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = EFI.Entity

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
class MovingImageRecord(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["MovingImageRecord"]
    class_class_curie: ClassVar[str] = "efi:MovingImageRecord"
    class_name: ClassVar[str] = "MovingImageRecord"
    class_model_uri: ClassVar[URIRef] = EFI.MovingImageRecord

    has_event: Optional[Union[Union[dict, "Event"], List[Union[dict, "Event"]]]] = empty_list()
    has_title: Optional[Union[Union[dict, "Title"], List[Union[dict, "Title"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_event, list):
            self.has_event = [self.has_event] if self.has_event is not None else []
        self.has_event = [v if isinstance(v, Event) else Event(**as_dict(v)) for v in self.has_event]

        if not isinstance(self.has_title, list):
            self.has_title = [self.has_title] if self.has_title is not None else []
        self.has_title = [v if isinstance(v, Title) else Title(**as_dict(v)) for v in self.has_title]

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


@dataclass
class WorkVariant(MovingImageRecord):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["WorkVariant"]
    class_class_curie: ClassVar[str] = "efi:WorkVariant"
    class_name: ClassVar[str] = "WorkVariant"
    class_model_uri: ClassVar[URIRef] = EFI.WorkVariant

    country: Optional[Union[str, List[str]]] = empty_list()
    type: Optional[Union[str, "WorkTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.country, list):
            self.country = [self.country] if self.country is not None else []
        self.country = [v if isinstance(v, str) else str(v) for v in self.country]

        if self.type is not None and not isinstance(self.type, WorkTypeEnum):
            self.type = WorkTypeEnum(self.type)

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


@dataclass
class Activity(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["Activity"]
    class_class_curie: ClassVar[str] = "efi:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = EFI.Activity

    has_agent: Optional[Union[Union[dict, "Agent"], List[Union[dict, "Agent"]]]] = empty_list()
    category: Optional[Union[str, URIorCURIE]] = None
    type: Optional[Union[str, "ActivityTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_agent, list):
            self.has_agent = [self.has_agent] if self.has_agent is not None else []
        self.has_agent = [v if isinstance(v, Agent) else Agent(**as_dict(v)) for v in self.has_agent]

        self.category = str(self.class_class_curie)

        if self.type is not None and not isinstance(self.type, ActivityTypeEnum):
            self.type = ActivityTypeEnum(self.type)

        super().__post_init__(**kwargs)


@dataclass
class Agent(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["Agent"]
    class_class_curie: ClassVar[str] = "efi:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = EFI.Agent

    has_identifier: Optional[Union[Union[dict, "Identifier"], List[Union[dict, "Identifier"]]]] = empty_list()
    name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_identifier, list):
            self.has_identifier = [self.has_identifier] if self.has_identifier is not None else []
        self.has_identifier = [v if isinstance(v, Identifier) else Identifier(**as_dict(v)) for v in self.has_identifier]

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


class CorporateBody(Agent):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["CorporateBody"]
    class_class_curie: ClassVar[str] = "efi:CorporateBody"
    class_name: ClassVar[str] = "CorporateBody"
    class_model_uri: ClassVar[URIRef] = EFI.CorporateBody


    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


@dataclass
class Person(Agent):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["Person"]
    class_class_curie: ClassVar[str] = "efi:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = EFI.Person

    family_name: Optional[str] = None
    given_name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.family_name is not None and not isinstance(self.family_name, str):
            self.family_name = str(self.family_name)

        if self.given_name is not None and not isinstance(self.given_name, str):
            self.given_name = str(self.given_name)

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


@dataclass
class Event(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["Event"]
    class_class_curie: ClassVar[str] = "efi:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = EFI.Event

    has_activity: Optional[Union[Union[dict, Activity], List[Union[dict, Activity]]]] = empty_list()
    date: Optional[str] = None
    type: Optional[Union[str, "EventTypeEnum"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_activity, list):
            self.has_activity = [self.has_activity] if self.has_activity is not None else []
        self.has_activity = [v if isinstance(v, Activity) else Activity(**as_dict(v)) for v in self.has_activity]

        if self.date is not None and not isinstance(self.date, str):
            self.date = str(self.date)

        if self.type is not None and not isinstance(self.type, EventTypeEnum):
            self.type = EventTypeEnum(self.type)

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


class Identifier(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["Identifier"]
    class_class_curie: ClassVar[str] = "efi:Identifier"
    class_name: ClassVar[str] = "Identifier"
    class_model_uri: ClassVar[URIRef] = EFI.Identifier


    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


@dataclass
class Title(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["Title"]
    class_class_curie: ClassVar[str] = "efi:Title"
    class_name: ClassVar[str] = "Title"
    class_model_uri: ClassVar[URIRef] = EFI.Title

    type: Optional[Union[str, "TitleTypeEnum"]] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.type is not None and not isinstance(self.type, TitleTypeEnum):
            self.type = TitleTypeEnum(self.type)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


@dataclass
class MovingImageRecordCollection(Entity):
    """
    A holder for MovingImageRecord objects
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EFI["MovingImageRecordCollection"]
    class_class_curie: ClassVar[str] = "efi:MovingImageRecordCollection"
    class_name: ClassVar[str] = "MovingImageRecordCollection"
    class_model_uri: ClassVar[URIRef] = EFI.MovingImageRecordCollection

    has_record: Optional[Union[Union[dict, MovingImageRecord], List[Union[dict, MovingImageRecord]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_record, list):
            self.has_record = [self.has_record] if self.has_record is not None else []
        self.has_record = [v if isinstance(v, MovingImageRecord) else MovingImageRecord(**as_dict(v)) for v in self.has_record]

        super().__post_init__(**kwargs)
        self.category = str(self.class_class_curie)


# Enumerations
class ActivityTypeEnum(EnumDefinitionImpl):

    Director = PermissibleValue(
        text="Director",
        meaning=FIAF["Director"])
    Producer = PermissibleValue(
        text="Producer",
        meaning=FIAF["Producer"])
    ProductionCompany = PermissibleValue(
        text="ProductionCompany",
        meaning=FIAF["ProductionCompany"])
    ProductionDesigner = PermissibleValue(
        text="ProductionDesigner",
        meaning=FIAF["ProductionDesigner"])
    ProductionManager = PermissibleValue(
        text="ProductionManager",
        meaning=FIAF["ProductionManager"])

    _defn = EnumDefinition(
        name="ActivityTypeEnum",
    )

class EventTypeEnum(EnumDefinitionImpl):

    BroadcastEvent = PermissibleValue(text="BroadcastEvent")
    CastingEvent = PermissibleValue(text="CastingEvent")
    CensorshipEvent = PermissibleValue(text="CensorshipEvent")
    DigitisationEvent = PermissibleValue(text="DigitisationEvent")
    DistributionEvent = PermissibleValue(text="DistributionEvent")
    DonationEvent = PermissibleValue(text="DonationEvent")
    DuplicationEvent = PermissibleValue(text="DuplicationEvent")
    ExchangeEvent = PermissibleValue(text="ExchangeEvent")
    FilmPrintingEvent = PermissibleValue(text="FilmPrintingEvent")
    HomeVideoPublicationEvent = PermissibleValue(text="HomeVideoPublicationEvent")
    IndoorShootingEvent = PermissibleValue(text="IndoorShootingEvent")
    LoanEvent = PermissibleValue(text="LoanEvent")
    MasteringEvent = PermissibleValue(text="MasteringEvent")
    NonTheatricalDistributionEvent = PermissibleValue(text="NonTheatricalDistributionEvent")
    NotForReleaseEvent = PermissibleValue(text="NotForReleaseEvent")
    OffAirRecordingEvent = PermissibleValue(text="OffAirRecordingEvent")
    OnlineTransmissionEvent = PermissibleValue(text="OnlineTransmissionEvent")
    OutdoorShootingEvent = PermissibleValue(text="OutdoorShootingEvent")
    PostProductionEvent = PermissibleValue(text="PostProductionEvent")
    PreReleaseEvent = PermissibleValue(text="PreReleaseEvent")
    PurchaseEvent = PermissibleValue(text="PurchaseEvent")
    RatingEvent = PermissibleValue(text="RatingEvent")
    ReleaseEvent = PermissibleValue(text="ReleaseEvent")
    ReproductionEvent = PermissibleValue(text="ReproductionEvent")
    RevisionEvent = PermissibleValue(text="RevisionEvent")
    RightsCopyrightRegistrationEvent = PermissibleValue(text="RightsCopyrightRegistrationEvent")
    ScanningEvent = PermissibleValue(text="ScanningEvent")
    TelecineEvent = PermissibleValue(text="TelecineEvent")
    TheatricalDistributionEvent = PermissibleValue(text="TheatricalDistributionEvent")
    TransferEvent = PermissibleValue(text="TransferEvent")
    UnknownEvent = PermissibleValue(text="UnknownEvent")
    UploadingEvent = PermissibleValue(text="UploadingEvent")
    VideoCopyingEvent = PermissibleValue(text="VideoCopyingEvent")
    InspectionEvent = PermissibleValue(text="InspectionEvent")
    AwardsOrNominationsEvent = PermissibleValue(text="AwardsOrNominationsEvent")
    PreservationEvent = PermissibleValue(text="PreservationEvent")
    ProductionEvent = PermissibleValue(text="ProductionEvent")
    AcquisitionEvent = PermissibleValue(text="AcquisitionEvent")
    DecisionEvent = PermissibleValue(text="DecisionEvent")
    ManufactureEvent = PermissibleValue(text="ManufactureEvent")
    PublicationEvent = PermissibleValue(text="PublicationEvent")

    _defn = EnumDefinition(
        name="EventTypeEnum",
    )

class TitleTypeEnum(EnumDefinitionImpl):

    AbbreviatedTitle = PermissibleValue(text="AbbreviatedTitle")
    AcquisitionTitle = PermissibleValue(text="AcquisitionTitle")
    CorrectedTitle = PermissibleValue(text="CorrectedTitle")
    IdentifyingTitle = PermissibleValue(text="IdentifyingTitle")
    ParallelTitle = PermissibleValue(text="ParallelTitle")
    PreferredTitle = PermissibleValue(text="PreferredTitle")
    PreReleaseTitle = PermissibleValue(text="PreReleaseTitle")
    SearchTitle = PermissibleValue(text="SearchTitle")
    SuppliedDevisedTitle = PermissibleValue(text="SuppliedDevisedTitle")
    TranslatedTitle = PermissibleValue(text="TranslatedTitle")
    TransliteratedTitle = PermissibleValue(text="TransliteratedTitle")
    WorkingTitle = PermissibleValue(text="WorkingTitle")

    _defn = EnumDefinition(
        name="TitleTypeEnum",
    )

class WorkTypeEnum(EnumDefinitionImpl):

    Analytic = PermissibleValue(text="Analytic")
    Collection = PermissibleValue(text="Collection")
    Monographic = PermissibleValue(text="Monographic")
    Serial = PermissibleValue(text="Serial")

    _defn = EnumDefinition(
        name="WorkTypeEnum",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=EFI.id, domain=None, range=URIRef)

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=EFI.name, domain=None, range=Optional[str])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=EFI.description, domain=None, range=Optional[str])

slots.has_record = Slot(uri=EFI.has_record, name="has_record", curie=EFI.curie('has_record'),
                   model_uri=EFI.has_record, domain=None, range=Optional[Union[Union[dict, MovingImageRecord], List[Union[dict, MovingImageRecord]]]])

slots.type = Slot(uri=EFI.type, name="type", curie=EFI.curie('type'),
                   model_uri=EFI.type, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.category = Slot(uri=RDF.type, name="category", curie=RDF.curie('type'),
                   model_uri=EFI.category, domain=None, range=Optional[Union[str, URIorCURIE]])

slots.has_event = Slot(uri=EFI.has_event, name="has_event", curie=EFI.curie('has_event'),
                   model_uri=EFI.has_event, domain=None, range=Optional[Union[Union[dict, Event], List[Union[dict, Event]]]])

slots.date = Slot(uri=EFI.date, name="date", curie=EFI.curie('date'),
                   model_uri=EFI.date, domain=None, range=Optional[str])

slots.has_activity = Slot(uri=EFI.has_activity, name="has_activity", curie=EFI.curie('has_activity'),
                   model_uri=EFI.has_activity, domain=None, range=Optional[Union[Union[dict, Activity], List[Union[dict, Activity]]]])

slots.has_agent = Slot(uri=EFI.has_agent, name="has_agent", curie=EFI.curie('has_agent'),
                   model_uri=EFI.has_agent, domain=None, range=Optional[Union[Union[dict, Agent], List[Union[dict, Agent]]]])

slots.family_name = Slot(uri=EFI.family_name, name="family_name", curie=EFI.curie('family_name'),
                   model_uri=EFI.family_name, domain=None, range=Optional[str])

slots.given_name = Slot(uri=EFI.given_name, name="given_name", curie=EFI.curie('given_name'),
                   model_uri=EFI.given_name, domain=None, range=Optional[str])

slots.country = Slot(uri=EFI.country, name="country", curie=EFI.curie('country'),
                   model_uri=EFI.country, domain=None, range=Optional[Union[str, List[str]]])

slots.has_identifier = Slot(uri=EFI.has_identifier, name="has_identifier", curie=EFI.curie('has_identifier'),
                   model_uri=EFI.has_identifier, domain=None, range=Optional[Union[Union[dict, Identifier], List[Union[dict, Identifier]]]])

slots.has_title = Slot(uri=EFI.has_title, name="has_title", curie=EFI.curie('has_title'),
                   model_uri=EFI.has_title, domain=None, range=Optional[Union[Union[dict, Title], List[Union[dict, Title]]]])

slots.value = Slot(uri=EFI.value, name="value", curie=EFI.curie('value'),
                   model_uri=EFI.value, domain=None, range=Optional[str])

slots.WorkVariant_type = Slot(uri=EFI.type, name="WorkVariant_type", curie=EFI.curie('type'),
                   model_uri=EFI.WorkVariant_type, domain=WorkVariant, range=Optional[Union[str, "WorkTypeEnum"]])

slots.Activity_type = Slot(uri=EFI.type, name="Activity_type", curie=EFI.curie('type'),
                   model_uri=EFI.Activity_type, domain=Activity, range=Optional[Union[str, "ActivityTypeEnum"]])

slots.Event_type = Slot(uri=EFI.type, name="Event_type", curie=EFI.curie('type'),
                   model_uri=EFI.Event_type, domain=Event, range=Optional[Union[str, "EventTypeEnum"]])

slots.Title_type = Slot(uri=EFI.type, name="Title_type", curie=EFI.curie('type'),
                   model_uri=EFI.Title_type, domain=Title, range=Optional[Union[str, "TitleTypeEnum"]])
