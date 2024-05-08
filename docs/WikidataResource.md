

# Class: WikidataResource


_Identifier for Wikidata entities_





URI: [avefi:WikidataResource](https://av-efi.net/schema/av-efi-schema/WikidataResource)




```mermaid
 classDiagram
    class WikidataResource
      AuthorityResource <|-- WikidataResource
      
      WikidataResource : category
        
      WikidataResource : id
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [AuthorityResource](AuthorityResource.md)
        * **WikidataResource**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [String](String.md) | A unique identifier for a thing | [AuthorityResource](AuthorityResource.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## See Also

* [https://www.wikidata.org/wiki/Wikidata:Identifiers](https://www.wikidata.org/wiki/Wikidata:Identifiers)

## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| formatter_uri_for_rdf_resource | https://www.wikidata.org/entity/$1 || formatter_url_for_web_resource | https://www.wikidata.org/entity/$1 || provides | ['CreativeWorkIdentifier', 'PlaceIdentifier', 'OrganizationIdentifier', 'PersonIdentifier', 'SubjectHeadingIdentifier'] |



### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:WikidataResource |
| native | avefi:WikidataResource |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: WikidataResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: https://www.wikidata.org/entity/$1
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://www.wikidata.org/entity/$1
  provides:
    tag: provides
    value:
    - CreativeWorkIdentifier
    - PlaceIdentifier
    - OrganizationIdentifier
    - PersonIdentifier
    - SubjectHeadingIdentifier
description: Identifier for Wikidata entities
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.wikidata.org/wiki/Wikidata:Identifiers
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[LPQ]\\d+$

```
</details>

### Induced

<details>
```yaml
name: WikidataResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: https://www.wikidata.org/entity/$1
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://www.wikidata.org/entity/$1
  provides:
    tag: provides
    value:
    - CreativeWorkIdentifier
    - PlaceIdentifier
    - OrganizationIdentifier
    - PersonIdentifier
    - SubjectHeadingIdentifier
description: Identifier for Wikidata entities
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.wikidata.org/wiki/Wikidata:Identifiers
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[LPQ]\\d+$
attributes:
  id:
    name: id
    description: A unique identifier for a thing
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: WikidataResource
    domain_of:
    - PIDRecord
    - AuthorityResource
    range: string
    required: true
    pattern: ^[LPQ]\\d+$
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: WikidataResource
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>