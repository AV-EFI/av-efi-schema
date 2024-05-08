

# Slot: has_alternate_name

URI: [schema:alternateName](http://schema.org/alternateName)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subject](Subject.md) | Subject descriptor terms for the content of a film specifying its period, the... |  no  |
| [Agent](Agent.md) | Agent involved in some activity related to the moving image resource |  no  |
| [GeographicName](GeographicName.md) | Name of country, region or other location |  no  |
| [Genre](Genre.md) | Genre describes categories of Works, characterized by similar plots, themes, ... |  no  |







## Properties

* Range: [String](String.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_alternate_name
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: schema:alternateName
multivalued: true
alias: has_alternate_name
domain_of:
- GeographicName
- Genre
- Subject
- Agent
range: string

```
</details>