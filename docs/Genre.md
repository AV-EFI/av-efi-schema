

# Class: Genre


_Genre describes categories of Works, characterized by similar plots, themes, settings, situations, and characters. Examples of genres are “westerns” and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.1_





URI: [avefi:Genre](https://av-efi.net/schema/av-efi-schema/Genre)




```mermaid
 classDiagram
    class Genre
      Entity <|-- Genre
      
      Genre : category
        
      Genre : has_alternate_name
        
      Genre : has_name
        
      Genre : same_as
        
          Genre --> GNDResource : same_as
        
      
```





## Inheritance
* [Entity](Entity.md)
    * **Genre**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [has_alternate_name](has_alternate_name.md) | 0..* <br/> [String](String.md) |  | direct |
| [has_name](has_name.md) | 1..1 <br/> [String](String.md) | A human-readable name for a thing | direct |
| [same_as](same_as.md) | 0..* <br/> [GNDResource](GNDResource.md) |  | direct |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |





## Usages

| used by | used in | type | used |
| ---  | --- | --- | --- |
| [WorkVariant](WorkVariant.md) | [has_genre](has_genre.md) | range | [Genre](Genre.md) |






## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:Genre |
| native | avefi:Genre |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Genre
description: 'Genre describes categories of Works, characterized by similar plots,
  themes, settings, situations, and characters. Examples of genres are “westerns”
  and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary
  of Filmographic Terms D.2.1'
from_schema: https://av-efi.net/schema/av-efi-schema
is_a: Entity
slots:
- has_alternate_name
- has_name
- same_as
slot_usage:
  same_as:
    name: same_as
    domain_of:
    - WorkVariant
    - GeographicName
    - Genre
    - Subject
    - Agent
    - Manifestation
    range: GNDResource

```
</details>

### Induced

<details>
```yaml
name: Genre
description: 'Genre describes categories of Works, characterized by similar plots,
  themes, settings, situations, and characters. Examples of genres are “westerns”
  and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary
  of Filmographic Terms D.2.1'
from_schema: https://av-efi.net/schema/av-efi-schema
is_a: Entity
slot_usage:
  same_as:
    name: same_as
    domain_of:
    - WorkVariant
    - GeographicName
    - Genre
    - Subject
    - Agent
    - Manifestation
    range: GNDResource
attributes:
  has_alternate_name:
    name: has_alternate_name
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:alternateName
    multivalued: true
    alias: has_alternate_name
    owner: Genre
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
    owner: Genre
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
    owner: Genre
    domain_of:
    - WorkVariant
    - GeographicName
    - Genre
    - Subject
    - Agent
    - Manifestation
    range: GNDResource
    inlined: true
    inlined_as_list: true
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: Genre
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>