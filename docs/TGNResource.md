

# Class: TGNResource


_Getty Thesaurus of Geographic Names ID_





URI: [avefi:TGNResource](https://av-efi.net/schema/av-efi-schema/TGNResource)




```mermaid
 classDiagram
    class TGNResource
      AuthorityResource <|-- TGNResource
      
      TGNResource : category
        
      TGNResource : id
        
      
```





## Inheritance
* [Entity](Entity.md)
    * [AuthorityResource](AuthorityResource.md)
        * **TGNResource**



## Slots

| Name | Cardinality and Range | Description | Inheritance |
| ---  | --- | --- | --- |
| [id](id.md) | 1..1 <br/> [String](String.md) | A unique identifier for a thing | [AuthorityResource](AuthorityResource.md) |
| [category](category.md) | 1..1 <br/> [Uriorcurie](Uriorcurie.md) |  | [Entity](Entity.md) |









## See Also

* [https://www.getty.edu/research/tools/vocabularies/tgn/index.html](https://www.getty.edu/research/tools/vocabularies/tgn/index.html)
* [https://vocab.getty.edu/resource?uri=http://vocab.getty.edu/dataset/tgn](https://vocab.getty.edu/resource?uri=http://vocab.getty.edu/dataset/tgn)
* [https://www.wikidata.org/wiki/Property:P1667](https://www.wikidata.org/wiki/Property:P1667)

## Identifier and Mapping Information





### Annotations

| property | value |
| --- | --- |
| formatter_uri_for_rdf_resource | http://vocab.getty.edu/tgn/$1 || formatter_url_for_web_resource | https://vocab.getty.edu/page/tgn/$1 || provides | ['PlaceIdentifier'] |



### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema





## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | avefi:TGNResource |
| native | avefi:TGNResource |





## LinkML Source

<!-- TODO: investigate https://stackoverflow.com/questions/37606292/how-to-create-tabbed-code-blocks-in-mkdocs-or-sphinx -->

### Direct

<details>
```yaml
name: TGNResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: http://vocab.getty.edu/tgn/$1
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://vocab.getty.edu/page/tgn/$1
  provides:
    tag: provides
    value:
    - PlaceIdentifier
description: Getty Thesaurus of Geographic Names ID
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.getty.edu/research/tools/vocabularies/tgn/index.html
- https://vocab.getty.edu/resource?uri=http://vocab.getty.edu/dataset/tgn
- https://www.wikidata.org/wiki/Property:P1667
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[1-9][0-9]{6}$

```
</details>

### Induced

<details>
```yaml
name: TGNResource
annotations:
  formatter_uri_for_rdf_resource:
    tag: formatter_uri_for_rdf_resource
    value: http://vocab.getty.edu/tgn/$1
  formatter_url_for_web_resource:
    tag: formatter_url_for_web_resource
    value: https://vocab.getty.edu/page/tgn/$1
  provides:
    tag: provides
    value:
    - PlaceIdentifier
description: Getty Thesaurus of Geographic Names ID
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.getty.edu/research/tools/vocabularies/tgn/index.html
- https://vocab.getty.edu/resource?uri=http://vocab.getty.edu/dataset/tgn
- https://www.wikidata.org/wiki/Property:P1667
is_a: AuthorityResource
slot_usage:
  id:
    name: id
    domain_of:
    - PIDRecord
    - AuthorityResource
    pattern: ^[1-9][0-9]{6}$
attributes:
  id:
    name: id
    description: A unique identifier for a thing
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: schema:identifier
    identifier: true
    alias: id
    owner: TGNResource
    domain_of:
    - PIDRecord
    - AuthorityResource
    range: string
    required: true
    pattern: ^[1-9][0-9]{6}$
  category:
    name: category
    from_schema: https://av-efi.net/schema/av-efi-schema
    rank: 1000
    slot_uri: rdf:type
    designates_type: true
    alias: category
    owner: TGNResource
    domain_of:
    - Entity
    range: uriorcurie
    required: true

```
</details>