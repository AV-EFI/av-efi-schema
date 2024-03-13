```mermaid
erDiagram
MovingImageRecordCollection {
    uriorcurie category  
}
MovingImageRecord {
    uriorcurie category  
}
Title {
    TitleTypeEnum type  
    string value  
    uriorcurie category  
}
Event {
    string date  
    EventTypeEnum type  
    uriorcurie category  
}
Activity {
    ActivityTypeEnum type  
    uriorcurie category  
}
Agent {
    string name  
    uriorcurie category  
}
Identifier {
    uriorcurie category  
}

MovingImageRecordCollection ||--}o MovingImageRecord : "has_record"
MovingImageRecord ||--}o Event : "has_event"
MovingImageRecord ||--}o Title : "has_title"
Event ||--}o Activity : "has_activity"
Activity ||--}o Agent : "has_agent"
Agent ||--}o Identifier : "has_identifier"

```

