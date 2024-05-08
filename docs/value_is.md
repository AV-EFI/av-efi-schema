

# Slot: value_is


_Qualifier indicating the precision of an extent value or duration_



URI: [avefi:value_is](https://av-efi.net/schema/av-efi-schema/value_is)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Extent](Extent.md) | Physical length or size of the described object |  no  |
| [Duration](Duration.md) | Total running time of the described object in ISO 8601 duration format |  no  |







## Properties

* Range: [PrecisionEnum](PrecisionEnum.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: value_is
description: Qualifier indicating the precision of an extent value or duration
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
alias: value_is
domain_of:
- Duration
- Extent
range: PrecisionEnum

```
</details>