

# Slot: same_as

URI: [avefi:same_as](https://av-efi.net/schema/av-efi-schema/same_as)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subject](Subject.md) | Subject descriptor terms for the content of a film specifying its period, the... |  no  |
| [Manifestation](Manifestation.md) | FIAF Moving Image Cataloguing Manual 2 |  yes  |
| [WorkVariant](WorkVariant.md) | FIAF Moving Image Cataloguing Manual 1 |  no  |
| [Agent](Agent.md) | Agent involved in some activity related to the moving image resource |  no  |
| [GeographicName](GeographicName.md) | Name of country, region or other location |  no  |
| [Genre](Genre.md) | Genre describes categories of Works, characterized by similar plots, themes, ... |  yes  |







## Properties

* Range: [AuthorityResource](AuthorityResource.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: same_as
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
multivalued: true
alias: same_as
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

```
</details>