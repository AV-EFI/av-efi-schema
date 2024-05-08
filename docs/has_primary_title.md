

# Slot: has_primary_title


_Primary title to be displayed in search results etc. The type should be PreferredTitle for works / variants and TitleProper for manifestations / items. If not available, type must be SuppliedDevisedTitle, instead._



URI: [avefi:has_primary_title](https://av-efi.net/schema/av-efi-schema/has_primary_title)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ManifestationOrItem](ManifestationOrItem.md) |  |  no  |
| [WorkVariant](WorkVariant.md) | FIAF Moving Image Cataloguing Manual 1 |  no  |
| [MovingImageRecord](MovingImageRecord.md) |  |  no  |
| [Item](Item.md) | FIAF Moving Image Cataloguing Manual 3 |  no  |
| [Manifestation](Manifestation.md) | FIAF Moving Image Cataloguing Manual 2 |  no  |







## Properties

* Range: [Title](Title.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_primary_title
description: Primary title to be displayed in search results etc. The type should
  be PreferredTitle for works / variants and TitleProper for manifestations / items.
  If not available, type must be SuppliedDevisedTitle, instead.
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
alias: has_primary_title
owner: MovingImageRecord
domain_of:
- MovingImageRecord
range: Title
required: true

```
</details>