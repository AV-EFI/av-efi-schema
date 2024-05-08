

# Slot: is_item_of


_Indicate AVefi Manifestation the item belongs to. Every item must be associated with a manifestation from the same data provider_



URI: [avefi:is_item_of](https://av-efi.net/schema/av-efi-schema/is_item_of)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Item](Item.md) | FIAF Moving Image Cataloguing Manual 3 |  no  |







## Properties

* Range: [AVefiResource](AVefiResource.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: is_item_of
description: Indicate AVefi Manifestation the item belongs to. Every item must be
  associated with a manifestation from the same data provider
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
alias: is_item_of
domain_of:
- Item
range: AVefiResource
required: true

```
</details>