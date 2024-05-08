

# Class: GeographicName


_Name of country, region or other location. Names should be taken from appropriate authorities (e.g. GND) and recorded as a human readable string in the name attribute and as linked data in the same_as attribute. See also: FIAF Moving Image Cataloguing Manual 1.3.3, D.4_





URI: [avefi:GeographicName](https://av-efi.net/schema/av-efi-schema/GeographicName)




```mermaid
 classDiagram
    class GeographicName
      Entity <|-- GeographicName
      
      GeographicName : category
        
      GeographicName : has_alternate_name
        
      GeographicName : has_name
        
      GeographicName : same_as
        
          GeographicName --> AuthorityResource : same_as
        
      
```





## Inheritance
* [Entity](Entity.md)
    * **GeographicName**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [has_alternate_name](has_alternate_name.md) | 0..* <br/> [String](String.md) |  | direct |
| [has_name](has_name.md) | 1..1 <br/> [String](String.md) | A human-readable name for a thing | direct |
| [same_as](same_as.md) | 0..* <br/> [AuthorityResource](AuthorityResource.md) |  | direct |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [Event](Event.md) | [located_in](located_in.md) | range | [GeographicName](GeographicName.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:GeographicName |
| native | avefi:GeographicName |
| related | fiaf:Country, fiaf:Location |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: GeographicName
description: 'Name of country, region or other location. Names should be taken from
  appropriate authorities (e.g. GND) and recorded as a human readable string in the
  name attribute and as linked data in the same_as attribute. See also: FIAF Moving
  Image Cataloguing Manual 1.3.3, D.4'
from_schema: https://av-efi.net/schema/av-efi-schema
related_mappings:
- fiaf:Country
- fiaf:Location
is_a: Entity
slots:
- has_alternate_name
- has_name
- same_as

```
</details>

### Induced

<details>
```yaml
name: GeographicName
description: 'Name of country, region or other location. Names should be taken from
  appropriate authorities (e.g. GND) and recorded as a human readable string in the
  name attribute and as linked data in the same_as attribute. See also: FIAF Moving
  Image Cataloguing Manual 1.3.3, D.4'
from_schema: https://av-efi.net/schema/av-efi-schema
related_mappings:
- fiaf:Country
- fiaf:Location
is_a: Entity
attributes:
  has_alternate_name:
    name: has_alternate_name
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:alternateName
    multivalued: true
    alias: has_alternate_name
    owner: GeographicName
    domain_of:
    - GeographicName
    - Genre
    - Subject
    - Agent
    range: string
  has_name:
    name: has_name
    description: A human-readable name for a thing
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:name
    alias: has_name
    owner: GeographicName
    domain_of:
    - GeographicName
    - Genre
    - Subject
    - Agent
    - Title
    range: string
    required: true
  same_as:
    name: same_as
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: same_as
    owner: GeographicName
    domain_of:
    - WorkVariant
    - GeographicName
    - Genre
    - Subject
    - Agent
    - Manifestation
    range: AuthorityResource
    inlined: true
    inlined_as_list: true
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: GeographicName
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>