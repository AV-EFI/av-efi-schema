+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|Label & level     |JSONPath                  |Cardinality|Definition                                        |Allowed values, constraints, remarks              |
+==================+==========================+===========+==================================================+==================================================+
|identifier        |$..identifier             |1          |An unambiguous reference to the resource within a |Free text                                         |
|                  |                          |           |given context, preferably the (EFI) devloped in   |                                                  |
|                  |                          |           |the context of this project.                      |                                                  |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|is version of     |$..isVersionOf            |1-n        |PID of the Work/Variant                           |handle                                            |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|same as           |$..sameAs                 |0-n        |PID of same version archived at another           |handle                                            |
|                  |                          |           |institution, e.g. due to cooperative restoration  |                                                  |
|                  |                          |           |project                                           |                                                  |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|title             |$..title                  |0-n        |A word, phrase, character, or group of characters,|Free text                                         |
|                  |                          |           |naming the manifestation or variant. Depending on |                                                  |
|                  |                          |           |the cataloguing rules in use, titles may be       |                                                  |
|                  |                          |           |determined from the item itself, or from any      |                                                  |
|                  |                          |           |suitable secondary source.                        |                                                  |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|`*` type          |$..title.type             |1          |                                                  |`Controlled list of values                        |
|                  |                          |           |                                                  |<https://raw.githubusercontent.com/               |
|                  |                          |           |                                                  |AV-EFI/av-efi-schema/                             |
|                  |                          |           |                                                  |main/Controlled_Vocabularies/                     |
|                  |                          |           |                                                  |manifestation_4.1_titleType.json>`_               |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|release date      |$..releaseDate            |0-1        |Publication Date                                  |ISO 8601                                          |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|production year   |$..productionYear         |0-1        |Production year or timespan                       |Four digit integer                                |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|manifestation type|$..manifestationType      |0-n        |A word or phrase denoting the relationship between|`Controlled list of values                        |
|                  |                          |           |the manifestation and the variant or              |<https://raw.githubusercontent.com/               |
|                  |                          |           |cinematographic work that it manifests. May be    |AV-EFI/av-efi-schema/                             |
|                  |                          |           |omitted if no other manifestation is known.       |main/Controlled_Vocabularies/                     |
|                  |                          |           |                                                  |manifestation_7_manifestationType.json>`_         |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|has agent         |$..hasAgent               |0-n        |An entity that is involved in the creation,       |Free text                                         |
|                  |                          |           |realization, curation or exploitation of a        |                                                  |
|                  |                          |           |Manifestation.                                    |                                                  |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|source            |$..source                 |1          |The name of the archive or other organisation     |                                                  |
|                  |                          |           |supplying the record.                             |                                                  |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|`*` name          |$..source.name            |1          |                                                  |Free text                                         |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|`*` identifier    |$..source.identifier      |1          |                                                  |Free text                                         |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|`*` attribution   |$..source.attribution     |1          |                                                  |                                                  |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|`**` date         |$..source.attribution.date|1          |                                                  |ISO 8601                                          |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|`**` type         |$..source.attribution.type|1          |                                                  |`Controlled list of values                        |
|                  |                          |           |                                                  |<https://raw.githubusercontent.com/               |
|                  |                          |           |                                                  |AV-EFI/av-efi-schema/                             |
|                  |                          |           |                                                  |main/Controlled_Vocabularies/                     |
|                  |                          |           |                                                  |manifestation_9.3.2_sourceAttributionType.json>`_ |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|last modified     |$..lastModified           |1-n        |Date and time of last update to metadata record.  |ISO 8601                                          |
+------------------+--------------------------+-----------+--------------------------------------------------+--------------------------------------------------+
