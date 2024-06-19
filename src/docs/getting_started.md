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
