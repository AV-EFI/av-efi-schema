

# Slot: has_event


_Associate event(s) with a moving image record_



URI: [avefi:has_event](https://av-efi.net/schema/av-efi-schema/has_event)



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

* Range: [Event](Event.md)

* Multivalued: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: has_event
description: Associate event(s) with a moving image record
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
multivalued: true
alias: has_event
domain_of:
- MovingImageRecord
range: Event
inlined: true
inlined_as_list: true

```
</details>