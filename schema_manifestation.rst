+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|ID   |Name                 |Cardinality|Definition                                        |Allowed values, constraints, remarks              |
+=====+=====================+===========+==================================================+==================================================+
|1    |identifier           |1          |An unambiguous reference to the resource within a |Free text                                         |
|     |                     |           |given context, preferably the (EFI) devloped in   |                                                  |
|     |                     |           |the context of this project.                      |                                                  |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|2    |isVersionOf          |1-n        |PID of the Work/Variant                           |handle                                            |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|3    |sameAs               |0-n        |PID of same version archived at another           |handle                                            |
|     |                     |           |institution, e.g. due to cooperative restoration  |                                                  |
|     |                     |           |project                                           |                                                  |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|4    |title                |0-n        |A word, phrase, character, or group of characters,|Free text                                         |
|     |                     |           |naming the manifestation or variant. Depending on |                                                  |
|     |                     |           |the cataloguing rules in use, titles may be       |                                                  |
|     |                     |           |determined from the item itself, or from any      |                                                  |
|     |                     |           |suitable secondary source.                        |                                                  |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|4.1  |titleType            |1          |                                                  |`Controlled list of values                        |
|     |                     |           |                                                  |<https://raw.githubusercontent.com/               |
|     |                     |           |                                                  |AV-EFI/av-efi-schema/                             |
|     |                     |           |                                                  |main/Controlled_Vocabularies/                     |
|     |                     |           |                                                  |manifestation_4.1_titleType.json>`_               |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|5    |releaseDate          |0-1        |Publication Date                                  |ISO 8601                                          |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|6    |productionYear       |0-1        |Production year or timespan                       |Four digit integer                                |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|7    |manifestationType    |0-n        |A word or phrase denoting the relationship between|`Controlled list of values                        |
|     |                     |           |the manifestation and the variant or              |<https://raw.githubusercontent.com/               |
|     |                     |           |cinematographic work that it manifests. May be    |AV-EFI/av-efi-schema/                             |
|     |                     |           |omitted if no other manifestation is known.       |main/Controlled_Vocabularies/                     |
|     |                     |           |                                                  |manifestation_7_manifestationType.json>`_         |                                    |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|8    |hasAgent             |0-n        |An entity that is involved in the creation,       |Free text                                         |
|     |                     |           |realization, curation or exploitation of a        |                                                  |
|     |                     |           |Manifestation.                                    |                                                  |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|9    |source               |1          |The name of the archive or other organisation     |                                                  |
|     |                     |           |supplying the record.                             |                                                  |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|9.1  |sourceName           |1          |                                                  |Free text                                         |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|9.2  |sourceIdentifier     |1          |                                                  |Free text                                         |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|9.3  |sourceAttribution    |1          |                                                  |                                                  |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|9.3.1|sourceAttributionDate|1          |                                                  |ISO 8601                                          |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|9.3.2|sourceAttributionType|1          |                                                  |                                                  |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
|10   |lastModified         |1-n        |Date and time of last update to metadata record.  |ISO 8601                                          |
+-----+---------------------+-----------+--------------------------------------------------+--------------------------------------------------+
