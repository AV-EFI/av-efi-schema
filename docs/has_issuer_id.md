

# Slot: has_issuer_id


_Identifier for the responsible party as an URI suitable for linked data_



URI: [wdrs:issuedby](http://www.w3.org/2007/05/powder-s#issuedby)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [DescriptionResource](DescriptionResource.md) | Metadata about the PID rather than the identified object, i |  no  |







## Properties

* Range: [Uri](Uri.md)

* Required: True






## Examples

| Value |
| --- |
| https://ld.zdb-services.de/resource/organisations/DE-MUS-432511 |

## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_issuer_id
description: Identifier for the responsible party as an URI suitable for linked data
examples:
- value: https://ld.zdb-services.de/resource/organisations/DE-MUS-432511
  description: ISIL of the Filmmuseum Düsseldorf
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: wdrs:issuedby
alias: has_issuer_id
domain_of:
- DescriptionResource
range: uri
required: true

```
</details>