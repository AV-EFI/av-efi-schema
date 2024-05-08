

# Class: Subject


_Subject descriptor terms for the content of a film specifying its period, themes, locations, etc. Not to be confused with Genre. Provide name and if at all possible identifier(s) from supported authorities in the same_as slot. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.3_





URI: [avefi:Subject](https://av-efi.net/schema/av-efi-schema/Subject)




```mermaid
 classDiagram
    class Subject
      Entity <|-- Subject
      
      Subject : category
        
      Subject : has_alternate_name
        
      Subject : has_name
        
      Subject : same_as
        
          Subject --> AuthorityResource : same_as
        
      
```





## Inheritance
* [Entity](Entity.md)
    * **Subject**



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
| [WorkVariant](WorkVariant.md) | [has_subject](has_subject.md) | range | [Subject](Subject.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:Subject |
| native | avefi:Subject |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Subject
description: 'Subject descriptor terms for the content of a film specifying its period,
  themes, locations, etc. Not to be confused with Genre. Provide name and if at all
  possible identifier(s) from supported authorities in the same_as slot. See also:
  FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms
  D.2.3'
from_schema: https://av-efi.net/schema/av-efi-schema
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
name: Subject
description: 'Subject descriptor terms for the content of a film specifying its period,
  themes, locations, etc. Not to be confused with Genre. Provide name and if at all
  possible identifier(s) from supported authorities in the same_as slot. See also:
  FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms
  D.2.3'
from_schema: https://av-efi.net/schema/av-efi-schema
is_a: Entity
attributes:
  has_alternate_name:
    name: has_alternate_name
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:alternateName
    multivalued: true
    alias: has_alternate_name
    owner: Subject
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
    owner: Subject
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
    owner: Subject
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
    owner: Subject
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>