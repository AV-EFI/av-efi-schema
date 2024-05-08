

# Class: VIAFResource


_Virtual International Authority File identifier hosted by OCLC. The data is accumulated from various well established authority files from different parts of teh world_





URI: [avefi:VIAFResource](https://av-efi.net/schema/av-efi-schema/VIAFResource)




```mermaid
 classDiagram
    class VIAFResource
      AuthorityResource <|-- VIAFResource
      
      VIAFResource : category
        
      VIAFResource : id
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [AuthorityResource](AuthorityResource.md)
        * **VIAFResource**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [String](String.md) | A unique identifier for a thing | [AuthorityResource](AuthorityResource.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## See Also

* [https://viaf.org/](https://viaf.org/)
* [https://www.wikidata.org/entity/P214](https://www.wikidata.org/entity/P214)

## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| formatter_uri_for_rdf_resource | http://viaf.org/viaf/$1 || formatter_url_for_web_resource | https://viaf.org/viaf/$1 || provides | ['CreativeWorkIdentifier', 'PlaceIdentifier', 'OrganizationIdentifier', 'PersonIdentifier'] |



### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:VIAFResource |
| native | avefi:VIAFResource |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: VIAFResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: http://viaf.org/viaf/$1
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://viaf.org/viaf/$1
  provides:
    tag: provides
    value:
    - CreativeWorkIdentifier
    - PlaceIdentifier
    - OrganizationIdentifier
    - PersonIdentifier
description: Virtual International Authority File identifier hosted by OCLC. The data
  is accumulated from various well established authority files from different parts
  of teh world
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://viaf.org/
- https://www.wikidata.org/entity/P214
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^\\d+$

```
</details>

### Induced

<details>
```yaml
name: VIAFResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: http://viaf.org/viaf/$1
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://viaf.org/viaf/$1
  provides:
    tag: provides
    value:
    - CreativeWorkIdentifier
    - PlaceIdentifier
    - OrganizationIdentifier
    - PersonIdentifier
description: Virtual International Authority File identifier hosted by OCLC. The data
  is accumulated from various well established authority files from different parts
  of teh world
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://viaf.org/
- https://www.wikidata.org/entity/P214
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^\\d+$
attributes:
  id:
    name: id
    description: A unique identifier for a thing
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: VIAFResource
    domain_of:
    - PIDRecord
    - AuthorityResource
    range: string
    required: true
    pattern: ^\\d+$
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: VIAFResource
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>