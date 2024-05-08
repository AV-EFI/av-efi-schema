

# Slot: has_date


_Date (or interval/period) when an event has taken place. A subset of ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers ? (uncertain date) and ~ (approximate date). See examples and references for more information_



URI: [avefi:has_date](https://av-efi.net/schema/av-efi-schema/has_date)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Event](Event.md) | Significant event in the lifecycle of moving image work / variant, manifestat... |  no  |







## Properties

* Range: [String](String.md)

* Regex pattern: `^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$`






## Examples

| Value |
| --- |
| 2024-04-24 |
| 2024-04 |
| 2024 |
| 2024~ |
| 2024? |
| 2023/2024 |

## See Also

* [https://www.loc.gov/standards/datetime/](https://www.loc.gov/standards/datetime/)

## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_date
description: Date (or interval/period) when an event has taken place. A subset of
  ISO 8601 is supported, more specifically, EDTF conformance level 0 as well as qualifiers
  ? (uncertain date) and ~ (approximate date). See examples and references for more
  information
notes:
- https://www.w3.org/TR/xmlschema11-2/#date
examples:
- value: '2024-04-24'
  description: complete date, i.e. year, month and day
- value: 2024-04
  description: year and month
- value: '2024'
  description: year only
- value: 2024~
  description: approximate date (2024 or at least close to 2024)
- value: 2024?
  description: uncertain date (2024 or may be something different)
- value: 2023/2024
  description: interval (2023 until 2024)
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://www.loc.gov/standards/datetime/
rank: 1000
alias: has_date
domain_of:
- Event
range: string
pattern: ^-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?(/-?([1-9][0-9]{3,}|0[0-9]{3})(-(0[1-9]|1[0-2])(-(0[1-9]|[12][0-9]|3[01]))?)?[?~]?)?$

```
</details>