# av-efi-schema

Metadata schema for persistent film identifiers developed in the
AVefi project

URI: https://av-efi.net/schema/av-efi-schema

Name: av-efi-schema



## Classes

| Class | Description |
| --- | --- |
| [DescriptionResource](DescriptionResource.md) | Metadata about the PID rather than the identified object, i.e. who modified the PID metadata record when, making what changes |
| [Entity](Entity.md) | A generic grouping for all described things |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Activity](Activity.md) | FIAF Moving Image Cataloguing Manual 1.4.1.1 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Agent](Agent.md) | Agent involved in some activity related to the moving image resource. For agents of type "Person" specify name according to the convention "family name, given name" |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AuthorityResource](AuthorityResource.md) | Root class for all identifiers from some kind of authority or public register widely accepted in the community |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[AVefiResource](AVefiResource.md) | Handle with the prefix allocated for AVefi (eventually) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DOIResource](DOIResource.md) | Digital Object Identifier maintained by the DOI Foundation and commonly used for scientific publications including films. |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[FilmportalResource](FilmportalResource.md) | Identifier of the German Filmportal.de |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[GNDResource](GNDResource.md) | Gemeinsame Normdatei (GND) identifier maintained by Deutsche Nationalbibliothek (German National Library) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ISILResource](ISILResource.md) | International Standard Identifier for Libraries and Related Organizations including (film) archives |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[TGNResource](TGNResource.md) | Getty Thesaurus of Geographic Names ID |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[VIAFResource](VIAFResource.md) | Virtual International Authority File identifier hosted by OCLC. The data is accumulated from various well established authority files from different parts of teh world |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[WikidataResource](WikidataResource.md) | Identifier for Wikidata entities |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Duration](Duration.md) | Total running time of the described object in ISO 8601 duration format. The examples section lists possible values for the has_value slot. See also: FIAF Moving Image Cataloguing Manual 2.3.5.3, 3.1.5.11 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Event](Event.md) | Significant event in the lifecycle of moving image work / variant, manifestation or item. Always specify the type of event and if possible a date or a period of time via has_date. Specify located_in as appropriate, e.g. the country where the principal offices or production facilities of the production company are located for a production event. Involved parties in various roles can be linked via has_activity. See also: FIAF Moving Image Cataloguing Manual 1.4.2, 2.4.2, 3.3.2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Extent](Extent.md) | Physical length or size of the described object. See also: FIAF Moving Image Cataloguing Manual 2.3.5.2, 3.1.5.8 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Format](Format.md) | FIAF Moving Image Cataloguing Manual 2.3.4.1, 3.1.5.1 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Audio](Audio.md) | FIAF Moving Image Cataloguing Manual D.7.2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DigitalFile](DigitalFile.md) | FIAF Moving Image Cataloguing Manual D.7.2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[DigitalFileEncoding](DigitalFileEncoding.md) | FIAF Moving Image Cataloguing Manual D.7.2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Film](Film.md) | FIAF Moving Image Cataloguing Manual D.7.2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Optical](Optical.md) | FIAF Moving Image Cataloguing Manual D.7.2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Video](Video.md) | FIAF Moving Image Cataloguing Manual D.7.2 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Genre](Genre.md) | Genre describes categories of Works, characterized by similar plots, themes, settings, situations, and characters. Examples of genres are “westerns” and “thrillers”. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.1 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[GeographicName](GeographicName.md) | Name of country, region or other location. Names should be taken from appropriate authorities (e.g. GND) and recorded as a human readable string in the name attribute and as linked data in the same_as attribute. See also: FIAF Moving Image Cataloguing Manual 1.3.3, D.4 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Language](Language.md) | Provide language code from ISO 639-2 (Part 2: Alpha-3) and a list of language usage terms from our controlled vocabulary. See also: FIAF Moving Image Cataloguing Manual 1.3.5, 2.3.3 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MovingImageRecordCollection](MovingImageRecordCollection.md) | A holder for MovingImageRecord objects |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[PIDRecord](PIDRecord.md) | Grouping for all entities that represent a PID metadata record |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[MovingImageRecord](MovingImageRecord.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ManifestationOrItem](ManifestationOrItem.md) | None |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Item](Item.md) | FIAF Moving Image Cataloguing Manual 3.0 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Manifestation](Manifestation.md) | FIAF Moving Image Cataloguing Manual 2.0 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[WorkVariant](WorkVariant.md) | FIAF Moving Image Cataloguing Manual 1.0 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Subject](Subject.md) | Subject descriptor terms for the content of a film specifying its period, themes, locations, etc. Not to be confused with Genre. Provide name and if at all possible identifier(s) from supported authorities in the same_as slot. See also: FIAF Moving Image Cataloguing Manual 1.4.3 and FIAF Glossary of Filmographic Terms D.2.3 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Title](Title.md) | FIAF Moving Image Cataloguing Manual 1.3.2, 2.3.2, 3.1.2 |



## Slots

| Slot | Description |
| --- | --- |
| [category](category.md) |  |
| [code](code.md) | ISO 639-2 code for the Representation of Names of Languages (Part 2: Alpha-3) |
| [described_by](described_by.md) | Also record some metadata about the PID itself rather than the identified obj... |
| [element_type](element_type.md) |  |
| [has_access_status](has_access_status.md) |  |
| [has_activity](has_activity.md) | Associate activity (and subsequently agents) with event |
| [has_agent](has_agent.md) | Agent involved in some activity related to the moving image resource |
| [has_alternate_name](has_alternate_name.md) |  |
| [has_alternative_title](has_alternative_title.md) | Additional title(s) associated with the work / variant, manifestation, or ite... |
| [has_date](has_date.md) | Date (or interval/period) when an event has taken place |
| [has_duration](has_duration.md) | Total running time of the described object in ISO 8601 duration format |
| [has_event](has_event.md) | Associate event(s) with a moving image record |
| [has_extent](has_extent.md) | Physical length or size of the described object |
| [has_form](has_form.md) | Form describes the format and/or purpose of a Work, e |
| [has_format](has_format.md) |  |
| [has_genre](has_genre.md) | Genre describes categories of Works, characterized by similar plots, themes, ... |
| [has_history](has_history.md) | Link to revision history of this PID |
| [has_issuer_id](has_issuer_id.md) | Identifier for the responsible party as an URI suitable for linked data |
| [has_issuer_name](has_issuer_name.md) | Name of the responsible party |
| [has_item](has_item.md) | Indicate AVefi Items the institution has registered as part of the manifestat... |
| [has_name](has_name.md) | A human-readable name for a thing |
| [has_note](has_note.md) | FIAF Moving Image Cataloguing Manual Appendix B |
| [has_ordering_name](has_ordering_name.md) | Provide normalised form, e |
| [has_primary_title](has_primary_title.md) | Primary title to be displayed in search results etc |
| [has_record](has_record.md) |  |
| [has_subject](has_subject.md) | Subject descriptor terms for the content of a film specifying its period, the... |
| [has_unit](has_unit.md) | Unit of some quantity |
| [has_value](has_value.md) | Value of some quantity |
| [has_webresource](has_webresource.md) | Link to data provider's own presentation of manifestation or item on the web |
| [id](id.md) | A unique identifier for a thing |
| [in_language](in_language.md) | FIAF Moving Image Cataloguing Manual 1 |
| [is_copy_of](is_copy_of.md) | Link to AVefi item registered by another institution indicating that the two ... |
| [is_derivative_of](is_derivative_of.md) | Link to AVefi item from which this one has been derived in whole or in part, ... |
| [is_item_of](is_item_of.md) | Indicate AVefi Manifestation the item belongs to |
| [is_manifestation_of](is_manifestation_of.md) | Indicate AVefi WorkVariant (possibly more but no less than one) that is subje... |
| [is_part_of](is_part_of.md) | Relate, for instance, episodes to a series / serial |
| [is_variant_of](is_variant_of.md) | Link to the reference WorkVariant for the currently described variant |
| [last_modified](last_modified.md) | Timestamp (in UTC) for the latest modification to any field in the PID metada... |
| [located_in](located_in.md) |  |
| [same_as](same_as.md) |  |
| [type](type.md) |  |
| [usage](usage.md) |  |
| [value_is](value_is.md) | Qualifier indicating the precision of an extent value or duration |
| [variant_type](variant_type.md) | FIAF Moving Image Cataloguing Manual D |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [ActivityTypeEnum](ActivityTypeEnum.md) | Activity types / roles |
| [AgentTypeEnum](AgentTypeEnum.md) | FIAF Moving Image Cataloguing Manual 1 |
| [EventTypeEnum](EventTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [FormatAudioTypeEnum](FormatAudioTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [FormatDigitalFileEncodingTypeEnum](FormatDigitalFileEncodingTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [FormatDigitalFileTypeEnum](FormatDigitalFileTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [FormatFilmTypeEnum](FormatFilmTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [FormatOpticalTypeEnum](FormatOpticalTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [FormatVideoTypeEnum](FormatVideoTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [ItemAccessStatusEnum](ItemAccessStatusEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [ItemElementTypeEnum](ItemElementTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [LanguageUsageEnum](LanguageUsageEnum.md) | FIAF Moving Image Cataloguing Manual 2 |
| [ManifestationTypeEnum](ManifestationTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [PrecisionEnum](PrecisionEnum.md) | Qualifier indicating the precision of an extent value or duration |
| [TitleTypeEnum](TitleTypeEnum.md) | FIAF Moving Image Cataloguing Manual A |
| [UnitEnum](UnitEnum.md) | Units of measurement |
| [VariantTypeEnum](VariantTypeEnum.md) | FIAF Moving Image Cataloguing Manual D |
| [WorkFormEnum](WorkFormEnum.md) | FIAF Glossary of Filmographic Terms D |
| [WorkVariantTypeEnum](WorkVariantTypeEnum.md) | Work/Variant description type |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
