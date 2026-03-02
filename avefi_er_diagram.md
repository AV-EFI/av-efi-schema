```mermaid
erDiagram
Activity {
    IDString type  
    AVefiCurie category  
}
Agent {
    TextLine has_name  
    AgentTypeEnum type  
    TextLineList has_alternate_name  
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
    IDStringList has_source_key  
    HttpUri has_history  
    HttpUri has_issuer_id  
    TextLine has_issuer_name  
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
    Decimal has_value  
    PrecisionEnum has_precision  
    UnitEnum has_unit  
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
    TextLine has_name  
    TextLineList has_alternate_name  
}
GeographicName {
    TextLine has_name  
    TextLineList has_alternate_name  
    AVefiCurie category  
}
Item {
    ColourTypeEnum has_colour_type  
    SoundTypeEnum has_sound_type  
    ItemElementTypeEnum element_type  
    ItemAccessStatusEnum has_access_status  
    FrameRateEnum has_frame_rate  
    AVefiCurie category  
    HttpUriList has_webresource  
    TextAreaList has_note  
}
Language {
    LanguageCodeEnum code  
    LanguageUsageEnumList usage  
}
Manifestation {
    AVefiCurie category  
    HttpUriList has_webresource  
    TextAreaList has_note  
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
    WorkVariantTypeEnum type  
    WorkFormEnumList has_form  
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
Item ||--}o AuthorityResource : "is_copy_of, same_as"
Item ||--}o Event : "has_event"
Item ||--}o Format : "has_format"
Item ||--}o Language : "in_language"
Item ||--}o MovingImageResource : "has_identifier, is_derivative_of"
Item ||--}o Title : "has_alternative_title"
Manifestation ||--|o DescriptionResource : "described_by"
Manifestation ||--|o Title : "has_primary_title"
Manifestation ||--}o AuthorityResource : "same_as"
Manifestation ||--}o Event : "has_event"
Manifestation ||--}o MovingImageResource : "has_identifier, has_item"
Manifestation ||--}o Title : "has_alternative_title"
Manifestation ||--}| MovingImageResource : "is_manifestation_of"
WorkVariant ||--|o MovingImageResource : "is_variant_of"
WorkVariant ||--|| Title : "has_primary_title"
WorkVariant ||--}o AuthorityResource : "same_as"
WorkVariant ||--}o CategorizedThing : "has_subject"
WorkVariant ||--}o DescriptionResource : "described_by"
WorkVariant ||--}o Event : "has_event"
WorkVariant ||--}o Genre : "has_genre"
WorkVariant ||--}o MovingImageResource : "has_identifier, is_part_of"
WorkVariant ||--}o Title : "has_alternative_title"

```

