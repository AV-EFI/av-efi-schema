

# Slot: has_ordering_name


_Provide normalised form, e.g. for sorting by title_



URI: [avefi:has_ordering_name](https://av-efi.net/schema/av-efi-schema/has_ordering_name)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Title](Title.md) | FIAF Moving Image Cataloguing Manual 1 |  no  |







## Properties

* Range: [String](String.md)






## Examples

| Value |
| --- |
| American in Paris, An |
| Star Wars: Episode 9 – Der Aufstieg Skywalkers |

## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_ordering_name
description: Provide normalised form, e.g. for sorting by title
examples:
- value: American in Paris, An
  description: 'For display title: An American in Paris'
- value: 'Star Wars: Episode 9 – Der Aufstieg Skywalkers'
  description: 'For display title: Star Wars: Episode IX – Der Aufstieg Skywalkers'
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
alias: has_ordering_name
domain_of:
- Title
range: string

```
</details>