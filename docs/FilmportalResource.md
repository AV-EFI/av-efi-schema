

# Class: FilmportalResource


_Identifier of the German Filmportal.de_





URI: [avefi:FilmportalResource](https://av-efi.net/schema/av-efi-schema/FilmportalResource)




```mermaid
 classDiagram
    class FilmportalResource
      AuthorityResource <|-- FilmportalResource
      
      FilmportalResource : category
        
      FilmportalResource : id
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [AuthorityResource](AuthorityResource.md)
        * **FilmportalResource**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [String](String.md) | A unique identifier for a thing | [AuthorityResource](AuthorityResource.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## See Also

* [https://www.filmportal.de/](https://www.filmportal.de/)
* [https://www.wikidata.org/entity/P2639](https://www.wikidata.org/entity/P2639)

## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| formatter_uri_for_rdf_resource | https://www.filmportal.de/$1 || formatter_uri_for_web_resource | https://www.filmportal.de/$1 || provides | ['CreativeWorkIdentifier', 'PersonIdentifier'] |



### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:FilmportalResource |
| native | avefi:FilmportalResource |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: FilmportalResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: https://www.filmportal.de/$1
  formatter_uri_for_web_resource:
    tag: formatter_uri_for_web_resource
    value: https://www.filmportal.de/$1
  provides:
    tag: provides
    value:
    - CreativeWorkIdentifier
    - PersonIdentifier
description: Identifier of the German Filmportal.de
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.filmportal.de/
- https://www.wikidata.org/entity/P2639
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[\\da-f]{32}$

```
</details>

### Induced

<details>
```yaml
name: FilmportalResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: https://www.filmportal.de/$1
  formatter_uri_for_web_resource:
    tag: formatter_uri_for_web_resource
    value: https://www.filmportal.de/$1
  provides:
    tag: provides
    value:
    - CreativeWorkIdentifier
    - PersonIdentifier
description: Identifier of the German Filmportal.de
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.filmportal.de/
- https://www.wikidata.org/entity/P2639
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[\\da-f]{32}$
attributes:
  id:
    name: id
    description: A unique identifier for a thing
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: FilmportalResource
    domain_of:
    - PIDRecord
    - AuthorityResource
    range: string
    required: true
    pattern: ^[\\da-f]{32}$
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: FilmportalResource
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>