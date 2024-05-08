

# Class: ManifestationOrItem


* __NOTE__: this is an abstract class and should not be instantiated directly


URI: [avefi:ManifestationOrItem](https://av-efi.net/schema/av-efi-schema/ManifestationOrItem)




```mermaid
 classDiagram
    class ManifestationOrItem
      MovingImageRecord <|-- ManifestationOrItem
      

      ManifestationOrItem <|-- Manifestation
      ManifestationOrItem <|-- Item
      
      
      ManifestationOrItem : category
        
      ManifestationOrItem : described_by
        
          ManifestationOrItem --> DescriptionResource : described_by
        
      ManifestationOrItem : has_alternative_title
        
          ManifestationOrItem --> Title : has_alternative_title
        
      ManifestationOrItem : has_duration
        
          ManifestationOrItem --> Duration : has_duration
        
      ManifestationOrItem : has_event
        
          ManifestationOrItem --> Event : has_event
        
      ManifestationOrItem : has_extent
        
          ManifestationOrItem --> Extent : has_extent
        
      ManifestationOrItem : has_format
        
          ManifestationOrItem --> Format : has_format
        
      ManifestationOrItem : has_note
        
      ManifestationOrItem : has_primary_title
        
          ManifestationOrItem --> Title : has_primary_title
        
      ManifestationOrItem : has_webresource
        
      ManifestationOrItem : id
        
      ManifestationOrItem : in_language
        
          ManifestationOrItem --> Language : in_language
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [PIDRecord](PIDRecord.md)
        * [MovingImageRecord](MovingImageRecord.md)
            * **ManifestationOrItem**
                * [Manifestation](Manifestation.md)
                * [Item](Item.md)



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [has_duration](has_duration.md) | 0..1 <br/> [Duration](Duration.md) | Total running time of the described object in ISO 8601 duration format | direct |
| [has_extent](has_extent.md) | 0..1 <br/> [Extent](Extent.md) | Physical length or size of the described object | direct |
| [has_format](has_format.md) | 0..* <br/> [Format](Format.md) |  | direct |
| [has_note](has_note.md) | 0..* <br/> [String](String.md) | FIAF Moving Image Cataloguing Manual Appendix B | direct |
| [has_webresource](has_webresource.md) | 0..1 <br/> [Uri](Uri.md) | Link to data provider's own presentation of manifestation or item on the web | direct |
| [described_by](described_by.md) | 1..1 <br/> [DescriptionResource](DescriptionResource.md) | Also record some metadata about the PID itself rather than the identified obj... | [MovingImageRecord](MovingImageRecord.md) |
| [has_event](has_event.md) | 0..* <br/> [Event](Event.md) | Associate event(s) with a moving image record | [MovingImageRecord](MovingImageRecord.md) |
| [in_language](in_language.md) | 0..* <br/> [Language](Language.md) | FIAF Moving Image Cataloguing Manual 1 | [MovingImageRecord](MovingImageRecord.md) |
| [has_alternative_title](has_alternative_title.md) | 0..* <br/> [Title](Title.md) | Additional title(s) associated with the work / variant, manifestation, or ite... | [MovingImageRecord](MovingImageRecord.md) |
| [has_primary_title](has_primary_title.md) | 1..1 <br/> [Title](Title.md) | Primary title to be displayed in search results etc | [MovingImageRecord](MovingImageRecord.md) |
| [id](id.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) | A unique identifier for a thing | [PIDRecord](PIDRecord.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:ManifestationOrItem |
| native | avefi:ManifestationOrItem |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ManifestationOrItem
from_schema: https://av-efi.net/schema/av-efi-schema
is_a: MovingImageRecord
abstract: true
slots:
- has_duration
- has_extent
- has_format
- has_note
- has_webresource

```
</details>

### Induced

<details>
```yaml
name: ManifestationOrItem
from_schema: https://av-efi.net/schema/av-efi-schema
is_a: MovingImageRecord
abstract: true
attributes:
  has_duration:
    name: has_duration
    description: 'Total running time of the described object in ISO 8601 duration
      format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11'
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: has_duration
    owner: ManifestationOrItem
    domain_of:
    - ManifestationOrItem
    range: Duration
  has_extent:
    name: has_extent
    description: 'Physical length or size of the described object. See also: FIAF
      Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8'
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: has_extent
    owner: ManifestationOrItem
    domain_of:
    - ManifestationOrItem
    range: Extent
  has_format:
    name: has_format
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: has_format
    owner: ManifestationOrItem
    domain_of:
    - ManifestationOrItem
    range: Format
    inlined: true
    inlined_as_list: true
  has_note:
    name: has_note
    description: FIAF Moving Image Cataloguing Manual Appendix B
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: has_note
    owner: ManifestationOrItem
    domain_of:
    - ManifestationOrItem
    range: string
    inlined: true
    inlined_as_list: true
  has_webresource:
    name: has_webresource
    description: Link to data provider's own presentation of manifestation or item
      on the web
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: has_webresource
    owner: ManifestationOrItem
    domain_of:
    - ManifestationOrItem
    range: uri
  described_by:
    name: described_by
    description: Also record some metadata about the PID itself rather than the identified
      object
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: wdrs:describedby
    alias: described_by
    owner: ManifestationOrItem
    domain_of:
    - MovingImageRecord
    range: DescriptionResource
    required: true
    inlined: true
  has_event:
    name: has_event
    description: Associate event(s) with a moving image record
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: has_event
    owner: ManifestationOrItem
    domain_of:
    - MovingImageRecord
    range: Event
    inlined: true
    inlined_as_list: true
  in_language:
    name: in_language
    description: FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3
    from_schema: https://av-efi.net/schema/av-efi-schema
    related_mappings:
    - fiaf:hasLanguage
    - schema:inLanguage
    rank: 1000
    multivalued: true
    alias: in_language
    owner: ManifestationOrItem
    domain_of:
    - MovingImageRecord
    range: Language
    inlined: true
    inlined_as_list: true
  has_alternative_title:
    name: has_alternative_title
    description: Additional title(s) associated with the work / variant, manifestation,
      or item.
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: has_alternative_title
    owner: ManifestationOrItem
    domain_of:
    - MovingImageRecord
    range: Title
    inlined: true
    inlined_as_list: true
  has_primary_title:
    name: has_primary_title
    description: Primary title to be displayed in search results etc. The type should
      be PreferredTitle for works / variants and TitleProper for manifestations /
      items. If not available, type must be SuppliedDevisedTitle, instead.
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: has_primary_title
    owner: ManifestationOrItem
    domain_of:
    - MovingImageRecord
    range: Title
    required: true
  id:
    name: id
    description: A unique identifier for a thing
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: ManifestationOrItem
    domain_of:
    - PIDRecord
    - AuthorityResource
    range: uriorcurie
    required: true
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: ManifestationOrItem
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>