

# Slot: in_language


_FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3_



URI: [avefi:in_language](https://av-efi.net/schema/av-efi-schema/in_language)



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

* Range: [Language](Language.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: in_language
description: FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3
from_schema: https://av-efi.net/schema/av-efi-schema
related_mappings:
- fiaf:hasLanguage
- schema:inLanguage
rank: 1000
multivalued: true
alias: in_language
domain_of:
- MovingImageRecord
range: Language
inlined: true
inlined_as_list: true

```
</details>