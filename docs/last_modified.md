

# Slot: last_modified


_Timestamp (in UTC) for the latest modification to any field in the PID metadata record_



URI: [dcterms:modified](http://purl.org/dc/terms/modified)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DescriptionResource](DescriptionResource.md) | Metadata about the PID rather than the identified object, i |  no  |







## Properties

* Range: [Datetime](Datetime.md)

* Required: True

* Regex pattern: `^2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?Z$`





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: last_modified
description: Timestamp (in UTC) for the latest modification to any field in the PID
  metadata record
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: dcterms:modified
alias: last_modified
domain_of:
- DescriptionResource
range: datetime
required: true
pattern: ^2[0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T([0-1][0-9]|2[0-3]):[0-5][0-9]:([0-5][0-9]|60)(\.[0-9]+)?Z$

```
</details>