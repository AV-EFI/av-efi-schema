

# Class: DigitalFile


_FIAF Moving Image Cataloguing Manual D.7.2_





URI: [avefi:DigitalFile](https://av-efi.net/schema/av-efi-schema/DigitalFile)




```mermaid
 classDiagram
    class DigitalFile
      Format <|-- DigitalFile
      
      DigitalFile : category
        
      DigitalFile : type
        
          DigitalFile --> FormatDigitalFileTypeEnum : type
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [Format](Format.md)
        * **DigitalFile**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [type](type.md) | 0..1 <br/> [FormatDigitalFileTypeEnum](FormatDigitalFileTypeEnum.md) |  | [Format](Format.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:DigitalFile |
| native | avefi:DigitalFile |
| close | fiaf:DigitalFile |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: DigitalFile
description: FIAF Moving Image Cataloguing Manual D.7.2
from_schema: https://av-efi.net/schema/av-efi-schema
close_mappings:
- fiaf:DigitalFile
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
    range: FormatDigitalFileTypeEnum

```
</details>

### Induced

<details>
```yaml
name: DigitalFile
description: FIAF Moving Image Cataloguing Manual D.7.2
from_schema: https://av-efi.net/schema/av-efi-schema
close_mappings:
- fiaf:DigitalFile
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
    range: FormatDigitalFileTypeEnum
attributes:
  type:
    name: type
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: type
    owner: DigitalFile
    domain_of:
    - WorkVariant
    - Activity
    - Agent
    - Event
    - Title
    - Format
    - Manifestation
    range: FormatDigitalFileTypeEnum
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: DigitalFile
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>