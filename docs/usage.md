

# Slot: usage

URI: [avefi:usage](https://av-efi.net/schema/av-efi-schema/usage)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Language](Language.md) | Provide language code from ISO 639-2 (Part 2: Alpha-3) and a list of language... |  no  |







## Properties

* Range: [LanguageUsageEnum](LanguageUsageEnum.md)

* Multivalued: True

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: usage
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
multivalued: true
alias: usage
owner: Language
domain_of:
- Language
range: LanguageUsageEnum
required: true

```
</details>