

# Slot: described_by


_Also record some metadata about the PID itself rather than the identified object_



URI: [wdrs:describedby](http://www.w3.org/2007/05/powder-s#describedby)



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

* Range: [DescriptionResource](DescriptionResource.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: described_by
description: Also record some metadata about the PID itself rather than the identified
  object
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: wdrs:describedby
alias: described_by
domain_of:
- MovingImageRecord
range: DescriptionResource
required: true
inlined: true

```
</details>