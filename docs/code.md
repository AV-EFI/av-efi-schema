

# Slot: code


_ISO 639-2 code for the Representation of Names of Languages (Part 2: Alpha-3)_



URI: [avefi:code](https://av-efi.net/schema/av-efi-schema/code)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Language](Language.md) | Provide language code from ISO 639-2 (Part 2: Alpha-3) and a list of language... |  no  |







## Properties

* Range: [String](String.md)

* Required: True

* Regex pattern: `^[a-z]{3}$`





## See Also

* [https://id.loc.gov/vocabulary/iso639-2.html](https://id.loc.gov/vocabulary/iso639-2.html)

## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: code
description: 'ISO 639-2 code for the Representation of Names of Languages (Part 2:
  Alpha-3)'
from_schema: https://av-efi.net/schema/av-efi-schema
see_also:
- https://id.loc.gov/vocabulary/iso639-2.html
rank: 1000
alias: code
owner: Language
domain_of:
- Language
range: string
required: true
pattern: ^[a-z]{3}$

```
</details>