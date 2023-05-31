+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|Id    |Name                    |Cardinality|Type                     |Constrains                                        |Definition                                        |
+======+========================+===========+=========================+==================================================+==================================================+
|1     |KernelInformationProfile|0-1        |string                   |['^([\\x00-\\x2D,\\x30-\\x3F,\\x41-\\xFF])+(\\.([\|Handle-String in its general syntax. Problem here:|
|      |                        |           |                         |\x00-\\x2D,\\x30-\\x3F,\\x41-\\xFF])+)*\\/([\\x00-|Schema validation does not work properly, because |
|      |                        |           |                         |\\xFF])+$']                                       |implementations for ecma-262-RegExp do not seem to|
|      |                        |           |                         |                                                  |correctly parse hex coded regular expressions  (  |
|      |                        |           |                         |                                                  |ref: Handle-Identifier-                           |
|      |                        |           |                         |                                                  |General@21.T11148/3b8833cd7e19f60571a6 )          |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2     |cast                    |0-n        |array                    |array of subelements                              |List of actors (cast) (Context: MovieArchives) (  |
|      |                        |           |                         |                                                  |ref: cast@21.T11148/0eac2ad63f3322103b02 )        |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.1   |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |                         |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.2   |name                    |0-1        |object                   |object of subelement                              |The personal name consists of the family name and |
|      |                        |           |                         |                                                  |given name, both represented by namestrings. (    |
|      |                        |           |                         |                                                  |ref: personal-name@21.T11148/b917454226b391110a05 |
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.2.1 |family-name             |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic ) ( ref:                        |
|      |                        |           |                         |                                                  |namestring@21.T11148/ab8d232261b9b60ba559 )       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|2.2.2 |given-name              |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic ) ( ref:                        |
|      |                        |           |                         |                                                  |namestring@21.T11148/ab8d232261b9b60ba559 )       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|3     |countryOfReference      |0-n        |string                   |['/^A[^ABCHJKNPVY]|B[^CKPUX]|C                    |implicitly created because of multiple occurence  |
|      |                        |           |                         |[^BEJPQST]|D[EJKMOZ]|E[CEGHRST]|F[IJKMOR]|G[^CJ   |of child type country_of_reference: The country or|
|      |                        |           |                         |KOVXZ]|H[KMNRTU]|I[DEL-OQ-T]|J[EMOP]|K[EGHIMNPR   |countries where the principal offices of the      |
|      |                        |           |                         |WYZ]|L[ABCIKR-VY]|M[^BIJ]|N[ACEFGILOPRUZ]|OM|P[   |production company (or companies) of a            |
|      |                        |           |                         |AE-HK-NRSTWY]|QA|R[EOSUW]|S[^FPQUW]|T[^ABEIPQSU   |cinematographic work are located. ( context :     |
|      |                        |           |                         |XY]|U[AGMSYZ]|V[ACEGINU]|WF|WS|YE|YT|Z[AMW]$/ix'] |movie_db_ZIB ) ( ref: countries_of_reference@21.T1|
|      |                        |           |                         |                                                  |1148/08183f7e0cfaff8d69ff )                       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4     |credits                 |0-n        |array                    |array of subelements                              |The names and functions of persons responsible for|
|      |                        |           |                         |                                                  |the production and/or artistic or intellectual    |
|      |                        |           |                         |                                                  |content of a cinematographic work. The term       |
|      |                        |           |                         |                                                  |“credits” is often used more specifically to      |
|      |                        |           |                         |                                                  |distinguish between those behind the camera from  |
|      |                        |           |                         |                                                  |“cast,” those in front of the camera. ( context : |
|      |                        |           |                         |                                                  |movie_db_ZIB ) ( ref:                             |
|      |                        |           |                         |                                                  |credits@21.T11148/66c22fad3a990a40eb2b )          |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.1   |identifier              |0-1        |object                   |object of subelement                              |The PID of the work in the Handle System. (       |
|      |                        |           |                         |                                                  |context : MovieArchives) ( ref:                   |
|      |                        |           |                         |                                                  |identifier@21.T11148/fae9fd39301eb7e657d4 )       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.1.1 |identifier              |1          |string                   |['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-~]|Handle-String with ASCII prefix in its general    |
|      |                        |           |                         |)+$']                                             |syntax ( ref: Handle-Identifier-                  |
|      |                        |           |                         |                                                  |ASCII@21.T11148/3626040cadcac1571685 )            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.1.2 |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |                         |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.2   |name                    |1          |object                   |object of subelement                              |The personal name consists of the family name and |
|      |                        |           |                         |                                                  |given name, both represented by namestrings. (    |
|      |                        |           |                         |                                                  |ref: personal-name@21.T11148/b917454226b391110a05 |
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.2.1 |family-name             |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic ) ( ref:                        |
|      |                        |           |                         |                                                  |namestring@21.T11148/ab8d232261b9b60ba559 )       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.2.2 |given-name              |1          |string                   |['^[^;\\,]+$', 'maxLength1024']                   |String used in names, family names or given names.|
|      |                        |           |                         |                                                  |Can contain any unicode character except ',' and  |
|      |                        |           |                         |                                                  |';' to avoid conflicts in listings of names. (    |
|      |                        |           |                         |                                                  |context : generic ) ( ref:                        |
|      |                        |           |                         |                                                  |namestring@21.T11148/ab8d232261b9b60ba559 )       |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|4.3   |role                    |1          |string                   |['controlled list']                               |A role assigned to a person (Context:             |
|      |                        |           |                         |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |                         |                                                  |role@21.T11148/8dca46428d005a2f4c2e )             |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|5     |genre                   |0-n        |string                   |['controlled list']                               |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type genre: The name of  genre, which    |
|      |                        |           |                         |                                                  |characterise the general style of a               |
|      |                        |           |                         |                                                  |cinematographic work. ( context : movie_db_ZIB ) (|
|      |                        |           |                         |                                                  |ref: genres@21.T11148/cee386b04503398bc6ca )      |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|6     |identifiers             |0-n        |array                    |array of subelements                              |List of identifiers for movies (Context:          |
|      |                        |           |                         |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |                         |                                                  |identifiers@21.T11148/55b00519c07d7934f062 )      |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|6.1   |identifier              |1          |string                   |['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-~]|Handle-String with ASCII prefix in its general    |
|      |                        |           |                         |)+$']                                             |syntax ( ref: Handle-Identifier-                  |
|      |                        |           |                         |                                                  |ASCII@21.T11148/3626040cadcac1571685 )            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|6.2   |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |                         |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|7     |lastModified            |1          |string                   |['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-9]||Date and time of last update to metadata record. (|
|      |                        |           |                         |3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-9])(:|context : movie_db_ZIB ) ( ref:                   |
|      |                        |           |                         |)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-9]|2[|last_modified@21.T11148/a27923f25913583b1ea6 )    |
|      |                        |           |                         |0-3])(:)?([0-5][0-9])?))?))?$']                   |                                                  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|8     |originalDuration        |0-1        |string                   |['^PT[0-9]*H[0-9]*M[0-9]*\\.[0-9][0-9][0-9]S$']   |The running time of the first known manifestation |
|      |                        |           |                         |                                                  |of a cinematographic work, measured in minutes and|
|      |                        |           |                         |                                                  |seconds. (Context: MovieArchives) ( ref:          |
|      |                        |           |                         |                                                  |duration@21.T11148/5d3f344b5bd21e9500c6 )         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9     |originalFormat          |0-1        |object                   |object of subelement                              |The description of the physical artefact on which |
|      |                        |           |                         |                                                  |the first known manifestation of a cinematographic|
|      |                        |           |                         |                                                  |work was fixed. ( ref:                            |
|      |                        |           |                         |                                                  |original_format@21.T11148/cda76378eeb3ce51a3ff )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.1   |audioMaterialFormat     |0-1        |string                   |['controlled list']                               |Context: MovieArchives ( ref:                     |
|      |                        |           |                         |                                                  |audioMaterialFormat@21.T11148/42e93d201f7c48d6ee2d|
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.2   |audioMaterialType       |0-1        |string                   |['controlled list']                               |Context: MovieArchives ( ref:                     |
|      |                        |           |                         |                                                  |audioMaterialType@21.T11148/064a9d98276ddd62574a )|
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.3   |videoMaterialFormat     |0-1        |string                   |['controlled list']                               |Context: MovieArchives ( ref:                     |
|      |                        |           |                         |                                                  |videoMaterialFormat@21.T11148/a100714b83c34aaab3ca|
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|9.4   |videoMaterialType       |0-1        |string                   |['controlled list']                               |Context: MovieArchives ( ref:                     |
|      |                        |           |                         |                                                  |videoMaterialType@21.T11148/9b2792ed49f2c062b3aa )|
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|10    |originalLanguage        |0-n        |string                   |['^([A-Z][A-Z][A-Z]|[a-z][a-z][a-z]){1}$']        |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type original_language: The language or  |
|      |                        |           |                         |                                                  |languages of the spoken, sung or written content  |
|      |                        |           |                         |                                                  |of the first known manifestation of a             |
|      |                        |           |                         |                                                  |cinematographic work. ( context : movie_db_ZIB ) (|
|      |                        |           |                         |                                                  |ref:                                              |
|      |                        |           |                         |                                                  |original_languages@21.T11148/577d96232ee6ea2f8dfa |
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|11    |originalLength          |0-n        |array of [string, string]|[['^[0-9]*\\.[0-9][0-9]$'], ['controlled list']]  |The total physical length of the first known      |
|      |                        |           |                         |                                                  |manifestation of a cinematographic work, measured |
|      |                        |           |                         |                                                  |in feet or metres. ( ref:                         |
|      |                        |           |                         |                                                  |original_length@21.T11148/2ffeb8c300db64507734 )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|12    |productionCompany       |0-n        |array                    |array of subelements                              |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type production_company: The name of an  |
|      |                        |           |                         |                                                  |organisation or company under whose financial,    |
|      |                        |           |                         |                                                  |technical and organisational management a         |
|      |                        |           |                         |                                                  |cinematographic work is made. ( context :         |
|      |                        |           |                         |                                                  |movie_db_ZIB ) ( ref: production_companies@21.T111|
|      |                        |           |                         |                                                  |48/cc9350e8525a1ca5ffe4 )                         |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|12.1  |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |                         |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|12.2  |name                    |1          |string                   |['(.)*']                                          |string consisting of unicode characters except    |
|      |                        |           |                         |                                                  |newline. ( ref: unicode-line-                     |
|      |                        |           |                         |                                                  |string@21.T11148/f1627ce85386d8d75078 )           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|13    |relatedIdentifier       |0-1        |object                   |object of subelement                              |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type related_identifier: Other unique    |
|      |                        |           |                         |                                                  |identifiers like EIDR, ISAN, … ( context :        |
|      |                        |           |                         |                                                  |movie_db_ZIB ) ( ref:                             |
|      |                        |           |                         |                                                  |related_identifiers@21.T11148/d72482f16d18ff46f8f4|
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|13.1  |relatedIdentifierType   |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |                         |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|13.2  |relatedIdentifierValue  |1          |string                   |['(.)*']                                          |string consisting of unicode characters except    |
|      |                        |           |                         |                                                  |newline. ( ref: unicode-line-                     |
|      |                        |           |                         |                                                  |string@21.T11148/f1627ce85386d8d75078 )           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|14    |schema_version          |0-1        |string                   |['controlled list']                               |Version for a WORK (Context: MovieArchives) ( ref:|
|      |                        |           |                         |                                                  |SchemaVersion@21.T11148/0ed7199092d107853421 )    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15    |series                  |0-1        |object                   |object of subelement                              |A series is a group of separate items related to  |
|      |                        |           |                         |                                                  |one another by the fact that each item bears, in  |
|      |                        |           |                         |                                                  |addition to its own title, a collective title     |
|      |                        |           |                         |                                                  |applying to the group as a whole. A serial is a   |
|      |                        |           |                         |                                                  |type of “short subject” work which is             |
|      |                        |           |                         |                                                  |characterized principally by the episodic         |
|      |                        |           |                         |                                                  |development of a story. ( context : MovieArchives |
|      |                        |           |                         |                                                  |) ( ref: series@21.T11148/8c45d090913a21d5cac1 )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.1  |identifier              |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |                         |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.2  |title                   |0-1        |object                   |object of subelement                              |A word, phrase, character, or group of characters,|
|      |                        |           |                         |                                                  |normally appearing in an item, naming the item or |
|      |                        |           |                         |                                                  |the work contained in it. (Context: MovieArchives,|
|      |                        |           |                         |                                                  |AV-EFI)  ( ref:                                   |
|      |                        |           |                         |                                                  |title@21.T11148/3c6de1b7dd91465d437e )            |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.2.1|titleType               |1          |string                   |['controlled list']                               |The type of a title. Controlled List Values:      |
|      |                        |           |                         |                                                  |[Original Title, Release Title, Archive Title,    |
|      |                        |           |                         |                                                  |Alternative Title, Sort Title]. (context :        |
|      |                        |           |                         |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |                         |                                                  |titleType@21.T11148/2f4e516fbdfa40a52453 )        |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|15.2.2|titleValue              |1          |string                   |['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |                         |                                                  |: generic ) ( ref: unicode-                       |
|      |                        |           |                         |                                                  |string@21.T11148/798588c5a1ec532f737b )           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16    |source                  |1-n        |array                    |array of subelements                              |The name of the archive or other organisation     |
|      |                        |           |                         |                                                  |supplying the record. (context: MovieArchives) (  |
|      |                        |           |                         |                                                  |ref: sources@21.T11148/bce16dd0260827ecf338 )     |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.1  |date                    |0-1        |string                   |['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-9]||combined date and time representations as string. |
|      |                        |           |                         |3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-9])(:|It refers to RFC3339 and ISO 8601 and allows to   |
|      |                        |           |                         |)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-9]|2[|give just date, week or ordinal date notation and |
|      |                        |           |                         |0-3])(:)?([0-5][0-9])?))?))?$']                   |combined date and time in UTC. Defined by regular |
|      |                        |           |                         |                                                  |expression. ( ref: date-time-                     |
|      |                        |           |                         |                                                  |weak@21.T11148/9ca79b6ce26f3fd4fad3 )             |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.2  |identifier_uri          |0-1        |string                   |['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |                         |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |                         |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.3  |name                    |1          |string                   |['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |                         |                                                  |: generic ) ( ref: unicode-                       |
|      |                        |           |                         |                                                  |string@21.T11148/798588c5a1ec532f737b )           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.4  |sourceAttribution       |0-1        |object                   |object of subelement                              |(Context: MovieArchives) ( ref:                   |
|      |                        |           |                         |                                                  |sourceAttribution@21.T11148/3dc898fc1da407321cbf )|
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.4.1|attributionDate         |0-1        |string                   |['^(\\d{4})-(\\d{2})-(\\d{2})T(\\d{2}):(\\d{2}):(\|(Context: MovieArchives) ( ref:                   |
|      |                        |           |                         |\d{2}(?:\\.\\d*)?)((-(\\d{2}):(\\d{2})|Z)?)$']    |attributionDate@21.T11148/7d22fb807cbbbeaa376c )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|16.4.2|attributionType         |0-1        |string                   |['controlled list']                               |(Context: MovieArchives) ( ref:                   |
|      |                        |           |                         |                                                  |attributionType@21.T11148/62304704da8a6510e9e4 )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|17    |title                   |1-n        |array                    |array of subelements                              |A word, phrase, character, or group of characters,|
|      |                        |           |                         |                                                  |normally appearing in an item, naming the item or |
|      |                        |           |                         |                                                  |the work contained in it. (Context: MovieArchives,|
|      |                        |           |                         |                                                  |AV-EFI) ( ref:                                    |
|      |                        |           |                         |                                                  |titles@21.T11148/50c9e3dd19460ed72a07 )           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|17.1  |titleType               |1          |string                   |['controlled list']                               |The type of a title. Controlled List Values:      |
|      |                        |           |                         |                                                  |[Original Title, Release Title, Archive Title,    |
|      |                        |           |                         |                                                  |Alternative Title, Sort Title]. (context :        |
|      |                        |           |                         |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |                         |                                                  |titleType@21.T11148/2f4e516fbdfa40a52453 )        |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|17.2  |titleValue              |1          |string                   |['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |                         |                                                  |: generic ) ( ref: unicode-                       |
|      |                        |           |                         |                                                  |string@21.T11148/798588c5a1ec532f737b )           |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|18    |yearsOfReference        |0-n        |array                    |array of subelements                              |implicitly created because of multiple occurence  |
|      |                        |           |                         |                                                  |of child type year_of_reference: A date           |
|      |                        |           |                         |                                                  |asssociated with an event in the life cycle of the|
|      |                        |           |                         |                                                  |cinematographic work, typically associated with   |
|      |                        |           |                         |                                                  |its creation, availability or registration (for   |
|      |                        |           |                         |                                                  |example for copyright purposes). ( context :      |
|      |                        |           |                         |                                                  |movie_db_ZIB ) ( ref:                             |
|      |                        |           |                         |                                                  |years_of_reference@21.T11148/089d6db63cf69c35930d |
|      |                        |           |                         |                                                  |)                                                 |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|18.1  |endYear                 |0-1        |string                   |['^([0-9]{4})$']                                  |The year when the data was or will be made        |
|      |                        |           |                         |                                                  |publicly available. Remark: If an embargo period  |
|      |                        |           |                         |                                                  |has been in effect, use the date when the embargo |
|      |                        |           |                         |                                                  |period ends. In the case of datasets, "publish" is|
|      |                        |           |                         |                                                  |understood to mean making the data available on a |
|      |                        |           |                         |                                                  |specific date to the community of researchers. If |
|      |                        |           |                         |                                                  |there is no standard publication year value, use  |
|      |                        |           |                         |                                                  |the date that would be preferred from a citation  |
|      |                        |           |                         |                                                  |perspective. (context : DataCite) ( ref:          |
|      |                        |           |                         |                                                  |publicationYear@21.T11148/d080610ed8382c3c2ae4 )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|18.2  |referenceType           |1          |string                   |['controlled list']                               |Type of reference (Context: MovieArchives) ( ref: |
|      |                        |           |                         |                                                  |referenceType@21.T11148/03dfc92c55cea3e18920 )    |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
|18.3  |startYear               |1          |string                   |['^([0-9]{4})$']                                  |The year when the data was or will be made        |
|      |                        |           |                         |                                                  |publicly available. Remark: If an embargo period  |
|      |                        |           |                         |                                                  |has been in effect, use the date when the embargo |
|      |                        |           |                         |                                                  |period ends. In the case of datasets, "publish" is|
|      |                        |           |                         |                                                  |understood to mean making the data available on a |
|      |                        |           |                         |                                                  |specific date to the community of researchers. If |
|      |                        |           |                         |                                                  |there is no standard publication year value, use  |
|      |                        |           |                         |                                                  |the date that would be preferred from a citation  |
|      |                        |           |                         |                                                  |perspective. (context : DataCite) ( ref:          |
|      |                        |           |                         |                                                  |publicationYear@21.T11148/d080610ed8382c3c2ae4 )  |
+------+------------------------+-----------+-------------------------+--------------------------------------------------+--------------------------------------------------+
