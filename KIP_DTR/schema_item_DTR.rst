+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|Id    |Name                     |Cardinality|Type  |Constraints                                       |Definition                                        |
+======+=========================+===========+======+==================================================+==================================================+
|1     |KernelInformationProfile |0-1        |string|['^([\\x00-\\x2D,\\x30-\\x3F,\\x41-               |Handle-String in its general syntax. Problem here:|
|      |                         |           |      |\\xFF])+(\\.([\\x00-\\x2D,\\x30-\\x3F,\\x41-      |Schema validation does not work properly, because |
|      |                         |           |      |\\xFF])+)*\\/([\\x00-\\xFF])+$']                  |implementations for ecma-262-RegExp do not seem to|
|      |                         |           |      |                                                  |correctly parse hex coded regular expressions     |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2     |identifier               |0-1        |object|object of subelement                              |The PID of the work in the Handle System. (       |
|      |                         |           |      |                                                  |context : MovieArchives)                          |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2.1   |identifier               |1          |string|['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |Handle-String with ASCII prefix in its general    |
|      |                         |           |      |~])+$']                                           |syntax                                            |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2.2   |identifier_uri           |0-1        |string|['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                         |           |      |]*))?(#(.*))?']                                   |generic )                                         |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|3     |is_data_object_of        |1          |string|['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |The PID of the publication event, this dataObject |
|      |                         |           |      |~])+$']                                           |is part of. ( context : movie_db_ZIB )            |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|4     |item_file_size           |0-1        |string|['^[. 0-9]+(KB|MB|GB|TB|PB|B)$']                  |same as filesize 21.T11148/cc0c1fc9a56fc2f54723   |
|      |                         |           |      |                                                  |but allowing for delimiter                        |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|5     |language_versions        |0-n        |string|['controlled list']                               |implicitly created because of multiple occurence  |
|      |                         |           |      |                                                  |of child type 'language_version': Language version|
|      |                         |           |      |                                                  |of the video. ( context : movie_db_ZIB )          |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|6     |last_modified            |1          |string|['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |Date and time of last update to metadata record. (|
|      |                         |           |      |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |context : movie_db_ZIB )                          |
|      |                         |           |      |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|                                                  |
|      |                         |           |      |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |                                                  |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|7     |physical_descriptions    |0-n        |string|['controlled list']                               |implicitly created because of multiple occurence  |
|      |                         |           |      |                                                  |of child type 'physical_description': The broad   |
|      |                         |           |      |                                                  |media type of the Item (e.g., film, video, audio, |
|      |                         |           |      |                                                  |optical, digital file). Recording this high-level |
|      |                         |           |      |                                                  |information will enable simple searching for only |
|      |                         |           |      |                                                  |film, video, digital, etc. elements rather than   |
|      |                         |           |      |                                                  |searching by all possible formats and carriers. ( |
|      |                         |           |      |                                                  |context : movie_db_ZIB )                          |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|9     |same_as                  |0-n        |string|['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |This dataObject may come from a joint digitization|
|      |                         |           |      |~])+$']                                           |effort of more than one institution. After the    |
|      |                         |           |      |                                                  |digitization it is common practice to supply all  |
|      |                         |           |      |                                                  |the participating institutions with the digital   |
|      |                         |           |      |                                                  |Objects, so there may be other dataObjects        |
|      |                         |           |      |                                                  |identical to this one. ( context : movie_db_ZIB ) |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10    |source                   |1          |object|object of subelement                              |The name of the archive or other organisation     |
|      |                         |           |      |                                                  |supplying the record. ( context : movie_db_ZIB )  |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.1  |sourceAttribution        |0-1        |object|object of subelement                              |(Context: MovieArchives)                          |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.1.1|attributionDate          |0-1        |string|['^(\\d{4})-(\\d{2})-                             |(Context: MovieArchives)                          |
|      |                         |           |      |(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2}(?:\\.\\d*)?)((-|                                                  |
|      |                         |           |      |(\\d{2}):(\\d{2})|Z)?)$']                         |                                                  |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.1.2|attributionType          |0-1        |string|['controlled list']                               |(Context: MovieArchives)                          |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.2  |sourceDate               |0-1        |string|['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |combined date and time representations as string. |
|      |                         |           |      |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |It refers to RFC3339 and ISO 8601 and allows to   |
|      |                         |           |      |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|give just date, week or ordinal date notation and |
|      |                         |           |      |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |combined date and time in UTC. Defined by regular |
|      |                         |           |      |                                                  |expression.                                       |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.3  |sourceIdentifier         |0-1        |string|['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                         |           |      |]*))?(#(.*))?']                                   |generic )                                         |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.4  |sourceName               |1          |string|['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                         |           |      |                                                  |: generic )                                       |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12    |supplementary_information|0-1        |string|['(.|\n)*']                                       |Additional information specific to the Item (     |
|      |                         |           |      |                                                  |context : movie_db_ZIB )                          |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|13    |title                    |0-1        |string|['(.)*']                                          |string consisting of unicode characters except    |
|      |                         |           |      |                                                  |newline.                                          |
+------+-------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
