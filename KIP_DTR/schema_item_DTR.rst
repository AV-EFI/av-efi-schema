+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|Id    |Name                      |Cardinality|Type  |Constraints                                       |Definition                                        |
+======+==========================+===========+======+==================================================+==================================================+
|1     |KernelInformationProfile  |0-1        |string|['^([\\x00-\\x2D,\\x30-\\x3F,\\x41-               |Handle-String in its general syntax. Problem here:|
|      |                          |           |      |\\xFF])+(\\.([\\x00-\\x2D,\\x30-\\x3F,\\x41-      |Schema validation does not work properly, because |
|      |                          |           |      |\\xFF])+)*\\/([\\x00-\\xFF])+$']                  |implementations for ecma-262-RegExp do not seem to|
|      |                          |           |      |                                                  |correctly parse hex coded regular expressions  (  |
|      |                          |           |      |                                                  |ref: Handle-Identifier-                           |
|      |                          |           |      |                                                  |General@21.T11148/3b8833cd7e19f60571a6 )          |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2     |identifier                |0-1        |object|object of subelement                              |The PID of the work in the Handle System. (       |
|      |                          |           |      |                                                  |context : MovieArchives) ( ref:                   |
|      |                          |           |      |                                                  |identifier@21.T11148/fae9fd39301eb7e657d4 )       |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2.1   |identifier                |1          |string|['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |Handle-String with ASCII prefix in its general    |
|      |                          |           |      |~])+$']                                           |syntax ( ref: Handle-Identifier-                  |
|      |                          |           |      |                                                  |ASCII@21.T11148/3626040cadcac1571685 )            |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|2.2   |identifier_uri            |0-1        |string|['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                          |           |      |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                          |           |      |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|3     |is_data_object_of         |1          |string|['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |The PID of the publication event, this dataObject |
|      |                          |           |      |~])+$']                                           |is part of. ( context : movie_db_ZIB ) ( ref:     |
|      |                          |           |      |                                                  |is_data_object_of@21.T11148/419ba04a05d800a903a0 )|
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|4     |item_file_size            |0-1        |string|['^[. 0-9]+(KB|MB|GB|TB|PB|B)$']                  |same as filesize 21.T11148/cc0c1fc9a56fc2f54723   |
|      |                          |           |      |                                                  |but allowing for delimiter  ( ref: filesize_with_d|
|      |                          |           |      |                                                  |elimiter@21.T11148/61dec38771a5e5bf44cf )         |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|5     |language_versions         |0-n        |string|['controlled list']                               |implicitly created because of multiple occurence  |
|      |                          |           |      |                                                  |of child type 'language_version': Language version|
|      |                          |           |      |                                                  |of the video. ( context : movie_db_ZIB ) ( ref:   |
|      |                          |           |      |                                                  |language_versions@21.T11148/7865a17891323845369f )|
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|6     |last_modified             |1          |string|['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |Date and time of last update to metadata record. (|
|      |                          |           |      |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |context : movie_db_ZIB ) ( ref:                   |
|      |                          |           |      |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|last_modified@21.T11148/a27923f25913583b1ea6 )    |
|      |                          |           |      |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |                                                  |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|7     |physical_descriptions     |0-n        |string|['controlled list']                               |implicitly created because of multiple occurence  |
|      |                          |           |      |                                                  |of child type 'physical_description': The broad   |
|      |                          |           |      |                                                  |media type of the Item (e.g., film, video, audio, |
|      |                          |           |      |                                                  |optical, digital file). Recording this high-level |
|      |                          |           |      |                                                  |information will enable simple searching for only |
|      |                          |           |      |                                                  |film, video, digital, etc. elements rather than   |
|      |                          |           |      |                                                  |searching by all possible formats and carriers. ( |
|      |                          |           |      |                                                  |context : movie_db_ZIB ) ( ref: physical_descripti|
|      |                          |           |      |                                                  |ons@21.T11148/d130a04670f3825a123b )              |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|8     |preservation_access_status|0-1        |string|['controlled list']                               |Description of the preservation or access status  |
|      |                          |           |      |                                                  |of the dataObject, for example Master, Viewing,   |
|      |                          |           |      |                                                  |etc. Select term from a controlled list. (Context:|
|      |                          |           |      |                                                  |AV-EFI) ( ref: preservation_access_status@21.T1114|
|      |                          |           |      |                                                  |8/ec53e13cba99d01e6ff2 )                          |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|9     |same_as                   |0-n        |string|['^([0-9,A-Z,a-z])+(\\.([0-9,A-Z,a-z])+)*\\/([!-  |This dataObject may come from a joint digitization|
|      |                          |           |      |~])+$']                                           |effort of more than one institution. After the    |
|      |                          |           |      |                                                  |digitization it is common practice to supply all  |
|      |                          |           |      |                                                  |the participating institutions with the digital   |
|      |                          |           |      |                                                  |Objects, so there may be other dataObjects        |
|      |                          |           |      |                                                  |identical to this one. ( context : movie_db_ZIB ) |
|      |                          |           |      |                                                  |( ref: same_as@21.T11148/d95bff728d4dd304ae86 )   |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10    |source                    |1          |object|object of subelement                              |The name of the archive or other organisation     |
|      |                          |           |      |                                                  |supplying the record. ( context : movie_db_ZIB ) (|
|      |                          |           |      |                                                  |ref: source@21.T11148/828d338a9b04221c9cbe )      |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.1  |sourceAttribution         |0-1        |object|object of subelement                              |(Context: MovieArchives) ( ref:                   |
|      |                          |           |      |                                                  |sourceAttribution@21.T11148/3dc898fc1da407321cbf )|
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.1.1|attributionDate           |0-1        |string|['^(\\d{4})-(\\d{2})-                             |(Context: MovieArchives) ( ref:                   |
|      |                          |           |      |(\\d{2})T(\\d{2}):(\\d{2}):(\\d{2}(?:\\.\\d*)?)((-|attributionDate@21.T11148/7d22fb807cbbbeaa376c )  |
|      |                          |           |      |(\\d{2}):(\\d{2})|Z)?)$']                         |                                                  |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.1.2|attributionType           |0-1        |string|['controlled list']                               |(Context: MovieArchives) ( ref:                   |
|      |                          |           |      |                                                  |attributionType@21.T11148/62304704da8a6510e9e4 )  |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.2  |sourceDate                |0-1        |string|['^([0-9]{4})(-)?([0][1-9]|1[0-2])(-)?([0-2][0-   |combined date and time representations as string. |
|      |                          |           |      |9]|3[0-1])([T| ]([0-1][0-9]|2[0-3])(:)?([0-5][0-  |It refers to RFC3339 and ISO 8601 and allows to   |
|      |                          |           |      |9])(:)?([0-5][0-9](\\.[0-9]*)?(Z|([\\+|-]([0-1][0-|give just date, week or ordinal date notation and |
|      |                          |           |      |9]|2[0-3])(:)?([0-5][0-9])?))?))?$']              |combined date and time in UTC. Defined by regular |
|      |                          |           |      |                                                  |expression. ( ref: date-time-                     |
|      |                          |           |      |                                                  |weak@21.T11148/9ca79b6ce26f3fd4fad3 )             |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.3  |sourceIdentifier          |0-1        |string|['^(([^:/?#]+):)(\\/\\/([^/?#]*))?([^?#]*)(\\?([^#|URI: Uniform Resource Identifier ( context :      |
|      |                          |           |      |]*))?(#(.*))?']                                   |generic ) ( ref:                                  |
|      |                          |           |      |                                                  |URI@21.T11148/5fd9bd37e430da57d338 )              |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|10.4  |sourceName                |1          |string|['(.|\n)*']                                       |string consisting of unicode characters. ( context|
|      |                          |           |      |                                                  |: generic ) ( ref: unicode-                       |
|      |                          |           |      |                                                  |string@21.T11148/798588c5a1ec532f737b )           |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|11    |specific_carrier_type     |0-1        |string|['controlled list']                               |Materialiarten (Context: Movie_DB) ( ref: specific|
|      |                          |           |      |                                                  |_carrier_type@21.T11148/3f564c8bc25abd6ba8e8 )    |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|12    |supplementary_information |0-1        |string|['(.|\n)*']                                       |Additional information specific to the Item (     |
|      |                          |           |      |                                                  |context : movie_db_ZIB ) ( ref: supplementary_info|
|      |                          |           |      |                                                  |rmation@21.T11148/7d811596268aceb7a0b3 )          |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
|13    |title                     |0-1        |string|['(.)*']                                          |string consisting of unicode characters except    |
|      |                          |           |      |                                                  |newline. ( ref: unicode-line-                     |
|      |                          |           |      |                                                  |string@21.T11148/f1627ce85386d8d75078 )           |
+------+--------------------------+-----------+------+--------------------------------------------------+--------------------------------------------------+
