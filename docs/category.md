

# Slot: category

URI: [rdf:type](http://www.w3.org/1999/02/22-rdf-syntax-ns#type)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Activity](Activity.md) | FIAF Moving Image Cataloguing Manual 1 |  no  |
| [Extent](Extent.md) | Physical length or size of the described object |  no  |
| [Item](Item.md) | FIAF Moving Image Cataloguing Manual 3 |  no  |
| [GeographicName](GeographicName.md) | Name of country, region or other location |  no  |
| [AuthorityResource](AuthorityResource.md) | Root class for all identifiers from some kind of authority or public register... |  no  |
| [MovingImageRecordCollection](MovingImageRecordCollection.md) | A holder for MovingImageRecord objects |  no  |
| [Language](Language.md) | Provide language code from ISO 639-2 (Part 2: Alpha-3) and a list of language... |  no  |
| [Entity](Entity.md) | A generic grouping for all described things |  no  |
| [ManifestationOrItem](ManifestationOrItem.md) |  |  no  |
| [Optical](Optical.md) | FIAF Moving Image Cataloguing Manual D |  no  |
| [MovingImageRecord](MovingImageRecord.md) |  |  no  |
| [VIAFResource](VIAFResource.md) | Virtual International Authority File identifier hosted by OCLC |  no  |
| [Title](Title.md) | FIAF Moving Image Cataloguing Manual 1 |  no  |
| [DigitalFileEncoding](DigitalFileEncoding.md) | FIAF Moving Image Cataloguing Manual D |  no  |
| [AVefiResource](AVefiResource.md) | Handle with the prefix allocated for AVefi (eventually) |  no  |
| [Video](Video.md) | FIAF Moving Image Cataloguing Manual D |  no  |
| [ISILResource](ISILResource.md) | International Standard Identifier for Libraries and Related Organizations inc... |  no  |
| [WikidataResource](WikidataResource.md) | Identifier for Wikidata entities |  no  |
| [Audio](Audio.md) | FIAF Moving Image Cataloguing Manual D |  no  |
| [WorkVariant](WorkVariant.md) | FIAF Moving Image Cataloguing Manual 1 |  no  |
| [DigitalFile](DigitalFile.md) | FIAF Moving Image Cataloguing Manual D |  no  |
| [TGNResource](TGNResource.md) | Getty Thesaurus of Geographic Names ID |  no  |
| [Duration](Duration.md) | Total running time of the described object in ISO 8601 duration format |  no  |
| [Genre](Genre.md) | Genre describes categories of Works, characterized by similar plots, themes, ... |  no  |
| [Subject](Subject.md) | Subject descriptor terms for the content of a film specifying its period, the... |  no  |
| [Manifestation](Manifestation.md) | FIAF Moving Image Cataloguing Manual 2 |  no  |
| [Format](Format.md) | FIAF Moving Image Cataloguing Manual 2 |  no  |
| [GNDResource](GNDResource.md) | Gemeinsame Normdatei (GND) identifier maintained by Deutsche Nationalbiblioth... |  no  |
| [PIDRecord](PIDRecord.md) | Grouping for all entities that represent a PID metadata record |  no  |
| [DOIResource](DOIResource.md) | Digital Object Identifier maintained by the DOI Foundation and commonly used ... |  no  |
| [Film](Film.md) | FIAF Moving Image Cataloguing Manual D |  no  |
| [Agent](Agent.md) | Agent involved in some activity related to the moving image resource |  no  |
| [FilmportalResource](FilmportalResource.md) | Identifier of the German Filmportal |  no  |
| [Event](Event.md) | Significant event in the lifecycle of moving image work / variant, manifestat... |  no  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)

* Required: True





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: category
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
slot_uri: rdf:type
designates_type: true
alias: category
domain_of:
- Entity
range: uriorcurie
required: true

```
</details>