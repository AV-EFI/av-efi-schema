+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|Label & level            |JSONPath                   |Cardinality|Definition                                        |Allowed values, constraints, remarks      |
|                         |                           |           |                                                  |                                          |
+=========================+===========================+===========+==================================================+==========================================+
|title                    |$..title                   |0-1        |The title of an item contained in a dataObject may|Free text                                 |
|                         |                           |           |differ, either slightly or wholly, from the title |                                          |
|                         |                           |           |of the Version and/or Work/Variant to which it is |                                          |
|                         |                           |           |linked hierarchically. In particular, where an    |                                          |
|                         |                           |           |incomplete physical product of the Version has    |                                          |
|                         |                           |           |been acquired and been catalogued as an item      |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|physical description     |$..physicalDescription     |0-n        |The broad media type of the item contained in a   |`Controlled list of values                |
|                         |                           |           |dataObject (e.g., film, video, audio, optical,    |<https://raw.githubusercontent.com/       |
|                         |                           |           |digital file). Recording this high-level          |AV-EFI/av-efi-schema/                     |
|                         |                           |           |information will enable simple searching for only |main/Controlled_Vocabularies/             |
|                         |                           |           |film, video, digital, etc. elements rather than   |item_2_physicalDescription.json>`_        |
|                         |                           |           |searching by all possible formats and carriers.   |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|specific carrier type    |$..specificCarrierType     |0-1        |The physical carrier storing the digital file.For |`Controlled list of values                |
|                         |                           |           |digital files, it is most important for users to  |<https://raw.githubusercontent.com/       |
|                         |                           |           |immediately identify the file container or wrapper|AV-EFI/av-efi-schema/                     |
|                         |                           |           |(MXF, MOV, DPX, etc.) Institutions should develop |main/Controlled_Vocabularies/             |
|                         |                           |           |standard lists of terms to indicate the specific  |item_3_specificCarrierType.json>`_        |
|                         |                           |           |carrier type or refer to authoritative existing   |                                          |
|                         |                           |           |lists.                                            |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|preservation status      |$..preservationStatus      |0-1        |Description of the preservation or access status  |`Controlled list of values                |
|                         |                           |           |of the dataObject, for example Master, Viewing,   |<https://raw.githubusercontent.com/       |
|                         |                           |           |etc. Select term from a controlled list.          |AV-EFI/av-efi-schema/                     |
|                         |                           |           |                                                  |main/Controlled_Vocabularies/             |
|                         |                           |           |                                                  |item_4_preservationStatus.json>`_         |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|supplementary information|$..supplementaryInformation|0-1        |Additional information specific to the item       |Free text                                 |
|                         |                           |           |contained in the dataObject                       |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|file size                |$..fileSize                |0-1        |The numerical measurement indicating the size of  |Unsigned Integer and the Unit             |
|                         |                           |           |the digital asset’s file(s), in KB, MB, GB, or TB.|                                          |
|                         |                           |           |(Total size of Item)                              |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|is data object of        |$..isDataObjectOf          |1          |PID of manifestion/version                        |handle                                    |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|identifier               |$..identifier              |1          |An unambiguous reference to the resource within a |Free text                                 |
|                         |                           |           |given context                                     |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|language version         |$..languageVersion         |0-n        |Language version of the item                      |`Controlled list of values                |
|                         |                           |           |                                                  |<https://raw.githubusercontent.com/       |
|                         |                           |           |                                                  |AV-EFI/av-efi-schema/                     |
|                         |                           |           |                                                  |main/Controlled_Vocabularies/             |
|                         |                           |           |                                                  |item_9_languageVersion.json>`_            |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|source                   |$..source                  |1          |The name of the archive or other organisation     |                                          |
|                         |                           |           |supplying the record.                             |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|`*` name                 |$..source.name             |1          |                                                  |Free text                                 |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|`*` identifier           |$..source.identifier       |1          |                                                  |Free text                                 |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|`*` attribution          |$..source.attribution      |1          |                                                  |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|`**` date                |$..source.attribution.date |1          |                                                  |ISO 8601                                  |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|`**` type                |$..source.attribution.type |1          |                                                  |`Controlled list of values                |
|                         |                           |           |                                                  |<https://raw.githubusercontent.com/       |
|                         |                           |           |                                                  |AV-EFI/av-efi-schema/                     |
|                         |                           |           |                                                  |main/Controlled_Vocabularies/             |
|                         |                           |           |                                                  |item_10.3.2_sourceAttributionType.json>`_ |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|last modified            |$..lastModified            |1-n        |Date and time of last update to metadata record.  |ISO 8601                                  |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
|same as                  |$..sameAs                  |0-n        |PID of same item archived at another institution, |handle                                    |
|                         |                           |           |e.g. due to cooperative restoration project       |                                          |
+-------------------------+---------------------------+-----------+--------------------------------------------------+------------------------------------------+
