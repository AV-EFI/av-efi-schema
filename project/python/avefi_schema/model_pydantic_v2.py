from __future__ import annotations 
from datetime import (
    datetime,
    date
)
from decimal import Decimal 
from enum import Enum 
import re
import sys
from typing import (
    Any,
    List,
    Literal,
    Dict,
    Optional,
    Union
)
from pydantic.version import VERSION  as PYDANTIC_VERSION 
if int(PYDANTIC_VERSION[0])>=2:
    from pydantic import (
        BaseModel,
        ConfigDict,
        Field,
        field_validator
    )
else:
    from pydantic import (
        BaseModel,
        Field,
        validator
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
    # FIAF Moving Image Cataloguing Manual D.7.2
    MOV = "MOV"
    # FIAF Moving Image Cataloguing Manual D.7.2
    MP4 = "MP4"
    # FIAF Moving Image Cataloguing Manual D.7.2
    MXF = "MXF"


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
    # FIAF Moving Image Cataloguing Manual D.7.2
    DVCPROHD = "DVCPROHD"
    # FIAF Moving Image Cataloguing Manual D.7.2
    DigitalBetacam = "DigitalBetacam"
    # FIAF Moving Image Cataloguing Manual D.7.2
    HDCAMSR = "HDCAMSR"


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
    # FIAF Moving Image Cataloguing Manual D.7.8
    DCP = "DCP"
    # FIAF Moving Image Cataloguing Manual D.7.8
    DirectBWPositive = "DirectBWPositive"
    # FIAF Moving Image Cataloguing Manual D.7.8
    DuplicateNegative = "DuplicateNegative"
    # FIAF Moving Image Cataloguing Manual D.7.8
    DuplicatePositive = "DuplicatePositive"
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
    FIAF Glossary of Filmographic Terms D.1.9
    """
    # FIAF Glossary of Filmographic Terms D.1.9
    AmateurFilm = "AmateurFilm"
    # FIAF Glossary of Filmographic Terms D.1.9
    Compilation = "Compilation"
    # FIAF Glossary of Filmographic Terms D.1.9
    Excerpt = "Excerpt"
    # FIAF Glossary of Filmographic Terms D.1.9
    Feature = "Feature"
    # FIAF Glossary of Filmographic Terms D.1.9
    Featurette = "Featurette"
    # FIAF Glossary of Filmographic Terms D.1.9
    HomeMovie = "HomeMovie"
    # FIAF Glossary of Filmographic Terms D.1.9
    Outtake = "Outtake"
    # FIAF Glossary of Filmographic Terms D.1.9
    ScreenTest = "ScreenTest"
    # FIAF Glossary of Filmographic Terms D.1.9
    Series = "Series"
    # FIAF Glossary of Filmographic Terms D.1.9
    Short = "Short"
    # FIAF Glossary of Filmographic Terms D.1.9
    StockFootage = "StockFootage"
    # FIAF Glossary of Filmographic Terms D.1.9
    Trailer = "Trailer"
    # FIAF Glossary of Filmographic Terms D.1.9
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
    category: Literal["https://av-efi.net/av-efi-schema/CategorizedThing","avefi:CategorizedThing"] = Field("avefi:CategorizedThing", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class PIDRecord(CategorizedThing):
    """
    Grouping for all entities that represent a PID metadata record
    """
    id: Optional[str] = Field(None, description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/PIDRecord","avefi:PIDRecord"] = Field("avefi:PIDRecord", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class MovingImageRecord(PIDRecord):
    described_by: Optional[DescriptionResource] = Field(None, description="""Also record some metadata about the PID itself rather than the identified object""")
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default_factory=list, description="""Associate event(s) with a moving image record""")
    in_language: Optional[List[Language]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""")
    has_alternative_title: Optional[List[Title]] = Field(default_factory=list, description="""Additional title(s) associated with the work / variant, manifestation, or item.""")
    has_primary_title: Title = Field(..., description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""")
    id: Optional[str] = Field(None, description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/MovingImageRecord","avefi:MovingImageRecord"] = Field("avefi:MovingImageRecord", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class DescriptionResource(ConfiguredBaseModel):
    """
    Metadata about the PID rather than the identified object, i.e. who modified the PID metadata record when, making what changes
    """
    has_history: Optional[str] = Field(None, description="""Link to revision history of this PID""")
    has_issuer_id: str = Field(..., description="""Identifier for the responsible party as an URI suitable for linked data""")
    has_issuer_name: str = Field(..., description="""Name of the responsible party""")
    last_modified: datetime  = Field(..., description="""Timestamp (in UTC) for the latest modification to any field in the PID metadata record""")

    @field_validator('has_history')
    def pattern_has_history(cls, v):
        pattern=re.compile(r"^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_history format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_history format: {v}")
        return v

    @field_validator('has_issuer_id')
    def pattern_has_issuer_id(cls, v):
        pattern=re.compile(r"^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_issuer_id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_issuer_id format: {v}")
        return v

    @field_validator('last_modified')
    def pattern_last_modified(cls, v):
        pattern=re.compile(r"^2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?(Z|\+00:00)$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid last_modified format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid last_modified format: {v}")
        return v


class WorkVariant(MovingImageRecord):
    """
    FIAF Moving Image Cataloguing Manual 1.0
    """
    has_form: Optional[List[WorkFormEnum]] = Field(default_factory=list, description="""Form describes the format and/or purpose of a Work, e.g., “non-fiction”, “short” and “animation”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.1""")
    has_genre: Optional[List[Genre]] = Field(default_factory=list, description="""Genre describes categories of Works, characterized by similar plots, themes, settings, situations, and characters. Examples of genres are “westerns” and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.1""")
    has_subject: Optional[List[Subject]] = Field(default_factory=list, description="""Subject descriptor terms for the content of a film specifying its period, themes, locations, etc. Not to be confused with Genre. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.3""")
    is_part_of: Optional[List[AVefiResource]] = Field(default_factory=list, description="""Relate, for instance, episodes to a series / serial. See also: FIAF Moving Image Cataloguing Manual D.17""")
    is_variant_of: Optional[AVefiResource] = Field(None, description="""Link to the reference WorkVariant for the currently described variant. See also: FIAF Moving Image Cataloguing Manual 1.0.2, 1.1.2, 1.4.5""")
    same_as: Optional[List[Union[AuthorityResource,AVefiResource,DOIResource,FilmportalResource,GNDResource,ISILResource,TGNResource,VIAFResource,WikidataResource]]] = Field(default_factory=list, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""")
    type: WorkVariantTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    variant_type: Optional[VariantTypeEnum] = Field(None, description="""FIAF Moving Image Cataloguing Manual D.2""")
    described_by: Optional[DescriptionResource] = Field(None, description="""Also record some metadata about the PID itself rather than the identified object""")
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default_factory=list, description="""Associate event(s) with a moving image record""")
    in_language: Optional[List[Language]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""")
    has_alternative_title: Optional[List[Title]] = Field(default_factory=list, description="""Additional title(s) associated with the work / variant, manifestation, or item.""")
    has_primary_title: Title = Field(..., description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""")
    id: Optional[str] = Field(None, description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/WorkVariant","avefi:WorkVariant"] = Field("avefi:WorkVariant", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class GeographicName(ConfiguredBaseModel):
    """
    Name of country, region or other location. Names should be taken from appropriate authorities (e.g. GND) and recorded as a human readable string in the name attribute and as linked data in the same_as attribute. See also: FIAF Moving Image Cataloguing Manual 1.3.3, D.4
    """
    has_alternate_name: Optional[List[str]] = Field(default_factory=list)
    has_name: str = Field(..., description="""A human-readable name for a thing""")
    same_as: Optional[List[Union[AuthorityResource,AVefiResource,DOIResource,FilmportalResource,GNDResource,ISILResource,TGNResource,VIAFResource,WikidataResource]]] = Field(default_factory=list, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""")


class Genre(ConfiguredBaseModel):
    """
    Genre describes categories of Works, characterized by similar plots, themes, settings, situations, and characters. Examples of genres are “westerns” and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.1
    """
    has_alternate_name: Optional[List[str]] = Field(default_factory=list)
    has_name: str = Field(..., description="""A human-readable name for a thing""")
    same_as: Optional[List[GNDResource]] = Field(default_factory=list, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""")


class Subject(ConfiguredBaseModel):
    """
    Subject descriptor terms for the content of a film specifying its period, themes, locations, etc. Not to be confused with Genre. Provide name and if at all possible identifier(s) from supported authorities in the same_as slot. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.3
    """
    has_alternate_name: Optional[List[str]] = Field(default_factory=list)
    has_name: str = Field(..., description="""A human-readable name for a thing""")
    same_as: Optional[List[Union[AuthorityResource,AVefiResource,DOIResource,FilmportalResource,GNDResource,ISILResource,TGNResource,VIAFResource,WikidataResource]]] = Field(default_factory=list, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""")


class Activity(CategorizedThing):
    """
    FIAF Moving Image Cataloguing Manual 1.4.1.1
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: str = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/Activity","avefi:Activity"] = Field("avefi:Activity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class AnimationActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.13
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: AnimationActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/AnimationActivity","avefi:AnimationActivity"] = Field("avefi:AnimationActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class CastActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.7
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: CastActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/CastActivity","avefi:CastActivity"] = Field("avefi:CastActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class CensorshipActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.1
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: CensorshipActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/CensorshipActivity","avefi:CensorshipActivity"] = Field("avefi:CensorshipActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class CinematographyActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.5
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: CinematographyActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/CinematographyActivity","avefi:CinematographyActivity"] = Field("avefi:CinematographyActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class CopyrightAndDistributionActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms C.2
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: CopyrightAndDistributionActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/CopyrightAndDistributionActivity","avefi:CopyrightAndDistributionActivity"] = Field("avefi:CopyrightAndDistributionActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class DirectingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.3
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: DirectingActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/DirectingActivity","avefi:DirectingActivity"] = Field("avefi:DirectingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class EditingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.10
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: EditingActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/EditingActivity","avefi:EditingActivity"] = Field("avefi:EditingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class LaboratoryActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.12
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: LaboratoryActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/LaboratoryActivity","avefi:LaboratoryActivity"] = Field("avefi:LaboratoryActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class MusicActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.11
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: MusicActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/MusicActivity","avefi:MusicActivity"] = Field("avefi:MusicActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class ProducingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.2
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: ProducingActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/ProducingActivity","avefi:ProducingActivity"] = Field("avefi:ProducingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class ProductionDesignActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.6
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: ProductionDesignActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/ProductionDesignActivity","avefi:ProductionDesignActivity"] = Field("avefi:ProductionDesignActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class PuppetActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.14
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: PuppetActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/PuppetActivity","avefi:PuppetActivity"] = Field("avefi:PuppetActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class SoundActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.9
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: SoundActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/SoundActivity","avefi:SoundActivity"] = Field("avefi:SoundActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class SpecialEffectsActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.8
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: SpecialEffectsActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/SpecialEffectsActivity","avefi:SpecialEffectsActivity"] = Field("avefi:SpecialEffectsActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class WritingActivity(Activity):
    """
    Activity types / roles. See also: FIAF Glossary of Filmographic Terms B.4
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: WritingActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/WritingActivity","avefi:WritingActivity"] = Field("avefi:WritingActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class ManifestationActivity(Activity):
    """
    Activity types / roles. See also: FIAF Moving Image Cataloguing Manual 2.4.1.1, D.8
    """
    has_agent: List[Agent] = Field(default_factory=list, description="""Agent involved in some activity related to the moving image resource""")
    type: ManifestationActivityTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/ManifestationActivity","avefi:ManifestationActivity"] = Field("avefi:ManifestationActivity", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class Agent(ConfiguredBaseModel):
    """
    Agent involved in some activity related to the moving image resource. For agents of type \"Person\" specify name according to the convention \"family name, given name\"
    """
    has_alternate_name: Optional[List[str]] = Field(default_factory=list)
    has_name: str = Field(..., description="""For natural persons, always use the convention \"family name, given name\"""")
    same_as: Optional[List[Union[AuthorityResource,AVefiResource,DOIResource,FilmportalResource,GNDResource,ISILResource,TGNResource,VIAFResource,WikidataResource]]] = Field(default_factory=list, description="""See [AuthorityResource doucmentation](AuthorityResource.md) for accepted identifiers""")
    type: AgentTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")


class Event(CategorizedThing):
    """
    Significant event in the lifecycle of moving image work / variant, manifestation or item. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country where the principal offices or production facilities of the production company are located for a production event. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual 1.4.2, 2.4.2, 3.3.2
    """
    has_activity: Optional[List[Union[Activity,AnimationActivity,CastActivity,CensorshipActivity,CinematographyActivity,CopyrightAndDistributionActivity,DirectingActivity,EditingActivity,LaboratoryActivity,MusicActivity,ProducingActivity,ProductionDesignActivity,PuppetActivity,SoundActivity,SpecialEffectsActivity,WritingActivity,ManifestationActivity]]] = Field(default_factory=list, description="""Associate activity (and subsequently agents) with event""")
    has_date: Optional[str] = Field(None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See examples and references for more information""")
    located_in: Optional[List[GeographicName]] = Field(default_factory=list)
    category: Literal["https://av-efi.net/av-efi-schema/Event","avefi:Event"] = Field("avefi:Event", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_date')
    def pattern_has_date(cls, v):
        pattern=re.compile(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_date format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_date format: {v}")
        return v


class ProductionEvent(Event):
    """
    Production event of a work/variant (or manifestation produced as a restoration). Provide a date or a period of time via has_date and specify located_in as appropriate, e.g. the country where the principal offices or production facilities of the production company are located. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.3
    """
    type: Optional[ProductionEventTypeEnum] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    has_activity: Optional[List[Union[AnimationActivity, CastActivity, CinematographyActivity, DirectingActivity, EditingActivity, MusicActivity, ProducingActivity, ProductionDesignActivity, PuppetActivity, SoundActivity, SpecialEffectsActivity, WritingActivity]]] = Field(default_factory=list, description="""Associate activity (and subsequently agents) with event""")
    has_date: Optional[str] = Field(None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See examples and references for more information""")
    located_in: Optional[List[GeographicName]] = Field(default_factory=list)
    category: Literal["https://av-efi.net/av-efi-schema/ProductionEvent","avefi:ProductionEvent"] = Field("avefi:ProductionEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_date')
    def pattern_has_date(cls, v):
        pattern=re.compile(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_date format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_date format: {v}")
        return v


class PreservationEvent(Event):
    """
    Preservation event originating a manifestation or possibly a vaniant. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.5
    """
    type: PreservationEventTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    has_activity: List[ManifestationActivity] = Field(default_factory=list, description="""Associate activity (and subsequently agents) with event""")
    has_date: Optional[str] = Field(None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See examples and references for more information""")
    located_in: Optional[List[GeographicName]] = Field(default_factory=list)
    category: Literal["https://av-efi.net/av-efi-schema/PreservationEvent","avefi:PreservationEvent"] = Field("avefi:PreservationEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_date')
    def pattern_has_date(cls, v):
        pattern=re.compile(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_date format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_date format: {v}")
        return v


class PublicationEvent(Event):
    """
    Publication event of a manifestation or possibly the first known publication of a work. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country where the manifestation was published. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.1
    """
    type: PublicationEventTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    has_activity: Optional[List[ManifestationActivity]] = Field(default_factory=list, description="""Associate activity (and subsequently agents) with event""")
    has_date: Optional[str] = Field(None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See examples and references for more information""")
    located_in: Optional[List[GeographicName]] = Field(default_factory=list)
    category: Literal["https://av-efi.net/av-efi-schema/PublicationEvent","avefi:PublicationEvent"] = Field("avefi:PublicationEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_date')
    def pattern_has_date(cls, v):
        pattern=re.compile(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_date format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_date format: {v}")
        return v


class ManufactureEvent(Event):
    """
    Manufacture event of a manifestation. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country where the labratory is located. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.7
    """
    type: ManufactureEventTypeEnum = Field(..., description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    has_activity: List[LaboratoryActivity] = Field(default_factory=list, description="""Associate activity (and subsequently agents) with event""")
    has_date: Optional[str] = Field(None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See examples and references for more information""")
    located_in: Optional[List[GeographicName]] = Field(default_factory=list)
    category: Literal["https://av-efi.net/av-efi-schema/ManufactureEvent","avefi:ManufactureEvent"] = Field("avefi:ManufactureEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_date')
    def pattern_has_date(cls, v):
        pattern=re.compile(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_date format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_date format: {v}")
        return v


class RightsCopyrightRegistrationEvent(Event):
    """
    Copyright and related rights registration event of a manifestation or possibly of a work/variant. Always specify date via has_date. Specify located_in as appropriate, e.g. the country where the copyright was registered. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual D.4.4
    """
    has_activity: List[CopyrightAndDistributionActivity] = Field(default_factory=list, description="""Associate activity (and subsequently agents) with event""")
    has_date: Optional[str] = Field(None, description="""Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See examples and references for more information""")
    located_in: Optional[List[GeographicName]] = Field(default_factory=list)
    category: Literal["https://av-efi.net/av-efi-schema/RightsCopyrightRegistrationEvent","avefi:RightsCopyrightRegistrationEvent"] = Field("avefi:RightsCopyrightRegistrationEvent", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_date')
    def pattern_has_date(cls, v):
        pattern=re.compile(r"^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_date format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_date format: {v}")
        return v


class Title(ConfiguredBaseModel):
    """
    FIAF Moving Image Cataloguing Manual 1.3.2, 2.3.2, 3.1.2
    """
    has_name: str = Field(..., description="""A human-readable name for a thing""")
    has_ordering_name: Optional[str] = Field(None, description="""Provide normalised form, e.g. for sorting by title. Only use this slot if value actually if different from has_name""")
    type: TitleTypeEnum = Field(..., description="""FIAF Moving Image Cataloguing Manual A.2""")


class ManifestationOrItem(MovingImageRecord):
    has_duration: Optional[Duration] = Field(None, description="""Total running time of the described object in ISO 8601 duration format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11""")
    has_extent: Optional[Extent] = Field(None, description="""Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8""")
    has_format: Optional[List[Union[Format,Audio,DigitalFile,DigitalFileEncoding,Film,Optical,Video]]] = Field(default_factory=list)
    has_note: Optional[List[str]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual Appendix B""")
    has_webresource: Optional[str] = Field(None, description="""Link to data provider's own presentation of manifestation or item on the web""")
    described_by: Optional[DescriptionResource] = Field(None, description="""Also record some metadata about the PID itself rather than the identified object""")
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default_factory=list, description="""Associate event(s) with a moving image record""")
    in_language: Optional[List[Language]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""")
    has_alternative_title: Optional[List[Title]] = Field(default_factory=list, description="""Additional title(s) associated with the work / variant, manifestation, or item.""")
    has_primary_title: Title = Field(..., description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""")
    id: Optional[str] = Field(None, description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/ManifestationOrItem","avefi:ManifestationOrItem"] = Field("avefi:ManifestationOrItem", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_webresource')
    def pattern_has_webresource(cls, v):
        pattern=re.compile(r"^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_webresource format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_webresource format: {v}")
        return v


class Duration(ConfiguredBaseModel):
    """
    Total running time of the described object in ISO 8601 duration format. The examples section lists possible values for the has_value slot. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11
    """
    has_value: Optional[str] = Field(None, description="""Value of some quantity""")
    has_precision: Optional[PrecisionEnum] = Field(None, description="""Qualifier indicating the precision of an extent value or duration""")

    @field_validator('has_value')
    def pattern_has_value(cls, v):
        pattern=re.compile(r"^PT(([1-9][0-9]*H)?(([1-5][0-9]|[1-9])M)?([1-5][0-9]|[1-9])S|([1-9][0-9]*H)?([1-5][0-9]|[1-9])M|[1-9][0-9]*H)$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_value format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_value format: {v}")
        return v


class Extent(ConfiguredBaseModel):
    """
    Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8
    """
    has_unit: Optional[UnitEnum] = Field(None, description="""Unit of some quantity""")
    has_value: Optional[Decimal] = Field(None, description="""Value of some quantity""")
    has_precision: Optional[PrecisionEnum] = Field(None, description="""Qualifier indicating the precision of an extent value or duration""")


class Format(CategorizedThing):
    """
    FIAF Moving Image Cataloguing Manual 2.3.4.1, 3.1.5.1
    """
    type: Optional[str] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/Format","avefi:Format"] = Field("avefi:Format", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class Audio(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    type: Optional[FormatAudioTypeEnum] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/Audio","avefi:Audio"] = Field("avefi:Audio", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class DigitalFile(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    type: Optional[FormatDigitalFileTypeEnum] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/DigitalFile","avefi:DigitalFile"] = Field("avefi:DigitalFile", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class DigitalFileEncoding(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    type: Optional[FormatDigitalFileEncodingTypeEnum] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/DigitalFileEncoding","avefi:DigitalFileEncoding"] = Field("avefi:DigitalFileEncoding", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class Film(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    type: Optional[FormatFilmTypeEnum] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/Film","avefi:Film"] = Field("avefi:Film", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class Optical(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    type: Optional[FormatOpticalTypeEnum] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/Optical","avefi:Optical"] = Field("avefi:Optical", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class Video(Format):
    """
    FIAF Moving Image Cataloguing Manual D.7.2
    """
    type: Optional[FormatVideoTypeEnum] = Field(None, description="""See specific class documentation for controlled vocabulary applicable to the type slot, respectively""")
    category: Literal["https://av-efi.net/av-efi-schema/Video","avefi:Video"] = Field("avefi:Video", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class Manifestation(ManifestationOrItem):
    """
    Manifestation as defined in FIAF Moving Image Cataloguing Manual 2.0. Note that manifestation type is recorded as publication event type
    """
    has_colour_type: Optional[ColourTypeEnum] = Field(None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.4, 3.1.5.6, D.7.11""")
    has_item: Optional[List[AVefiResource]] = Field(default_factory=list, description="""Indicate AVefi Items the institution has registered as part of the manifestation""")
    has_sound_type: Optional[SoundTypeEnum] = Field(None, description="""FIAF Moving Image Cataloguing Manual 2.3.4.3, 3.1.5.3, D.7.4""")
    is_manifestation_of: List[AVefiResource] = Field(default_factory=list, description="""Indicate AVefi WorkVariant (possibly more but no less than one) that is subject of the manifestation""")
    same_as: Optional[List[AVefiResource]] = Field(default_factory=list, description="""Link to AVefi resource registered by another data provider indicating that the two manifestations are known to be the same. Use this, for instance, when you have cooperated in making a digital restoration of some film work""")
    has_duration: Optional[Duration] = Field(None, description="""Total running time of the described object in ISO 8601 duration format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11""")
    has_extent: Optional[Extent] = Field(None, description="""Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8""")
    has_format: Optional[List[Union[Format,Audio,DigitalFile,DigitalFileEncoding,Film,Optical,Video]]] = Field(default_factory=list)
    has_note: Optional[List[str]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual Appendix B""")
    has_webresource: Optional[str] = Field(None, description="""Link to data provider's own presentation of manifestation or item on the web""")
    described_by: Optional[DescriptionResource] = Field(None, description="""Also record some metadata about the PID itself rather than the identified object""")
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default_factory=list, description="""Associate event(s) with a moving image record""")
    in_language: Optional[List[Language]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""")
    has_alternative_title: Optional[List[Title]] = Field(default_factory=list, description="""Additional title(s) associated with the work / variant, manifestation, or item.""")
    has_primary_title: Title = Field(..., description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""")
    id: Optional[str] = Field(None, description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/Manifestation","avefi:Manifestation"] = Field("avefi:Manifestation", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_webresource')
    def pattern_has_webresource(cls, v):
        pattern=re.compile(r"^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_webresource format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_webresource format: {v}")
        return v


class Language(ConfiguredBaseModel):
    """
    Provide language code from ISO 639-2 (Part 2: Alpha-3) and a list of language usage terms from our controlled vocabulary. See also: FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3
    """
    code: str = Field(..., description="""[ISO 639-2 code](https://id.loc.gov/vocabulary/iso639-2.html) for the Representation of Names of Languages (Part 2: Alpha-3)""")
    usage: List[LanguageUsageEnum] = Field(default_factory=list)

    @field_validator('code')
    def pattern_code(cls, v):
        pattern=re.compile(r"^[a-z]{3}$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid code format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid code format: {v}")
        return v


class Item(ManifestationOrItem):
    """
    FIAF Moving Image Cataloguing Manual 3.0
    """
    element_type: Optional[ItemElementTypeEnum] = Field(None)
    has_access_status: Optional[ItemAccessStatusEnum] = Field(None)
    is_copy_of: Optional[List[AVefiResource]] = Field(default_factory=list, description="""Link to AVefi item registered by another institution indicating that the two are known to be copies of each other""")
    is_derivative_of: Optional[List[AVefiResource]] = Field(default_factory=list, description="""Link to AVefi item from which this one has been derived in whole or in part, e.g. as a result of a restoration or digitasation project""")
    is_item_of: AVefiResource = Field(..., description="""Indicate AVefi Manifestation the item belongs to. Every item must be associated with a manifestation from the same data provider""")
    has_duration: Optional[Duration] = Field(None, description="""Total running time of the described object in ISO 8601 duration format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11""")
    has_extent: Optional[Extent] = Field(None, description="""Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8""")
    has_format: Optional[List[Union[Format,Audio,DigitalFile,DigitalFileEncoding,Film,Optical,Video]]] = Field(default_factory=list)
    has_note: Optional[List[str]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual Appendix B""")
    has_webresource: Optional[str] = Field(None, description="""Link to data provider's own presentation of manifestation or item on the web""")
    described_by: Optional[DescriptionResource] = Field(None, description="""Also record some metadata about the PID itself rather than the identified object""")
    has_event: Optional[List[Union[Event,ProductionEvent,PreservationEvent,PublicationEvent,ManufactureEvent,RightsCopyrightRegistrationEvent]]] = Field(default_factory=list, description="""Associate event(s) with a moving image record""")
    in_language: Optional[List[Language]] = Field(default_factory=list, description="""FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3""")
    has_alternative_title: Optional[List[Title]] = Field(default_factory=list, description="""Additional title(s) associated with the work / variant, manifestation, or item.""")
    has_primary_title: Title = Field(..., description="""Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead.""")
    id: Optional[str] = Field(None, description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/Item","avefi:Item"] = Field("avefi:Item", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('has_webresource')
    def pattern_has_webresource(cls, v):
        pattern=re.compile(r"^https?://[^/?#]+(/[^?#]*(\?([^#]*))?(#(.*))?)?$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid has_webresource format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid has_webresource format: {v}")
        return v


class MovingImageRecordContainer(ConfiguredBaseModel):
    """
    A holder for MovingImageRecord objects
    """
    has_record: Optional[Union[MovingImageRecord,WorkVariant,ManifestationOrItem,Manifestation,Item]] = Field(None, description="""Root slot holding the moving image metadata record, i.e. metadata describing a work/variant, manifestation or item. See also the Introduction of the FIAF Moving Image Cataloguing Manual""")


class AuthorityResource(CategorizedThing):
    """
    Root class for all identifiers from some kind of authority or public register widely accepted in the community
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/AuthorityResource","avefi:AuthorityResource"] = Field("avefi:AuthorityResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")


class AVefiResource(AuthorityResource):
    """
    Handle with the prefix allocated for AVefi (eventually)
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/AVefiResource","avefi:AVefiResource"] = Field("avefi:AVefiResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^21(\.([0-9A-Za-z])+)*/[!-~]+$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class DOIResource(AuthorityResource):
    """
    Digital Object Identifier maintained by the DOI Foundation and commonly used for scientific publications including films.
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/DOIResource","avefi:DOIResource"] = Field("avefi:DOIResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^10\.[0-9]{4,9}(\.[0-9]+)*(/|%2F)((?![\"&\'])\S)+$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class FilmportalResource(AuthorityResource):
    """
    Identifier of the German Filmportal.de
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/FilmportalResource","avefi:FilmportalResource"] = Field("avefi:FilmportalResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[\da-f]{32}$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class GNDResource(AuthorityResource):
    """
    Gemeinsame Normdatei (GND) identifier maintained by Deutsche Nationalbibliothek (German National Library)
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/GNDResource","avefi:GNDResource"] = Field("avefi:GNDResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[-\dX]+$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class ISILResource(AuthorityResource):
    """
    International Standard Identifier for Libraries and Related Organizations including (film) archives
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/ISILResource","avefi:ISILResource"] = Field("avefi:ISILResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Z]{2}-[A-Za-z\-0-9:/]{1,15}$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class TGNResource(AuthorityResource):
    """
    Getty Thesaurus of Geographic Names ID
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/TGNResource","avefi:TGNResource"] = Field("avefi:TGNResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[1-9][0-9]{6}$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class VIAFResource(AuthorityResource):
    """
    Virtual International Authority File identifier hosted by OCLC. The data is accumulated from various well established authority files from different parts of the world
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/VIAFResource","avefi:VIAFResource"] = Field("avefi:VIAFResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^\d+$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


class WikidataResource(AuthorityResource):
    """
    Identifier for Wikidata entities
    """
    id: str = Field(..., description="""A unique identifier for a thing""")
    category: Literal["https://av-efi.net/av-efi-schema/WikidataResource","avefi:WikidataResource"] = Field("avefi:WikidataResource", description="""Designates type, e.g. to distinguish different identifiers (GNDResource vs. VIAFResource)""")

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[LPQ]\d+$")
        if isinstance(v,list):
            for element in v:
                if not pattern.match(element):
                    raise ValueError(f"Invalid id format: {element}")
        elif isinstance(v,str):
            if not pattern.match(v):
                raise ValueError(f"Invalid id format: {v}")
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
CategorizedThing.model_rebuild()
PIDRecord.model_rebuild()
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
AVefiResource.model_rebuild()
DOIResource.model_rebuild()
FilmportalResource.model_rebuild()
GNDResource.model_rebuild()
ISILResource.model_rebuild()
TGNResource.model_rebuild()
VIAFResource.model_rebuild()
WikidataResource.model_rebuild()
