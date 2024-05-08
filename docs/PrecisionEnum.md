# Enum: PrecisionEnum




_Qualifier indicating the precision of an extent value or duration_



URI: [PrecisionEnum](PrecisionEnum.md)

## Permissible Values

| Value | Meaning | Description |
| --- | --- | --- |
| Approximate | None | Value may be inaccurate but is regarded to be close to the real thing |
| Uncertain | None | Sources for the given value are deemed unreliable, so it may as well be off t... |




## Slots

| Name | Description |
| ---  | --- |
| [value_is](value_is.md) | Qualifier indicating the precision of an extent value or duration |






## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: PrecisionEnum
description: Qualifier indicating the precision of an extent value or duration
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
permissible_values:
  Approximate:
    text: Approximate
    description: Value may be inaccurate but is regarded to be close to the real thing
  Uncertain:
    text: Uncertain
    description: Sources for the given value are deemed unreliable, so it may as well
      be off the mark

```
</details>
