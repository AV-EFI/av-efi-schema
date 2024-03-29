+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|Label & level        |JSONPath                             |Cardinality|Definition                                        |Allowed values, constraints, remarks  |
+=====================+=====================================+===========+==================================================+======================================+
|title                |$..title                             |1-n        |A word, phrase, character, or group of characters,|Free Text                             |
|                     |                                     |           |normally appearing in an item, naming the item or |                                      |
|                     |                                     |           |the work contained in it.                         |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` type             |$..title.type                        |1          |                                                  |`Controlled list of values            |
|                     |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |     
|                     |                                     |           |                                                  |work_1.1_titleType.json>`_            |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|series               |$..series                            |0-1        |A series is a group of separate items related to  |                                      |
|                     |                                     |           |one another by the fact that each item bears, in  |                                      |
|                     |                                     |           |addition to its own title, a collective title     |                                      |
|                     |                                     |           |applying to the group as a whole.  A serial is a  |                                      |
|                     |                                     |           |type of “short subject” work which is             |                                      |
|                     |                                     |           |characterized principally by the episodic         |                                      |
|                     |                                     |           |development of a story.                           |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` identifier       |$..series.identifier                 |0-1        |                                                  |URI                                   |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` title            |$..series.title                      |0-1        |                                                  |Free Text                             |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`**` type            |$..series.title.type                 |1          |                                                  |`Controlled list of values            |
|                     |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_2.2.1_seriesTitleType.json>`_    |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|cast                 |$..cast                              |0 – n      |A collective term for actors and their roles. A   |                                      |
|                     |                                     |           |broad distinction is made between cast and credits|                                      |
|                     |                                     |           |by defining cast as those in front of the camera  |                                      |
|                     |                                     |           |and credits as those behind the camera.           |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` name             |$..cast.name                         |1          |                                                  |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`**` first name      |$..cast.name.firstName               |0-1        |                                                  |Free Text                             |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`**` last name       |$..cast.name.lastNAme                |0-1        |                                                  |Free Text                             |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` identifier       |$..cast.identifier                   |0-1        |                                                  |URI                                   |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|credits              |$..credits                           |0 – n      |The names and functions of persons responsible for|                                      |
|                     |                                     |           |the production and/or artistic or intellectual    |                                      |
|                     |                                     |           |content of a cinematographic work. The term       |                                      |
|                     |                                     |           |“credits” is often used more specifically to      |                                      |
|                     |                                     |           |distinguish between those behind the camera from  |                                      |
|                     |                                     |           |“cast,” those in front of the camera.             |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` name             |$..credits.name                      |1          |                                                  |Free Text                             |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`**` first name      |$..credits.name.firstName            |           |                                                  |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`**` last name       |$..credits.name.lastName             |           |                                                  |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` role             |$..credits.role                      |1          |                                                  |`Controlled list of values            |
|                     |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_4.2_creditsRole.json>`_          |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` identifier       |$..credits.identifier                |1          |                                                  |URI                                   |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|production company   |$..productionCompany                 |0 – n      |The name of an organisation or company under whose|Free Text                             |
|                     |                                     |           |financial, technical and organisational management|                                      |
|                     |                                     |           |a cinematographic work is made.                   |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` identifier       |$..productionCompany.identifier      |0-1        |                                                  |URI                                   |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|country of reference |$..countryOfReference                |0 – n      |The country or countries where the principal      |ISO 3166-1 and ISO 3166-3 Alpha-2 code|
|                     |                                     |           |offices of the production company (or companies)  |                                      |
|                     |                                     |           |of a cinematographic work are located. (A         |                                      |
|                     |                                     |           |geographical entity represented as coded value    |                                      |
|                     |                                     |           |from a controlled vocabulary. Used in various     |                                      |
|                     |                                     |           |places throughout the schema.)                    |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|original format      |$..originalFormat                    |0 – 1      |The description of the physical artefact on which |                                      |
|                     |                                     |           |the first known manifestation of a cinematographic|                                      |
|                     |                                     |           |work was fixed.                                   |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` audio material   |$..originalFormat.audioMaterialFormat|           |                                                  |`Controlled list of values            |
|format               |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_7.1_audioMaterialFormat.json>`_  |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` audio material   |$..originalFormat.audioMaterialType  |           |                                                  |`Controlled list of values            |
|type                 |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_7.2_audioMaterialType.json>`_    |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` video material   |$..originalFormat.videoMaterialFormat|           |                                                  |`Controlled list of values            |
|format               |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_7.3_videoMaterialFormat.json>`_  |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` video material   |$..originalFormat.videoMaterialType  |           |                                                  |`Controlled list of values            |
|type                 |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_7.4_videoMaterialType.json>`_    |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|original length      |$..originalLength                    |0-n        |The total physical length of the first known      |Two decimals digits number            |
|                     |                                     |           |manifestation of a cinematographic work, measured |                                      |
|                     |                                     |           |in feet or metres.                                |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` unit             |$..originalLength.unit               |1          |                                                  |`Controlled list of values            |
|                     |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_8.1_originalLengthUnit.json>`_   |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|original duration    |$..originalDuration                  |0-n        |The running time of the first known manifestation |ISO 8601 PnYnMnDTnHnMnS               |
|                     |                                     |           |of a cinematographic work, measured in minutes and|                                      |
|                     |                                     |           |seconds.                                          |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|original language    |$..originalLanguage                  |0-n        |The language or languages of the spoken, sung or  |ISO 639-2 (T) Alpha 3                 |
|                     |                                     |           |written content of the first known manifestation  |                                      |
|                     |                                     |           |of a cinematographic work.                        |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|year of reference    |$..yearOfReference                   |0-n        |A date asssociated with an event in the life cycle|                                      |
|                     |                                     |           |of the cinematographic work, typically associated |                                      |
|                     |                                     |           |with its creation, availability or registration   |                                      |
|                     |                                     |           |(for example for copyright purposes).             |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` start            |$..yearOfReference.start             |0-1        |                                                  |four digit integer                    |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` end              |$..yearOfReference.end               |0-1        |                                                  |four digit integer                    |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` type             |$..yearOfReference.type              |1          |                                                  |`Controlled list of values            |
|                     |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_11.3_yearOfReferenceType.json>`_ |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|genre                |$..genre                             |0-n        |A descriptor or descriptors, preferably from a    |`Controlled list of values            |
|                     |                                     |           |controlled vocabulary which characterise the      |<https://raw.githubusercontent.com/   |
|                     |                                     |           |general style of a cinematographic work.          |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_12_genre.json>`_                 |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|related identifier   |$..relatedIdentifier                 |0-n        |A reference to a related cinematographic work,    |URI                                   |
|                     |                                     |           |preferably by means of a formal identification    |                                      |
|                     |                                     |           |system. “Has a relationship to promotional        |                                      |
|                     |                                     |           |material ”, “Has a relationship to an “object” (a |                                      |
|                     |                                     |           |non-moving image resource)” “Has a relationship to|                                      |
|                     |                                     |           |an archival document” (FIAF)                      |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|source               |$..source                            |1          |The name of the archive or other organisation     |                                      |
|                     |                                     |           |supplying the record.                             |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` name             |$..source.name                       |1          |                                                  |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` identifier       |$..source.identifier                 |1          |                                                  |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`*` attribution      |$..source.attribution                |1          |                                                  |                                      |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`**` date            |$..source.attribution.date           |1          |                                                  |ISO 8601                              |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|`**` type            |$..source.attribution.type           |1          |                                                  |`Controlled list of values            |
|                     |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_14.3.2_sourceAttributionType     |
|                     |                                     |           |                                                  |.json>`_                              |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|last modified        |$..lastModified                      |1          |Date and time of last update to metadata record.  |ISO 8601                              |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|subject              |$..subject                           |0-1        |subjects that describe the content of the Work    |`Controlled list of values            |
|                     |                                     |           |                                                  |<https://raw.githubusercontent.com/   |
|                     |                                     |           |                                                  |AV-EFI/av-efi-schema/                 |
|                     |                                     |           |                                                  |main/Controlled_Vocabularies/         |
|                     |                                     |           |                                                  |work_16_subject.json>`_               |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
|schema version       |$..schemaVersion                     |1          |Version of the used schema for a specific dataset |Controlled list of values             |
+---------------------+-------------------------------------+-----------+--------------------------------------------------+--------------------------------------+
