

# Class: Optical


_FIAF Moving Image Cataloguing Manual D.7.2_





URI: [avefi:Optical](https://av-efi.net/schema/av-efi-schema/Optical)




```mermaid
 classDiagram
    class Optical
      Format <|-- Optical
      
      Optical : category
        
      Optical : type
        
          Optical --> FormatOpticalTypeEnum : type
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [Format](Format.md)
        * **Optical**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [type](type.md) | 0..1 <br/> [FormatOpticalTypeEnum](FormatOpticalTypeEnum.md) |  | [Format](Format.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:Optical |
| native | avefi:Optical |
| close | fiaf:Optical |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Optical
description: FIAF Moving Image Cataloguing Manual D.7.2
from_schema: https://av-efi.net/schema/av-efi-schema
close_mappings:
- fiaf:Optical
is_a: Format
slot_usage:
  type:
    name: type
    domain_of:
    - WorkVariant
    - Activity
    - Agent
    - Event
    - Title
    - Format
    - Manifestation
    range: FormatOpticalTypeEnum

```
</details>

### Induced

<details>
```yaml
name: Optical
description: FIAF Moving Image Cataloguing Manual D.7.2
from_schema: https://av-efi.net/schema/av-efi-schema
close_mappings:
- fiaf:Optical
is_a: Format
slot_usage:
  type:
    name: type
    domain_of:
    - WorkVariant
    - Activity
    - Agent
    - Event
    - Title
    - Format
    - Manifestation
    range: FormatOpticalTypeEnum
attributes:
  type:
    name: type
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: type
    owner: Optical
    domain_of:
    - WorkVariant
    - Activity
    - Agent
    - Event
    - Title
    - Format
    - Manifestation
    range: FormatOpticalTypeEnum
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: Optical
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>