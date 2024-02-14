+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|Id    |Name                    |Cardinality|Type  |Constraints                                       |Definition                                        |
+======+========================+===========+======+==================================================+==================================================+
|1     |KernelInformationProfile|0-1        |string|['^([\\x00-\\x2D,\\x30-\\x3F,\\x41-               |Handle-String in its general syntax. Problem here:|
|      |                        |           |      |\\xFF])+(\\.([\\x00-\\x2D,\\x30-\\x3F,\\x41-      |Schema validation does not work properly, because |
|      |                        |           |      |\\xFF])+)*\\/([\\x00-\\xFF])+$']                  |implementations for ecma-262-RegExp do not seem to|
|      |                        |           |      |                                                  |correctly parse hex coded regular expressions  (  |
|      |                        |           |      |                                                  |ref: Handle-Identifier-                           |
|      |                        |           |      |                                                  |General@21.T11148/3b8833cd7e19f60571a6 )          |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2     |has_agent               |0-n        |array |array of subelements                              |An entity that is involved in the creation,       |
|      |                        |           |      |                                                  |realization, curation or exploitation of a        |
|      |                        |           |      |                                                  |Manifestation (Corporate Body) ( context :        |
|      |                        |           |      |                                                  |movie_db_ZIB ) ( ref:                             |
|      |                        |           |      |                                                  |hasAgent@21.T11148/5a69721cca16545c03e6 )         |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2.1   |identifier_uri          |0-1        |string|['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |      |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |      |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2.2   |name                    |1          |string|['(.)*']                                          |string consisting of unicode characters except    |
|      |                        |           |      |                                                  |newline. ( ref: unicode-line-                     |
|      |                        |           |      |                                                  |string@21.T11148/f1627ce85386d8d75078 )           |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|3     |has_data_objects        |1-n        |string|['^21(\\.([0-9,A-Z,a-z])+)*\\/([!-~])+$']         |Reference to a work using ePIC PID (context:      |
|      |                        |           |      |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |      |                                                  |is_version_of@21.T11148/ef19de26cec8cae78ceb )    |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|4     |identifier              |0-1        |string|['^21(\\.([0-9,A-Z,a-z])+)*\\/([!-~])+$']         |Handle-String in its ePIC ASCII numbering syntax (|
|      |                        |           |      |                                                  |ref: Handle-Identifier-ePIC-                      |
|      |                        |           |      |                                                  |ASCII@21.T11148/b731866dc9a1daee5300 )            |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|5     |is_version_of           |1-n        |string|['^21(\\.([0-9,A-Z,a-z])+)*\\/([!-~])+$']         |Reference to a work using ePIC PID (context:      |
|      |                        |           |      |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |      |                                                  |is_version_of@21.T11148/ef19de26cec8cae78ceb )    |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|6     |last_modified           |1          |string|['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |Date and time of last update to metadata record. (|
|      |                        |           |      |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |context : movie_db_ZIB ) ( ref:                   |
|      |                        |           |      |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|last_modified@21.T11148/a27923f25913583b1ea6 )    |
|      |                        |           |      |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |                                                  |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|7     |manifestation_types     |0-n        |string|['controlled list']                               |implicitly created because of multiple occurence  |
|      |                        |           |      |                                                  |of child type ‘manifestationType’: A word or      |
|      |                        |           |      |                                                  |phrase denoting the relationship between the      |
|      |                        |           |      |                                                  |manifestation and the variant or cinematographic  |
|      |                        |           |      |                                                  |work that it manifests. May be omitted if no other|
|      |                        |           |      |                                                  |manifestation is known. ( context : movie_db_ZIB )|
|      |                        |           |      |                                                  |( ref:                                            |
|      |                        |           |      |                                                  |manifestationTypes@21.T11148/c72633267da87f952971 |
|      |                        |           |      |                                                  |)                                                 |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|8     |production_year         |0-1        |string|['^([0-9]{4})$']                                  |Production year or timespan ( context :           |
|      |                        |           |      |                                                  |movie_db_ZIB ) ( ref:                             |
|      |                        |           |      |                                                  |productionYear@21.T11148/62e2596615d0c4f189df )   |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|9     |release_date            |0-1        |string|['^([0-9]{4})-([0]?[1-9]|1[0-2])-([0-2][0-9]|3[0- |Publication Date ( context : movie_db_ZIB ) ( ref:|
|      |                        |           |      |1])$']                                            |publication_event@21.T11148/f9b4cc48754481b07f75 )|
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10    |same_as                 |0-n        |string|['^21(\\.([0-9,A-Z,a-z])+)*\\/([!-~])+$']         |Reference to a work using ePIC PID (context:      |
|      |                        |           |      |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |      |                                                  |is_version_of@21.T11148/ef19de26cec8cae78ceb )    |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|11    |schema_version          |0-1        |string|['controlled list']                               |Version for a WORK (Context: MovieArchives) ( ref:|
|      |                        |           |      |                                                  |SchemaVersion@21.T11148/0ed7199092d107853421 )    |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12    |source                  |1          |object|object of subelement                              |The name of the archive or other organisation     |
|      |                        |           |      |                                                  |supplying the record. ( context : movie_db_ZIB ) (|
|      |                        |           |      |                                                  |ref: source@21.T11148/828d338a9b04221c9cbe )      |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12.1  |sourceAttribution       |0-1        |object|object of subelement                              |(Context: MovieArchives) ( ref:                   |
|      |                        |           |      |                                                  |sourceAttribution@21.T11148/3dc898fc1da407321cbf )|
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12.1.1|attributionDate         |0-1        |string|['^(\\d{4})-(\\d{2})-                             |(Context: MovieArchives) ( ref:                   |
|      |                        |           |      |(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2}(?:\\.\\d*)?)((-|attributionDate@21.T11148/7d22fb807cbbbeaa376c )  |
|      |                        |           |      |(\\d{2}):(\\d{2})|Z)?)$']                         |                                                  |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12.1.2|attributionType         |0-1        |string|['controlled list']                               |(Context: MovieArchives) ( ref:                   |
|      |                        |           |      |                                                  |attributionType@21.T11148/62304704da8a6510e9e4 )  |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12.2  |sourceDate              |0-1        |string|['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |combined date and time representations as string. |
|      |                        |           |      |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |It refers to RFC3339 and ISO 8601 and allows to   |
|      |                        |           |      |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|give just date, week or ordinal date notation and |
|      |                        |           |      |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |combined date and time in UTC. Defined by regular |
|      |                        |           |      |                                                  |expression. ( ref: date-time-                     |
|      |                        |           |      |                                                  |weak@21.T11148/9ca79b6ce26f3fd4fad3 )             |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12.3  |sourceIdentifier        |0-1        |string|['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                        |           |      |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                        |           |      |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12.4  |sourceName              |1          |string|['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |      |                                                  |: generic ) ( ref: unicode-                       |
|      |                        |           |      |                                                  |string@21.T11148/798588c5a1ec532f737b )           |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|13    |titles                  |0-n        |array |array of subelements                              |A word, phrase, character, or group of characters,|
|      |                        |           |      |                                                  |normally appearing in an item, naming the item or |
|      |                        |           |      |                                                  |the work contained in it. (Context: MovieArchives,|
|      |                        |           |      |                                                  |AV-EFI) ( ref:                                    |
|      |                        |           |      |                                                  |titles@21.T11148/50c9e3dd19460ed72a07 )           |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|13.1  |titleType               |1          |string|['controlled list']                               |The type of a title. Controlled List Values:      |
|      |                        |           |      |                                                  |[Original Title, Release Title, Archive Title,    |
|      |                        |           |      |                                                  |Alternative Title, Sort Title]. (context :        |
|      |                        |           |      |                                                  |MovieArchives) ( ref:                             |
|      |                        |           |      |                                                  |titleType@21.T11148/2f4e516fbdfa40a52453 )        |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|13.2  |titleValue              |1          |string|['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                        |           |      |                                                  |: generic ) ( ref: unicode-                       |
|      |                        |           |      |                                                  |string@21.T11148/798588c5a1ec532f737b )           |
+------+------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
