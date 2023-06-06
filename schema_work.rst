+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|ID    |Name                       |Cardinality|Definition                                        |Allowed values, constraints, remarks  |
+======+===========================+===========+==================================================+======================================+
|1     |title                      |1-n        |A word, phrase, character, or group of characters,|Free Text                             |
|      |                           |           |normally appearing in an item, naming the item or |                                      |
|      |                           |           |the work contained in it.                         |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|1.1   |titleType                  |1          |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_1.1_titleType.json>`_            |     
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|2     |series                     |0-1        |A series is a group of separate items related to  |                                      |
|      |                           |           |one another by the fact that each item bears, in  |                                      |
|      |                           |           |addition to its own title, a collective title     |                                      |
|      |                           |           |applying to the group as a whole.  A serial is a  |                                      |
|      |                           |           |type of “short subject” work which is             |                                      |
|      |                           |           |characterized principally by the episodic         |                                      |
|      |                           |           |development of a story.                           |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|2.1   |seriesIdentifier           |0-1        |                                                  |URI                                   |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|2.2   |seriesTitle                |0-1        |                                                  |Free Text                             |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|2.2.1 |seriesTitleType            |1          |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_2.2.1_seriesTitleType.json>`_    |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|3     |cast                       |0 – n      |A collective term for actors and their roles. A   |                                      |
|      |                           |           |broad distinction is made between cast and credits|                                      |
|      |                           |           |by defining cast as those in front of the camera  |                                      |
|      |                           |           |and credits as those behind the camera.           |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|3.1   |castName                   |1          |                                                  |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|3.1.1 |castFirstName              |0-1        |                                                  |Free Text                             |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|3.1.2 |castLastName               |0-1        |                                                  |Free Text                             |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|3.2   |castIdentifier             |0-1        |                                                  |URI                                   |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|4     |credits                    |0 – n      |The names and functions of persons responsible for|                                      |
|      |                           |           |the production and/or artistic or intellectual    |                                      |
|      |                           |           |content of a cinematographic work. The term       |                                      |
|      |                           |           |“credits” is often used more specifically to      |                                      |
|      |                           |           |distinguish between those behind the camera from  |                                      |
|      |                           |           |“cast,” those in front of the camera.             |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|4.1   |creditsName                |1          |                                                  |Free Text                             |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|4.1.1 |creditsFirstName           |           |                                                  |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|4.1.2 |creditsLastName            |           |                                                  |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|4.2   |creditsRole                |1          |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_4.2_creditsRole.json>`_          |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|4.3   |creditsIdentifier          |1          |                                                  |URI                                   |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|5     |productionCompany          |0 – n      |The name of an organisation or company under whose|Free Text                             |
|      |                           |           |financial, technical and organisational management|                                      |
|      |                           |           |a cinematographic work is made.                   |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|5.1   |productionCompanyIdentifier|0-1        |                                                  |URI                                   |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|6     |countryOfReference         |0 – n      |The country or countries where the principal      |ISO 3166-1 and ISO 3166-3 Alpha-2 code|
|      |                           |           |offices of the production company (or companies)  |                                      |
|      |                           |           |of a cinematographic work are located. (A         |                                      |
|      |                           |           |geographical entity represented as coded value    |                                      |
|      |                           |           |from a controlled vocabulary. Used in various     |                                      |
|      |                           |           |places throughout the schema.)                    |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|7     |originalFormat             |0 – 1      |The description of the physical artefact on which |                                      |
|      |                           |           |the first known manifestation of a cinematographic|                                      |
|      |                           |           |work was fixed.                                   |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|7.1   |audioMaterialFormat        |           |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_7.1_audioMaterialFormat.json>`_  |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|7.2   |audioMaterialType          |           |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_7.2_audioMaterialType.json>`_    |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|7.3   |videoMaterialFormat        |           |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_7.3_videoMaterialFormat.json>`_  |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|7.4   |videoMaterialType          |           |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_7.4_videoMaterialType.json>`_    |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|8     |originalLength             |0-n        |The total physical length of the first known      |Two decimals digits number            |
|      |                           |           |manifestation of a cinematographic work, measured |                                      |
|      |                           |           |in feet or metres.                                |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|8.1   |originalLengthUnit         |1          |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_8.1_originalLengthUnit.json>`_   |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|9     |originalDuration           |0-n        |The running time of the first known manifestation |ISO 8601 PnYnMnDTnHnMnS               |
|      |                           |           |of a cinematographic work, measured in minutes and|                                      |
|      |                           |           |seconds.                                          |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|10    |originalLanguage           |0-n        |The language or languages of the spoken, sung or  |ISO 639-2 (T) Alpha 3                 |
|      |                           |           |written content of the first known manifestation  |                                      |
|      |                           |           |of a cinematographic work.                        |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|11    |yearOfReference            |0-n        |A date asssociated with an event in the life cycle|                                      |
|      |                           |           |of the cinematographic work, typically associated |                                      |
|      |                           |           |with its creation, availability or registration   |                                      |
|      |                           |           |(for example for copyright purposes).             |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|11.1  |yearOfReferenceStart       |0-1        |                                                  |four digit integer                    |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|11.2  |yearOfReferenceEnd         |0-1        |                                                  |four digit integer                    |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|11.3  |yearOfReferenceType        |1          |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_11.3_yearOfReferenceType.json>`_ |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|12    |genre                      |0-n        |A descriptor or descriptors, preferably from a    |`Controlled list of values            |
|      |                           |           |controlled vocabulary which characterise the      |<https://raw.githubusercontent.com/   |
|      |                           |           |general style of a cinematographic work.          |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_12_genre.json>`_                 |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|13    |relatedIdentifier          |0-n        |A reference to a related cinematographic work,    |URI                                   |
|      |                           |           |preferably by means of a formal identification    |                                      |
|      |                           |           |system. “Has a relationship to promotional        |                                      |
|      |                           |           |material ”, “Has a relationship to an “object” (a |                                      |
|      |                           |           |non-moving image resource)” “Has a relationship to|                                      |
|      |                           |           |an archival document” (FIAF)                      |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|14    |source                     |1          |The name of the archive or other organisation     |                                      |
|      |                           |           |supplying the record.                             |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|14.1  |sourceName                 |1          |                                                  |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|14.2  |sourceIdentifier           |1          |                                                  |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|14.3  |sourceAttribution          |1          |                                                  |                                      |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|14.3.1|sourceAttributionDate      |1          |                                                  |ISO 8601                              |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|14.3.2|sourceAttributionType      |1          |                                                  |`Controlled list of values            |
|      |                           |           |                                                  |<https://raw.githubusercontent.com/   |
|      |                           |           |                                                  |AV-EFI/av-efi-schema/                 |
|      |                           |           |                                                  |main/Controlled_Vocabularies/         |
|      |                           |           |                                                  |work_14.3.2_sourceAttributionType     |
|      |                           |           |                                                  |.json>`_                              |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|15    |lastModified               |1          |Date and time of last update to metadata record.  |ISO 8601                              |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
|16    |schemaVersion              |1          |Version of the used schema for a specific dataset |Controlled list of values             |
+------+---------------------------+-----------+--------------------------------------------------+--------------------------------------+
