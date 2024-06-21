# Guide to AVefi schema coming from EN 15744

The AVefi Schema is developed in LinkML. In that framework, it is
composed of elements falling into four categories: slots, types,
enumerations, and classes. Slots can be thought of as data fields and
correspond to the keys in a JSON object. Consider, for example, the
following object describing an event:

```yaml
{
  "category": "avefi:ProductionEvent",
  "has_activity": [],   # list of activities and agents
  "has_date": "1929/1930",
  "located_in": [
    {
      "has_name": "Germany (German Reich)",
      "same_as": [
        {
          "category": "avefi:GNDResource",
          "id": "2008993-4"
        }
      ]
    }
  ]
}
```

This means that the AVefi schema defines a slot with the name has_date
(see the key of that name above) and a range of values as string of a
certain pattern.

Expected keys and the accepted range of corresponding values are
defined as slots in the AVefi schema.

## Example

This section illustrates the transformation of a sample dataset in the EN15744 standard into a JSON object according to the AVefi Schema. For each element, the expected form and position within the JSON object will be shown.

The following table displays an abbreviated excerpt from the sample dataset of the Work [‘Menschen am Sonntag - Das Dokument der Gegenwart’](https://github.com/AV-EFI/av-efi-schema/blob/main/examples/json/monographic_work_pid.json), shaped according to EN15744”.
| EN 15744 Element     | Value                                               |
|----------------------|-----------------------------------------------------|
| Title                | Menschen am Sonntag – Das Dokument der Gegenwart    |
| Cast                 | Borchert, Brigitte                                  |
| Credits              | Siodmak, Robert                                     |
| Country of Reference | Germany (German Reich)                              |
| Year of Reference    | 1929/1930                                           |
| Identifier           | 21.T11998/60BC0D95-6F00-4E84-B77B-F3174C211C12      |
| Identifier           | f570e1abdad841dc8d5b25b0f7737065                    |
| Genre                | Fiction                                             |
| Source               | Deutsche Kinemathek - Museum für Film und Fernsehen |

These are the first few lines of the corresponding JSON object (COMMENT: Zur Beschreibung von has_record, **Title**, **Source**, **Identifier**)

```yaml
{
  "has_record": {
    "category": "avefi:WorkVariant",
    "id": "21.T11998/60BC0D95-6F00-4E84-B77B-F3174C211C12",
    "has_primary_title": {
      "has_name": "Menschen am Sonntag – Das Dokument der Gegenwart",
      "type": "PreferredTitle"
    },
    "described_by": {
      "has_issuer_id": "https://w3id.org/isil/DE-MUS-407010",
      "has_issuer_name": "Deutsche Kinemathek - Museum für Film und Fernsehen",
      "last_modified": "2024-05-13T15:12:41+00:00"
    },
  ...
  }
  "@type": "MovingImageRecordContainer"
}
```

Within the AVefi Schema information concerning the production of the Work is described as part of a production event. This includes **Cast**, **Credits**, **Country of Reference** and **Year of Reference** (COMMENT: Hier Beschreibung von genannten Elementen):

```yaml
    "has_event": [
      {
        "category": "avefi:ProductionEvent",
        "has_activity": [
          {
            "category": "avefi:CastActivity",
            "has_agent": [
              {
                "has_name": "Borchert, Brigitte",
                "type": "Person",
                "same_as": [
                  {
                    "category": "avefi:GNDResource",
                    "id": "173787681"
                  }
                ]
              },
            ...
            ],
            "type": "CastMember"
          },
          ...
          {
            "category": "avefi:DirectingActivity",
            "has_agent": [
              {
                "has_name": "Siodmak, Robert",
                "type": "Person",
                "same_as": [
                  {
                    "category": "avefi:GNDResource",
                    "id": "11861472X"
                  }
                ]
              },
              ...
            ],
            "type": "Director"
          },
          ...
        ],
        "has_date": "1929/1930",
        "located_in": [
          {
            "has_name": "Germany (German Reich)",
            "same_as": [
              {
                "category": "avefi:GNDResource",
                "id": "2008993-4"
              }
            ]
          }
        ]
      }
    ],
```

**Genre** and additional **Identifiers** are described as followed:

```yaml
    "has_genre": [
      {
        "has_name": "Fiction"
      }
    ],
    "same_as": [
      {
        "category": "avefi:FilmportalResource",
        "id": "f570e1abdad841dc8d5b25b0f7737065"
      }
    ]
```
