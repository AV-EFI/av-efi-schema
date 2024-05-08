

# Class: Item


_FIAF Moving Image Cataloguing Manual 3.0_





URI: [avefi:Item](https://av-efi.net/schema/av-efi-schema/Item)




```mermaid
 classDiagram
    class Item
      ManifestationOrItem <|-- Item
      
      Item : category
        
      Item : described_by
        
          Item --> DescriptionResource : described_by
        
      Item : element_type
        
          Item --> ItemElementTypeEnum : element_type
        
      Item : has_access_status
        
          Item --> ItemAccessStatusEnum : has_access_status
        
      Item : has_alternative_title
        
          Item --> Title : has_alternative_title
        
      Item : has_duration
        
          Item --> Duration : has_duration
        
      Item : has_event
        
          Item --> Event : has_event
        
      Item : has_extent
        
          Item --> Extent : has_extent
        
      Item : has_format
        
          Item --> Format : has_format
        
      Item : has_note
        
      Item : has_primary_title
        
          Item --> Title : has_primary_title
        
      Item : has_webresource
        
      Item : id
        
      Item : in_language
        
          Item --> Language : in_language
        
      Item : is_copy_of
        
          Item --> AVefiResource : is_copy_of
        
      Item : is_derivative_of
        
          Item --> AVefiResource : is_derivative_of
        
      Item : is_item_of
        
          Item --> AVefiResource : is_item_of
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [PIDRecord](PIDRecord.md)
        * [MovingImageRecord](MovingImageRecord.md)
            * [ManifestationOrItem](ManifestationOrItem.md)
                * **Item**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [element_type](element_type.md) | 0..1 <br/> [ItemElementTypeEnum](ItemElementTypeEnum.md) |  | direct |
| [has_access_status](has_access_status.md) | 0..1 <br/> [ItemAccessStatusEnum](ItemAccessStatusEnum.md) |  | direct |
| [is_copy_of](is_copy_of.md) | 0..* <br/> [AVefiResource](AVefiResource.md) | Link to AVefi item registered by another institution indicating that the two ... | direct |
| [is_derivative_of](is_derivative_of.md) | 0..* <br/> [AVefiResource](AVefiResource.md) | Link to AVefi item from which this one has been derived in whole or in part, ... | direct |
| [is_item_of](is_item_of.md) | 1..1 <br/> [AVefiResource](AVefiResource.md) | Indicate AVefi Manifestation the item belongs to | direct |
| [has_duration](has_duration.md) | 0..1 <br/> [Duration](Duration.md) | Total running time of the described object in ISO 8601 duration format | [ManifestationOrItem](ManifestationOrItem.md) |
| [has_extent](has_extent.md) | 0..1 <br/> [Extent](Extent.md) | Physical length or size of the described object | [ManifestationOrItem](ManifestationOrItem.md) |
| [has_format](has_format.md) | 0..* <br/> [Format](Format.md) |  | [ManifestationOrItem](ManifestationOrItem.md) |
| [has_note](has_note.md) | 0..* <br/> [String](String.md) | FIAF Moving Image Cataloguing Manual Appendix B | [ManifestationOrItem](ManifestationOrItem.md) |
| [has_webresource](has_webresource.md) | 0..1 <br/> [Uri](Uri.md) | Link to data provider's own presentation of manifestation or item on the web | [ManifestationOrItem](ManifestationOrItem.md) |
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
| self | avefi:Item |
| native | avefi:Item |
| broad | fiaf:Item |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: Item
description: FIAF Moving Image Cataloguing Manual 3.0
from_schema: https://av-efi.net/schema/av-efi-schema
broad_mappings:
- fiaf:Item
is_a: ManifestationOrItem
slots:
- element_type
- has_access_status
- is_copy_of
- is_derivative_of
- is_item_of

```
</details>

### Induced

<details>
```yaml
name: Item
description: FIAF Moving Image Cataloguing Manual 3.0
from_schema: https://av-efi.net/schema/av-efi-schema
broad_mappings:
- fiaf:Item
is_a: ManifestationOrItem
attributes:
  element_type:
    name: element_type
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: element_type
    owner: Item
    domain_of:
    - Item
    range: ItemElementTypeEnum
  has_access_status:
    name: has_access_status
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: has_access_status
    owner: Item
    domain_of:
    - Item
    range: ItemAccessStatusEnum
  is_copy_of:
    name: is_copy_of
    description: Link to AVefi item registered by another institution indicating that
      the two are known to be copies of each other
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: is_copy_of
    owner: Item
    domain_of:
    - Item
    range: AVefiResource
    inlined: true
    inlined_as_list: true
  is_derivative_of:
    name: is_derivative_of
    description: Link to AVefi item from which this one has been derived in whole
      or in part, e.g. as a result of a restoration or digitasation project
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: is_derivative_of
    owner: Item
    domain_of:
    - Item
    range: AVefiResource
    inlined: true
    inlined_as_list: true
  is_item_of:
    name: is_item_of
    description: Indicate AVefi Manifestation the item belongs to. Every item must
      be associated with a manifestation from the same data provider
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: is_item_of
    owner: Item
    domain_of:
    - Item
    range: AVefiResource
    required: true
  has_duration:
    name: has_duration
    description: 'Total running time of the described object in ISO 8601 duration
      format. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11'
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    alias: has_duration
    owner: Item
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
    owner: Item
    domain_of:
    - ManifestationOrItem
    range: Extent
  has_format:
    name: has_format
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    multivalued: true
    alias: has_format
    owner: Item
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
    owner: Item
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
    owner: Item
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
    owner: Item
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
    owner: Item
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
    owner: Item
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
    owner: Item
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
    owner: Item
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
    owner: Item
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
    owner: Item
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>