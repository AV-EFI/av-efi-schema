

# Slot: has_issuer_name


_Name of the responsible party_



URI: [dcterms:contributor](http://purl.org/dc/terms/contributor)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DescriptionResource](DescriptionResource.md) | Metadata about the PID rather than the identified object, i |  no  |







## Properties

* Range: [String](String.md)

* Required: True






## Examples

| Value |
| --- |
| Filmmuseum Düsseldorf |

## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_issuer_name
description: Name of the responsible party
examples:
- value: Filmmuseum Düsseldorf
  description: Human readable name of the issuer
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: dcterms:contributor
alias: has_issuer_name
domain_of:
- DescriptionResource
range: string
required: true

```
</details>