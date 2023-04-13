+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| ID    | Property               | Obligation | Occurance | Definition                     | Allowed values,        |
|       |                        |            |           |                                | constraints,           |
|       |                        |            |           |                                | remarks                |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 1     | title                  | M          | 1-n       | A word, phrase, character,     | Free Text              |
|       |                        |            |           | or group of characters,        |                        |
|       |                        |            |           | normally appearing in an item, |                        |
|       |                        |            |           | naming the item or the work    |                        |
|       |                        |            |           | contained in it.               |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 1.1   | titleType              | M          | 1         |                                | Controlled list of     |
|       |                        |            |           |                                | values:                |
|       |                        |            |           |                                |   Original Title,      |
|       |                        |            |           |                                |   Release Title,       |
|       |                        |            |           |                                |   Archive Title,       |
|       |                        |            |           |                                |   Alternative Title,   |
|       |                        |            |           |                                |   Sort Title           |
|       |                        |            |           |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 2     | source                 | M          | 1         | The name of the archive or     | Free Text              |
|       |                        |            |           | other organisation supplying   |                        |
|       |                        |            |           | the record.                    |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 2.1   | source_identifier      | O          | 0-1       |                                | URI                    |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 3     | last_modified          | M          | 1         | Date and time of last          | ISO8601                |
|       |                        |            |           | update to metadata record.     |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 4     | series                 | O          | 0-1       | A series is a group of separate|                        |
|       |                        |            |           | items related to one another by|                        |
|       |                        |            |           | the fact that each item bears, |                        |
|       |                        |            |           | in addition to its own title,  |                        |
|       |                        |            |           | a collective title applying to |                        |
|       |                        |            |           | the group as a whole.          |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 5     | cast                   | O          | 0-n       | A collective term for actors   |                        |
|       |                        |            |           | and their roles. A broad       |                        |
|       |                        |            |           | distinction is made between    |                        |
|       |                        |            |           | cast and credits by defining   |                        |
|       |                        |            |           | cast as those in front of the  |                        |
|       |                        |            |           | camera and credits as those    |                        |
|       |                        |            |           | behind the camera.             |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 6     | credits                | O          | 0-n       | The names and functions of     |                        |
|       |                        |            |           | persons responsible for the    |                        |
|       |                        |            |           | production and/or artistic or  |                        |
|       |                        |            |           | intellectual content of a      |                        |
|       |                        |            |           | cinematographic work.          |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 7     | production_company     | O          | 0-n       | The name of an organisation or |                        |
|       |                        |            |           | company under whose financial, |                        |
|       |                        |            |           | technical and organisational   |                        |
|       |                        |            |           | management a cinematographic   |                        |
|       |                        |            |           | work is made.                  |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 8     | country_of_reference   | O          | 0-n       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 9     | original_format        | O          | 0-1       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 10    | original_length        | O          | 0-n       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 11    | original_duration      | O          | 0-n       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 12    | original_language      | O          | 0-n       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 13    | year_of_reference      | O          | 0-n       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 13.1  | start_year             | O          | 0-1       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 13.2  | end_year               | O          | 0-1       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 13.3  | reference_Type         | 1          | 1         |                                | Controlled list of:    | 
|       |                        |            |           |                                |   created,             |
|       |                        |            |           |                                |   copyrighted,         |
|       |                        |            |           |                                |   issued               |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 14    | genre                  | O          | 0-n       |                                | Controlled list of     |
|       |                        |            |           |                                | values:                |
|       |                        |            |           |                                |   Amateur film,        |
|       |                        |            |           |                                |   Animation,           |
|       |                        |            |           |                                |   Animation with       |
|       |                        |            |           |                                |   live-action,         |
|       |                        |            |           |                                |   Non-fiction,         |
|       |                        |            |           |                                |   Documentary-drama,   |
|       |                        |            |           |                                |   Anthology film,      |
|       |                        |            |           |                                |   Essay film,          |
|       |                        |            |           |                                |   Experimental film,   |
|       |                        |            |           |                                |   Home movie,          |
|       |                        |            |           |                                |   Industrial film,     |
|       |                        |            |           |                                |   Compilation film,    |
|       |                        |            |           |                                |   Short film,          |
|       |                        |            |           |                                |   Educational film,    |
|       |                        |            |           |                                |   Music video,         |
|       |                        |            |           |                                |   Propaganda film,     |
|       |                        |            |           |                                |   Fiction,             |
|       |                        |            |           |                                |   Trailer,             |
|       |                        |            |           |                                |   Advertising film,    |
|       |                        |            |           |                                |   Newsreel             |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
| 15    | relationship           | O          | 0-n       |                                |                        |
+-------+------------------------+------------+-----------+--------------------------------+------------------------+
