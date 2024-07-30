# LinkML generator for the Data Type Registry

## Purpose and usage of the TypeRegistrySubset

Given the source schema expressed in LinkML, types, enumerations,
classes and slots can be flagged for export to the Data Type Registry
by adding them to the TypeRegistrySubset.

## Modelling LinkML classes and inheritance in the Type Registry

Broadly speaking, LinkML classes correspond to InfoTypes in the Type
Registry since schema properties of an InfoType operate similarly to
slots in the context of a given LinkML class. For the type of schema
properties, PIDs of either a BasicInfoType or an InfoType are accepted
in much the same way that the range of a slot can be either a type, an
enumeration or a class. Additionally, the cardinality of schema
properties expresses accurately whether a slot is required and / or
multi-valued or not, as demonstrated below:

| cardinality | slot required | slot multivalued |
|-------------|---------------|------------------|
| 0 - 1       | false         | false            |
| 0 - n       | false         | true             |
| 1           | true          | false            |
| 1 - n       | true          | true             |

There are some differences, though, that need to be taken into
account. Unlike LinkML classes, InfoTypes do not have built-in support
for subclassing and inheritance. They do provide more generic ways of
schema composition features, however, that allow to achieve similar
effects in a somewhat round about way. To this end, two aspeects of
subclassing and inheritance in LinkML need to be dealt with
separately:

1.  LinkML subclasses inherit all slots of their parent class and
    alter them or add new ones as appropriate. InfoTypes can achieve
    the same using the extractProperties feature, see below.
2.  If the range of a LinkML slot is a class, all defined subclasses
    are part of that range automatically. There is no such thing as a
    subInfoType in that sense, but InfoTypes can be chained together
    with boolean operators, most notably the anyOf operator. Hence,
    the range composed of a class and / or its subclasses can be
    represented by an InfoType composing all the others with anyOf, see below.

### Inheritance part 1 – `"extractProperties": true`

Consider a source schema containing the following snippet:

```yaml
classes:

  MovingImageRecord:
    slots:
    - has_event
    - in_language
    in_subset:
    - TypeRegistrySubset

  WorkVariant:
    is_a: MovingImageRecord
    slots:
    - has_form
    in_subset:
    - TypeRegistrySubset

slots:

  has_event:
    inlined_as_list: true
    multivalued: true
    range: Event
    in_subset:
    - TypeRegistrySubset

  has_form:
    multivalued: true
    range: WorkFormEnum
    in_subset:
    - TypeRegistrySubset

  in_language:
    multivalued: true
    range: Language
    in_subset:
    - TypeRegistrySubset
```

The generated InfoType for WorkVariant would be similar to this:

```yaml
{
  "name": "WorkVariant",
  "Schema": {
    "Type": "Object",
    "Properties": [
      {
        "Name": "MovingImageRecord__Trunk",
        "Type": "pid_for_MovingImageRecord__Trunk",
        "Properties": {
          "Cardinality": "0 - 1",
          "extractProperties": true
        }
      },
      {
        "Name": "has_form",
        "Type": "pid_for_Form",
        "Properties": {
          "Cardinality": "0 - n"
        }
      }
    ]
  }
}
```

See below for an explanation of that ominous MovingImageRecord__Trunk.

### Inheritance part 2 – `"subCond": "anyOf"`

Expanding on the example schema above, the MovingImageRecord class
would actually result in two InfoTypes (as would WorkVariant, if it
had subclasses of its own). Here is the essence of the two InfoTypes
for MovingImageRecord:

```yaml
{
  "name": "MovingImageRecord__Trunk",
  "Schema": {
    "Type": "Object",
    "addProps": false,
    "Properties": [
      {
        "Name": "has_event",
        "Type": "pid_for_Event",
        "Properties": {
          "Cardinality": "0 - n"
        }
      },
      {
        "Name": "in_language",
        "Type": "pid_for_Language",
        "Properties": {
          "Cardinality": "0 - n"
        }
      }
    ]
  }
}
# [...]
{
  "name": "MovingImageRecord",
  "Schema": {
    "Type": "Object",
    "subCond": "anyOf",
    "addProps": true,
    "Properties": [
      {
        "Name": "MovingImageRecord__Trunk",
        "Type": "pid_for_MovingImageRecord__Trunk",
        "Properties": {
          "Cardinality": "0 - 1"
        }
      },
      {
        "Name": "WorkVariant",
        "Type": "pid_for_WorkVariant",
        "Properties": {
          "Cardinality": "0 - 1"
        }
      }
    ]
  }
}
```

MovingImageRecord can also be defined as a so-called abstract class in
LinkML. This means that instances of MovingImageRecord itself are not
valid against the schema, but instances of children are (as long as
they are not abstract themselves). In terms of the InfoTypes outlined
above this means that MovingImageRecord__Trunk itself would not be
mentioned as a valid alternative in the MovingImageRecord InfoType.
