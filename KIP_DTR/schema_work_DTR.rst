+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|Id    |Name                    |Cardinality|Type                     |Constraints                                       |Definition                                        |
+======+========================+===========+=========================+==================================================+==================================================+
|1     |KernelInformationProfile|0-1        |string                   |['^([\\x00-\\x2D,\\x30-\\x3F,\\x41-               |Handle-String in its general syntax. Problem here:|
|      |                        |           |                         |\\xFF])+(\\.([\\x00-\\x2D,\\x30-\\x3F,\\x41-      |Schema validation does not work properly, because |
|      |                        |           |                         |\\xFF])+)*\\/([\\x00-\\xFF])+$']                  |implementations for ecma-262-RegExp do not seem to|
|      |                        |           |                         |                                                  |correctly parse hex coded regular expressions     |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2     |cast                    |0-n        |array                    |array of subelements                              |List of actors (cast) (Context: MovieArchives)    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.1   |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic )                                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.2   |name                    |0-1        |object                   |object of subelement                              |The personal name consists of the family name and |
|      |                        |           |                         |                                                  |given name, both represented by namestrings.      |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.2.1 |family-name             |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic )                               |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.2.2 |given-name              |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic )                               |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|3     |countryOfReference      |0-n        |string                   |['/^A[^ABCHJKNPVY]|B[^CKPUX]|C                    |implicitly created because of multiple occurence  |
|      |                        |           |                         |[^BEJPQST]|D[EJKMOZ]|E[CEGHRST]|F[IJKMOR]|G[^CJ   |of child type country_of_reference: The country or|
|      |                        |           |                         |KOVXZ]|H[KMNRTU]|I[DEL-OQ-T]|J[EMOP]|K[EGHIMNPR   |countries where the principal offices of the      |
|      |                        |           |                         |WYZ]|L[ABCIKR-VY]|M[^BIJ]|N[ACEFGILOPRUZ]|OM|P[   |production company (or companies) of a            |
|      |                        |           |                         |AE-HK-NRSTWY]|QA|R[EOSUW]|S[^FPQUW]|T[^ABEIPQSU   |cinematographic work are located. ( context :     |
|      |                        |           |                         |XY]|U[AGMSYZ]|V[ACEGINU]|WF|WS|YE|YT|Z[AMW]$/ix'] |movie_db_ZIB )                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4     |credits                 |0-n        |array                    |array of subelements                              |The names and functions of persons responsible for|
|      |                        |           |                         |                                                  |the production and/or artistic or intellectual    |
|      |                        |           |                         |                                                  |content of a cinematographic work. The term       |
|      |                        |           |                         |                                                  |“credits” is often used more specifically to      |
|      |                        |           |                         |                                                  |distinguish between those behind the camera from  |
|      |                        |           |                         |                                                  |“cast,” those in front of the camera. ( context : |
|      |                        |           |                         |                                                  |movie_db_ZIB )                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.1   |identifier              |0-1        |object                   |object of subelement                              |The PID of the work in the Handle System. (       |
|      |                        |           |                         |                                                  |context : MovieArchives)                          |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.1.1 |identifier              |1          |string                   |['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |Handle-String with ASCII prefix in its general    |
|      |                        |           |                         |~])+$']                                           |syntax                                            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.1.2 |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic )                                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.2   |name                    |1          |object                   |object of subelement                              |The personal name consists of the family name and |
|      |                        |           |                         |                                                  |given name, both represented by namestrings.      |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.2.1 |family-name             |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic )                               |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.2.2 |given-name              |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic )                               |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.3   |role                    |1          |string                   |['controlled list']                               |A role assigned to a person (Context:             |
|      |                        |           |                         |                                                  |MovieArchives)                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|5     |genre                   |0-n        |string                   |['controlled list']                               |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type genre: The name of  genre, which    |
|      |                        |           |                         |                                                  |characterise the general style of a               |
|      |                        |           |                         |                                                  |cinematographic work. ( context : movie_db_ZIB )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|6     |identifiers             |0-n        |array                    |array of subelements                              |List of identifiers for movies (Context:          |
|      |                        |           |                         |                                                  |MovieArchives)                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|6.1   |identifier              |1          |string                   |['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |Handle-String with ASCII prefix in its general    |
|      |                        |           |                         |~])+$']                                           |syntax                                            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|6.2   |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic )                                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|7     |lastModified            |1          |string                   |['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |Date and time of last update to metadata record. (|
|      |                        |           |                         |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |context : movie_db_ZIB )                          |
|      |                        |           |                         |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|                                                  |
|      |                        |           |                         |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |                                                  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|8     |originalDuration        |0-1        |string                   |['^PT[0-9]*H[0-9]*M[0-9]*\\.[0-9][0-9][0-9]S$']   |The running time of the first known manifestation |
|      |                        |           |                         |                                                  |of a cinematographic work, measured in minutes and|
|      |                        |           |                         |                                                  |seconds. (Context: MovieArchives)                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9     |originalFormat          |0-1        |object                   |object of subelement                              |The description of the physical artefact on which |
|      |                        |           |                         |                                                  |the first known manifestation of a cinematographic|
|      |                        |           |                         |                                                  |work was fixed.                                   |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.1   |audioMaterialFormat     |0-1        |string                   |['controlled list']                               |Context: MovieArchives                            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.2   |audioMaterialType       |0-1        |string                   |['controlled list']                               |Context: MovieArchives                            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.3   |videoMaterialFormat     |0-1        |string                   |['controlled list']                               |Context: MovieArchives                            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.4   |videoMaterialType       |0-1        |string                   |['controlled list']                               |Context: MovieArchives                            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|10    |originalLanguage        |0-n        |string                   |['^([A-Z][A-Z][A-Z]|[a-z][a-z][a-z]){1}$']        |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type original_language: The language or  |
|      |                        |           |                         |                                                  |languages of the spoken, sung or written content  |
|      |                        |           |                         |                                                  |of the first known manifestation of a             |
|      |                        |           |                         |                                                  |cinematographic work. ( context : movie_db_ZIB )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|11    |originalLength          |0-n        |array of [string, string]|[['^[0-9]*\\.[0-9][0-9]$'], ['controlled list']]  |The total physical length of the first known      |
|      |                        |           |                         |                                                  |manifestation of a cinematographic work, measured |
|      |                        |           |                         |                                                  |in feet or metres.                                |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|12    |productionCompany       |0-n        |array                    |array of subelements                              |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type production_company: The name of an  |
|      |                        |           |                         |                                                  |organisation or company under whose financial,    |
|      |                        |           |                         |                                                  |technical and organisational management a         |
|      |                        |           |                         |                                                  |cinematographic work is made. ( context :         |
|      |                        |           |                         |                                                  |movie_db_ZIB )                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|12.1  |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic )                                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|12.2  |name                    |1          |string                   |['(.)*']                                          |string consisting of unicode characters except    |
|      |                        |           |                         |                                                  |newline.                                          |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|13    |relatedIdentifier       |0-1        |object                   |object of subelement                              |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type related_identifier: Other unique    |
|      |                        |           |                         |                                                  |identifiers like EIDR, ISAN, … ( context :        |
|      |                        |           |                         |                                                  |movie_db_ZIB )                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|13.1  |relatedIdentifierType   |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic )                                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|13.2  |relatedIdentifierValue  |1          |string                   |['(.)*']                                          |string consisting of unicode characters except    |
|      |                        |           |                         |                                                  |newline.                                          |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|14    |schemaVersion           |0-1        |string                   |['controlled list']                               |Version for a WORK (Context: MovieArchives)       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15    |series                  |0-1        |object                   |object of subelement                              |A series is a group of separate items related to  |
|      |                        |           |                         |                                                  |one another by the fact that each item bears, in  |
|      |                        |           |                         |                                                  |addition to its own title, a collective title     |
|      |                        |           |                         |                                                  |applying to the group as a whole. A serial is a   |
|      |                        |           |                         |                                                  |type of “short subject” work which is             |
|      |                        |           |                         |                                                  |characterized principally by the episodic         |
|      |                        |           |                         |                                                  |development of a story. ( context : MovieArchives |
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.1  |identifier              |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic )                                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.2  |title                   |0-1        |object                   |object of subelement                              |A word, phrase, character, or group of characters,|
|      |                        |           |                         |                                                  |normally appearing in an item, naming the item or |
|      |                        |           |                         |                                                  |the work contained in it. (Context: MovieArchives,|
|      |                        |           |                         |                                                  |AV-EFI)                                           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.2.1|titleType               |1          |string                   |['controlled list']                               |The type of a title. Controlled List Values:      |
|      |                        |           |                         |                                                  |[Original Title, Release Title, Archive Title,    |
|      |                        |           |                         |                                                  |Alternative Title, Sort Title]. (context :        |
|      |                        |           |                         |                                                  |MovieArchives)                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.2.2|titleValue              |1          |string                   |['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |                         |                                                  |: generic )                                       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16    |source                  |1-n        |array                    |array of subelements                              |The name of the archive or other organisation     |
|      |                        |           |                         |                                                  |supplying the record. (context: MovieArchives)    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.1  |sourceAttribution       |0-1        |object                   |object of subelement                              |(Context: MovieArchives)                          |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.1.1|attributionDate         |0-1        |string                   |['^(\\d{4})-(\\d{2})-                             |(Context: MovieArchives)                          |
|      |                        |           |                         |(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2}(?:\\.\\d*)?)((-|                                                  |
|      |                        |           |                         |(\\d{2}):(\\d{2})|Z)?)$']                         |                                                  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.1.2|attributionType         |0-1        |string                   |['controlled list']                               |(Context: MovieArchives)                          |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.2  |sourceDate              |0-1        |string                   |['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |combined date and time representations as string. |
|      |                        |           |                         |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |It refers to RFC3339 and ISO 8601 and allows to   |
|      |                        |           |                         |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|give just date, week or ordinal date notation and |
|      |                        |           |                         |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |combined date and time in UTC. Defined by regular |
|      |                        |           |                         |                                                  |expression.                                       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.3  |sourceIdentifier        |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic )                                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.4  |sourceName              |1          |string                   |['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |                         |                                                  |: generic )                                       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|17    |subject                 |0-n        |string                   |['controlled list']                               |subjects that describe the content of the Work    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|18    |title                   |1-n        |array                    |array of subelements                              |A word, phrase, character, or group of characters,|
|      |                        |           |                         |                                                  |normally appearing in an item, naming the item or |
|      |                        |           |                         |                                                  |the work contained in it. (Context: MovieArchives,|
|      |                        |           |                         |                                                  |AV-EFI)                                           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|18.1  |titleType               |1          |string                   |['controlled list']                               |The type of a title. Controlled List Values:      |
|      |                        |           |                         |                                                  |[Original Title, Release Title, Archive Title,    |
|      |                        |           |                         |                                                  |Alternative Title, Sort Title]. (context :        |
|      |                        |           |                         |                                                  |MovieArchives)                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|18.2  |titleValue              |1          |string                   |['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |                         |                                                  |: generic )                                       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|19    |yearOfReference         |0-n        |array                    |array of subelements                              |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type year_of_reference: A date           |
|      |                        |           |                         |                                                  |asssociated with an event in the life cycle of the|
|      |                        |           |                         |                                                  |cinematographic work, typically associated with   |
|      |                        |           |                         |                                                  |its creation, availability or registration (for   |
|      |                        |           |                         |                                                  |example for copyright purposes). ( context :      |
|      |                        |           |                         |                                                  |movie_db_ZIB )                                    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|19.1  |yearOfReferenceEnd      |0-1        |string                   |['^([0-9]{4})$']                                  |The year when the data was or will be made        |
|      |                        |           |                         |                                                  |publicly available. Remark: If an embargo period  |
|      |                        |           |                         |                                                  |has been in effect, use the date when the embargo |
|      |                        |           |                         |                                                  |period ends. In the case of datasets, "publish" is|
|      |                        |           |                         |                                                  |understood to mean making the data available on a |
|      |                        |           |                         |                                                  |specific date to the community of researchers. If |
|      |                        |           |                         |                                                  |there is no standard publication year value, use  |
|      |                        |           |                         |                                                  |the date that would be preferred from a citation  |
|      |                        |           |                         |                                                  |perspective. (context : DataCite)                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|19.2  |yearOfReferenceStart    |1          |string                   |['^([0-9]{4})$']                                  |The year when the data was or will be made        |
|      |                        |           |                         |                                                  |publicly available. Remark: If an embargo period  |
|      |                        |           |                         |                                                  |has been in effect, use the date when the embargo |
|      |                        |           |                         |                                                  |period ends. In the case of datasets, "publish" is|
|      |                        |           |                         |                                                  |understood to mean making the data available on a |
|      |                        |           |                         |                                                  |specific date to the community of researchers. If |
|      |                        |           |                         |                                                  |there is no standard publication year value, use  |
|      |                        |           |                         |                                                  |the date that would be preferred from a citation  |
|      |                        |           |                         |                                                  |perspective. (context : DataCite)                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|19.3  |yearOfReferenceType     |1          |string                   |['controlled list']                               |Type of reference (Context: MovieArchives)        |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
