# Enum: WorkVariantTypeEnum




_Work/Variant description type. See also: FIAF Moving Image Cataloguing Manual 1.2.1, D.1_



URI: [WorkVariantTypeEnum](WorkVariantTypeEnum.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Analytic | fiaf:Analytic | Content that is contained in another content |
| Collection | fiaf:Collection | Content issued in several independent parts; an ‘umbrella’ work title coverin... |
| Monographic | fiaf:Monographic | Complete content in one part or intended to be completed in a finite number o... |
| Serial | fiaf:Serial | Content issued in successive parts and intended to be continued indefinitely,... |




## Slots

| Name | Description |
| ---  | --- |
| [type](type.md) |  |






## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: WorkVariantTypeEnum
description: 'Work/Variant description type. See also: FIAF Moving Image Cataloguing
  Manual 1.2.1, D.1'
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
permissible_values:
  Analytic:
    text: Analytic
    description: Content that is contained in another content
    meaning: fiaf:Analytic
  Collection:
    text: Collection
    description: Content issued in several independent parts; an ‘umbrella’ work title
      covering a number of different Works/Variants/Manifestations
    meaning: fiaf:Collection
  Monographic:
    text: Monographic
    description: Complete content in one part or intended to be completed in a finite
      number of parts
    meaning: fiaf:Monographic
  Serial:
    text: Serial
    description: Content issued in successive parts and intended to be continued indefinitely,
      or across a span of time. A Work record for a television series is catalogued
      as a “Serial”, individual episodes may be catalogued as a Monographic record
    meaning: fiaf:Serial

```
</details>
