```mermaid
erDiagram
Item {
    ItemElementTypeEnum element_type  
    ItemAccessStatusEnum has_access_status  
    stringList has_note  
    uri has_webresource  
    uriorcurie id  
    uriorcurie category  
}
Title {
    string has_name  
    string has_ordering_name  
    TitleTypeEnum type  
    uriorcurie category  
}
Language {
    string code  
    LanguageUsageEnumList usage  
    uriorcurie category  
}
Event {
    string has_date  
    EventTypeEnum type  
    uriorcurie category  
}
GeographicName {
    stringList has_alternate_name  
    string has_name  
    uriorcurie category  
}
AuthorityResource {
    string id  
    uriorcurie category  
}
Activity {
    ActivityTypeEnum type  
    uriorcurie category  
}
Agent {
    stringList has_alternate_name  
    string has_name  
    AgentTypeEnum type  
    uriorcurie category  
}
DescriptionResource {
    uri has_history  
    uri has_issuer_id  
    string has_issuer_name  
    datetime last_modified  
}
Format {
    uriorcurie type  
    uriorcurie category  
}
Extent {
    UnitEnum has_unit  
    decimal has_value  
    PrecisionEnum value_is  
    uriorcurie category  
}
Duration {
    string has_value  
    PrecisionEnum value_is  
    uriorcurie category  
}
AVefiResource {
    string id  
    uriorcurie category  
}
Manifestation {
    ManifestationTypeEnum type  
    stringList has_note  
    uri has_webresource  
    uriorcurie id  
    uriorcurie category  
}
WorkVariant {
    WorkFormEnumList has_form  
    WorkVariantTypeEnum type  
    VariantTypeEnum variant_type  
    uriorcurie id  
    uriorcurie category  
}
Subject {
    stringList has_alternate_name  
    string has_name  
    uriorcurie category  
}
Genre {
    stringList has_alternate_name  
    string has_name  
    uriorcurie category  
}
GNDResource {
    string id  
    uriorcurie category  
}

Item ||--}o AVefiResource : "is_copy_of"
Item ||--}o AVefiResource : "is_derivative_of"
Item ||--|| AVefiResource : "is_item_of"
Item ||--|o Duration : "has_duration"
Item ||--|o Extent : "has_extent"
Item ||--}o Format : "has_format"
Item ||--|| DescriptionResource : "described_by"
Item ||--}o Event : "has_event"
Item ||--}o Language : "in_language"
Item ||--}o Title : "has_alternative_title"
Item ||--|| Title : "has_primary_title"
Event ||--}o Activity : "has_activity"
Event ||--}o GeographicName : "located_in"
GeographicName ||--}o AuthorityResource : "same_as"
Activity ||--}| Agent : "has_agent"
Agent ||--}o AuthorityResource : "same_as"
Manifestation ||--}o AVefiResource : "has_item"
Manifestation ||--}| AVefiResource : "is_manifestation_of"
Manifestation ||--}o AVefiResource : "same_as"
Manifestation ||--|o Duration : "has_duration"
Manifestation ||--|o Extent : "has_extent"
Manifestation ||--}o Format : "has_format"
Manifestation ||--|| DescriptionResource : "described_by"
Manifestation ||--}o Event : "has_event"
Manifestation ||--}o Language : "in_language"
Manifestation ||--}o Title : "has_alternative_title"
Manifestation ||--|| Title : "has_primary_title"
WorkVariant ||--}o Genre : "has_genre"
WorkVariant ||--}o Subject : "has_subject"
WorkVariant ||--}o AVefiResource : "is_part_of"
WorkVariant ||--|o AVefiResource : "is_variant_of"
WorkVariant ||--}o AuthorityResource : "same_as"
WorkVariant ||--|| DescriptionResource : "described_by"
WorkVariant ||--}o Event : "has_event"
WorkVariant ||--}o Language : "in_language"
WorkVariant ||--}o Title : "has_alternative_title"
WorkVariant ||--|| Title : "has_primary_title"
Subject ||--}o AuthorityResource : "same_as"
Genre ||--}o GNDResource : "same_as"

```

