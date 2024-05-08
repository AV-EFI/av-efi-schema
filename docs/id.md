

# Slot: id


_A unique identifier for a thing_



URI: [schema:identifier](http://schema.org/identifier)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ISILResource](ISILResource.md) | International Standard Identifier for Libraries and Related Organizations inc... |  yes  |
| [VIAFResource](VIAFResource.md) | Virtual International Authority File identifier hosted by OCLC |  yes  |
| [GNDResource](GNDResource.md) | Gemeinsame Normdatei (GND) identifier maintained by Deutsche Nationalbiblioth... |  yes  |
| [ManifestationOrItem](ManifestationOrItem.md) |  |  no  |
| [WikidataResource](WikidataResource.md) | Identifier for Wikidata entities |  yes  |
| [PIDRecord](PIDRecord.md) | Grouping for all entities that represent a PID metadata record |  no  |
| [DOIResource](DOIResource.md) | Digital Object Identifier maintained by the DOI Foundation and commonly used ... |  yes  |
| [WorkVariant](WorkVariant.md) | FIAF Moving Image Cataloguing Manual 1 |  no  |
| [MovingImageRecord](MovingImageRecord.md) |  |  no  |
| [FilmportalResource](FilmportalResource.md) | Identifier of the German Filmportal |  yes  |
| [TGNResource](TGNResource.md) | Getty Thesaurus of Geographic Names ID |  yes  |
| [Item](Item.md) | FIAF Moving Image Cataloguing Manual 3 |  no  |
| [AVefiResource](AVefiResource.md) | Handle with the prefix allocated for AVefi (eventually) |  yes  |
| [AuthorityResource](AuthorityResource.md) | Root class for all identifiers from some kind of authority or public register... |  yes  |
| [Manifestation](Manifestation.md) | FIAF Moving Image Cataloguing Manual 2 |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: id
description: A unique identifier for a thing
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: schema:identifier
identifier: true
alias: id
domain_of:
- PIDRecord
- AuthorityResource
range: uriorcurie
required: true

```
</details>