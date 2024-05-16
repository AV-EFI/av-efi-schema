# Mapping and data exchange formats

The underlying APIs used in the AVefi project use JSON as a data
exchange format. We aim to assist our partners in mapping their data
to the AVefi metadata schema and convert them from different source
formats. You can find some [sample datasets][] within the schema
repository.

[sample datasets]: https://github.com/AV-EFI/av-efi-schema/tree/main/examples/

For demonstration purposes and better readability, here is an example
in YAML, is it might be provided by a film archive in order to
register PIDs for a film work, a particular manifestation and the
local item:

```yaml
---
category: avefi:MovingImageRecordCollection
has_record:
- category: avefi:WorkVariant
  type: Monographic
  id: work_identifier
  has_primary_title:
    type: PreferredTitle
    has_name: Menschen am Sonntag – Das Dokument der Gegenwart
  has_event:
  - type: ProductionEvent
    has_date: 1929/1930
    located_in:
    - has_name: Germany (German Reich)
      same_as:
      - category: avefi:GNDResource
        id: 2008993-4
    has_activity:
    - type: CastMember
      has_agent:
      - type: Person
        has_name: Borchert, Brigitte
        same_as:
        - category: avefi:GNDResource
          id: '173787681'
      - type: Person
        has_name: Splettstößer, Erwin
        same_as:
        - category: avefi:GNDResource
          id: '1061393046'
      - type: Person
        has_name: Waltershausen, Wolfgang von
        same_as:
        - category: avefi:GNDResource
          id: '173857868'
    - type: Writer
      has_agent:
      - type: Person
        has_name: Wilder, Billy
        same_as:
        - category: avefi:GNDResource
          id: '118632795'
    - type: Director
      has_agent:
      - type: Person
        has_name: Siodmak, Robert
        same_as:
        - category: avefi:GNDResource
          id: 11861472X
      - type: Person
        has_name: Ulmer, Edgar G.
        same_as:
        - category: avefi:GNDResource
          id: '124471196'
      - type: Person
        has_name: Gliese, Rochus
        same_as:
        - category: avefi:GNDResource
          id: '116663308'
    - type: Cinematographer
      has_agent:
      - type: Person
        has_name: Schüfftan, Eugen
        same_as:
        - category: avefi:GNDResource
          id: 12495748X
    - type: FilmEditor
      has_agent:
      - type: Person
        has_name: Siodmak, Robert
        same_as:
        - category: avefi:GNDResource
          id: 11861472X
    - type: Composer
      has_agent:
      - type: Person
        has_name: Stenzel, Otto
  has_genre:
  - has_name: Fiction
  same_as:
  - category: avefi:FilmportalResource
    id: f570e1abdad841dc8d5b25b0f7737065
  described_by:
    has_issuer_id: DE-MUS-407010
    has_issuer_name: Deutsche Kinemathek - Museum für Film und Fernsehen
    last_modified: '2024-05-13T15:12:41Z'
- category: avefi:Manifestation
  type: PreservationRestoration
  id: manifestation_identifier
  has_primary_title:
    type: TitleProper
    has_name: Menschen am Sonntag
  has_event:
  - type: ProductionEvent
    has_date: 2013/2014
  - type: ReleaseEvent
    has_date: 2014
  in_language:
  - usage: Intertitles
    code: deu
  - usage: Subtitles
    code: eng
  - usage: Subtitles
    code: fra
  has_colour_type: BlackAndWhite
  has_sound_type: Sound
  is_manifestation_of:
  - category: avefi:LocalResource
    id: work_identifier
  has_item:
  - category: avefi:LocalResource
    id: item_identifier1
- category: avefi:Item
  element_type: DCP
  id: item_identifier1
  has_primary_title:
    type: TitleProper
    has_name: Menschen am Sonntag
  has_access_status: Distribution
  has_extent:
    has_unit: GigaByte
    has_value: 113
  has_format:
  - category: avefi:DigitalFile
    type: MXF
  is_item_of:
    category: avefi:LocalResource
    id: manifestation_identifier
```
