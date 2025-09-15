```mermaid
erDiagram
Activity {
    IDString type  
    AVefiCurie category  
}
Agent {
    TextLineList has_alternate_name  
    TextLine has_name  
    AgentTypeEnum type  
    AVefiCurie category  
}
AuthorityResource {
    IDString id  
    AVefiCurie category  
}
CategorizedThing {
    AVefiCurie category  
}
DescriptionResource {
    HttpUri has_history  
    HttpUri has_issuer_id  
    TextLine has_issuer_name  
    IDStringList has_source_key  
    ISODateTimeUTC last_modified  
}
Duration {
    ISODurationInHours has_value  
    PrecisionEnum has_precision  
}
Event {
    ISODate has_date  
    AVefiCurie category  
}
Extent {
    UnitEnum has_unit  
    Decimal has_value  
    PrecisionEnum has_precision  
}
Format {
    IDString type  
    AVefiCurie category  
}
GNDResource {
    GNDID id  
    AVefiCurie category  
}
Genre {
    TextLineList has_alternate_name  
    TextLine has_name  
}
GeographicName {
    TextLineList has_alternate_name  
    TextLine has_name  
    AVefiCurie category  
}
Item {
    ItemElementTypeEnum element_type  
    ItemAccessStatusEnum has_access_status  
    ColourTypeEnum has_colour_type  
    FrameRateEnum has_frame_rate  
    SoundTypeEnum has_sound_type  
    TextAreaList has_note  
    HttpUriList has_webresource  
    AVefiCurie category  
}
Language {
    LanguageCodeEnum code  
    LanguageUsageEnumList usage  
}
Manifestation {
    TextAreaList has_note  
    HttpUriList has_webresource  
    AVefiCurie category  
}
MovingImageResource {
    IDString id  
    AVefiCurie category  
}
Title {
    TextLine has_name  
    TextLine has_ordering_name  
    TitleTypeEnum type  
}
WorkVariant {
    WorkFormEnumList has_form  
    WorkVariantTypeEnum type  
    VariantTypeEnum variant_type  
    AVefiCurie category  
}

Activity ||--}| Agent : "has_agent"
Agent ||--}o AuthorityResource : "same_as"
Event ||--}o Activity : "has_activity"
Event ||--}o GeographicName : "located_in"
Genre ||--}o GNDResource : "same_as"
GeographicName ||--}o AuthorityResource : "same_as"
Item ||--|o DescriptionResource : "described_by"
Item ||--|o Duration : "has_duration"
Item ||--|o Extent : "has_extent"
Item ||--|o Title : "has_primary_title"
Item ||--|| MovingImageResource : "is_item_of"
Item ||--}o AuthorityResource : "is_copy_of"
Item ||--}o AuthorityResource : "same_as"
Item ||--}o Event : "has_event"
Item ||--}o Format : "has_format"
Item ||--}o Language : "in_language"
Item ||--}o MovingImageResource : "has_identifier"
Item ||--}o MovingImageResource : "is_derivative_of"
Item ||--}o Title : "has_alternative_title"
Manifestation ||--|o DescriptionResource : "described_by"
Manifestation ||--|o Title : "has_primary_title"
Manifestation ||--}o AuthorityResource : "same_as"
Manifestation ||--}o Event : "has_event"
Manifestation ||--}o MovingImageResource : "has_identifier"
Manifestation ||--}o MovingImageResource : "has_item"
Manifestation ||--}o Title : "has_alternative_title"
Manifestation ||--}| MovingImageResource : "is_manifestation_of"
WorkVariant ||--|o MovingImageResource : "is_variant_of"
WorkVariant ||--|| Title : "has_primary_title"
WorkVariant ||--}o AuthorityResource : "same_as"
WorkVariant ||--}o CategorizedThing : "has_subject"
WorkVariant ||--}o DescriptionResource : "described_by"
WorkVariant ||--}o Event : "has_event"
WorkVariant ||--}o Genre : "has_genre"
WorkVariant ||--}o MovingImageResource : "has_identifier"
WorkVariant ||--}o MovingImageResource : "is_part_of"
WorkVariant ||--}o Title : "has_alternative_title"

```

