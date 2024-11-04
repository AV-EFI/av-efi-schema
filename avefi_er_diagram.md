```mermaid
erDiagram
Item {
    ItemElementTypeEnum element_type  
    ItemAccessStatusEnum has_access_status  
    TextAreaList has_note  
    HttpUriList has_webresource  
    IDStringList has_source_key  
    AVefiCurie category  
}
Title {
    TextLine has_name  
    TextLine has_ordering_name  
    TitleTypeEnum type  
}
Language {
    LanguageCodeEnum code  
    LanguageUsageEnumList usage  
}
MovingImageResource {
    IDString id  
    AVefiCurie category  
}
Event {
    ISODate has_date  
    AVefiCurie category  
}
GeographicName {
    TextLineList has_alternate_name  
    TextLine has_name  
    AVefiCurie category  
}
AuthorityResource {
    IDString id  
    AVefiCurie category  
}
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
DescriptionResource {
    HttpUri has_history  
    HttpUri has_issuer_id  
    TextLine has_issuer_name  
    ISODateTimeUTC last_modified  
}
Format {
    IDString type  
    AVefiCurie category  
}
Extent {
    UnitEnum has_unit  
    Decimal has_value  
    PrecisionEnum has_precision  
}
Duration {
    ISODurationInHours has_value  
    PrecisionEnum has_precision  
}
Manifestation {
    ColourTypeEnum has_colour_type  
    SoundTypeEnum has_sound_type  
    TextAreaList has_note  
    HttpUriList has_webresource  
    IDStringList has_source_key  
    AVefiCurie category  
}
WorkVariant {
    WorkFormEnumList has_form  
    WorkVariantTypeEnum type  
    VariantTypeEnum variant_type  
    IDStringList has_source_key  
    AVefiCurie category  
}
CategorizedThing {
    AVefiCurie category  
}
Genre {
    TextLineList has_alternate_name  
    TextLine has_name  
}
GNDResource {
    GNDID id  
    AVefiCurie category  
}

Item ||--}o AuthorityResource : "is_copy_of"
Item ||--}o MovingImageResource : "is_derivative_of"
Item ||--|| MovingImageResource : "is_item_of"
Item ||--|o Duration : "has_duration"
Item ||--|o Extent : "has_extent"
Item ||--}o Format : "has_format"
Item ||--|o DescriptionResource : "described_by"
Item ||--}o Event : "has_event"
Item ||--}o MovingImageResource : "has_identifier"
Item ||--}o Language : "in_language"
Item ||--}o Title : "has_alternative_title"
Item ||--|| Title : "has_primary_title"
Event ||--}o Activity : "has_activity"
Event ||--}o GeographicName : "located_in"
GeographicName ||--}o AuthorityResource : "same_as"
Activity ||--}| Agent : "has_agent"
Agent ||--}o AuthorityResource : "same_as"
Manifestation ||--}o MovingImageResource : "has_item"
Manifestation ||--}| MovingImageResource : "is_manifestation_of"
Manifestation ||--}o MovingImageResource : "same_as"
Manifestation ||--|o Duration : "has_duration"
Manifestation ||--|o Extent : "has_extent"
Manifestation ||--}o Format : "has_format"
Manifestation ||--|o DescriptionResource : "described_by"
Manifestation ||--}o Event : "has_event"
Manifestation ||--}o MovingImageResource : "has_identifier"
Manifestation ||--}o Language : "in_language"
Manifestation ||--}o Title : "has_alternative_title"
Manifestation ||--|| Title : "has_primary_title"
WorkVariant ||--}o Genre : "has_genre"
WorkVariant ||--}o CategorizedThing : "has_subject"
WorkVariant ||--}o MovingImageResource : "is_part_of"
WorkVariant ||--|o MovingImageResource : "is_variant_of"
WorkVariant ||--}o AuthorityResource : "same_as"
WorkVariant ||--|o DescriptionResource : "described_by"
WorkVariant ||--}o Event : "has_event"
WorkVariant ||--}o MovingImageResource : "has_identifier"
WorkVariant ||--}o Language : "in_language"
WorkVariant ||--}o Title : "has_alternative_title"
WorkVariant ||--|| Title : "has_primary_title"
Genre ||--}o GNDResource : "same_as"

```

