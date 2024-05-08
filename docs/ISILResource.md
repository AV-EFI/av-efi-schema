

# Class: ISILResource


_International Standard Identifier for Libraries and Related Organizations including (film) archives_





URI: [avefi:ISILResource](https://av-efi.net/schema/av-efi-schema/ISILResource)




```mermaid
 classDiagram
    class ISILResource
      AuthorityResource <|-- ISILResource
      
      ISILResource : category
        
      ISILResource : id
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [AuthorityResource](AuthorityResource.md)
        * **ISILResource**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [String](String.md) | A unique identifier for a thing | [AuthorityResource](AuthorityResource.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## See Also

* [https://biblstandard.dk/isil/index.htm](https://biblstandard.dk/isil/index.htm)
* [https://www.wikidata.org/wiki/Property:P791](https://www.wikidata.org/wiki/Property:P791)

## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| formatter_url_for_web_resource | https://w3id.org/isil/$1 || provides | ['OrganizationIdentifier'] |



### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:ISILResource |
| native | avefi:ISILResource |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: ISILResource
annotations:
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://w3id.org/isil/$1
  provides:
    tag: provides
    value:
    - OrganizationIdentifier
description: International Standard Identifier for Libraries and Related Organizations
  including (film) archives
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://biblstandard.dk/isil/index.htm
- https://www.wikidata.org/wiki/Property:P791
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[A-Z]{2}-[A-Za-z\-0-9:/]{1,15}$

```
</details>

### Induced

<details>
```yaml
name: ISILResource
annotations:
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://w3id.org/isil/$1
  provides:
    tag: provides
    value:
    - OrganizationIdentifier
description: International Standard Identifier for Libraries and Related Organizations
  including (film) archives
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://biblstandard.dk/isil/index.htm
- https://www.wikidata.org/wiki/Property:P791
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[A-Z]{2}-[A-Za-z\-0-9:/]{1,15}$
attributes:
  id:
    name: id
    description: A unique identifier for a thing
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: ISILResource
    domain_of:
    - PIDRecord
    - AuthorityResource
    range: string
    required: true
    pattern: ^[A-Z]{2}-[A-Za-z\-0-9:/]{1,15}$
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: ISILResource
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>