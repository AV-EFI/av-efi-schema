

# Slot: has_name


_A human-readable name for a thing_



URI: [schema:name](http://schema.org/name)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Subject](Subject.md) | Subject descriptor terms for the content of a film specifying its period, the... |  no  |
| [Agent](Agent.md) | Agent involved in some activity related to the moving image resource |  yes  |
| [Title](Title.md) | FIAF Moving Image Cataloguing Manual 1 |  yes  |
| [GeographicName](GeographicName.md) | Name of country, region or other location |  no  |
| [Genre](Genre.md) | Genre describes categories of Works, characterized by similar plots, themes, ... |  no  |







## Properties

* Range: [String](String.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_name
description: A human-readable name for a thing
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: schema:name
alias: has_name
domain_of:
- GeographicName
- Genre
- Subject
- Agent
- Title
range: string
required: true

```
</details>