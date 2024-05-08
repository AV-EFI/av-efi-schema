# Enum: UnitEnum




_Units of measurement. Definitions are taken from the Quantities, Units, Dimensions and Data Types Ontologies (QUDT)_



URI: [UnitEnum](UnitEnum.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Feet | unit:FT | Unit of length defined as being 0 |
| GigaByte | unit:GigaBYTE | Unit for digital information equivalent to 1000 megabytes |
| KiloByte | unit:KiloBYTE | Unit for digital information equivalent to 1000 bytes |
| Metre | unit:M | Metric and SI base unit of distance |
| MegaByte | unit:MegaBYTE | Unit for digital information equivalent to 1000 kilobytes |
| TeraByte | unit:TeraBYTE | Unit for digital information equivalent to 1000 gigabytes |




## Slots

| Name | Description |
| ---  | --- |
| [has_unit](has_unit.md) | Unit of some quantity |






## See Also

* [https://www.qudt.org/doc/DOC_VOCAB-UNITS.html](https://www.qudt.org/doc/DOC_VOCAB-UNITS.html)

## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: UnitEnum
description: Units of measurement. Definitions are taken from the Quantities, Units,
  Dimensions and Data Types Ontologies (QUDT)
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.qudt.org/doc/DOC_VOCAB-UNITS.html
rank: 1000
permissible_values:
  Feet:
    text: Feet
    description: Unit of length defined as being 0.3048 metres
    meaning: unit:FT
  GigaByte:
    text: GigaByte
    description: Unit for digital information equivalent to 1000 megabytes
    meaning: unit:GigaBYTE
  KiloByte:
    text: KiloByte
    description: Unit for digital information equivalent to 1000 bytes
    meaning: unit:KiloBYTE
  Metre:
    text: Metre
    description: Metric and SI base unit of distance
    meaning: unit:M
  MegaByte:
    text: MegaByte
    description: Unit for digital information equivalent to 1000 kilobytes
    meaning: unit:MegaBYTE
  TeraByte:
    text: TeraByte
    description: Unit for digital information equivalent to 1000 gigabytes
    meaning: unit:TeraBYTE

```
</details>
