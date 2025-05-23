# LinkML generator for the Data Type Registry

Please consult the [Data Type Registry user
documentation][typeregistry] and [LinkML generator
documentation][linkml_gen] for background information.

The DataTypeGenerator class can be used in two modes of operation as
determined by the sync_mode parameter: By default,
`(sync_mode=False)` it operates on a read-only basis trying to find
PIDs for types, enums and classes in the source schema, resolving them
and comparing the retrieved data to the InfoType or BasicInfoType
generated on the fly from that type, enum or class. Otherwise,
(`sync_mode=True`) InfoTypes (respectively BasicInfoTypes) are
updated as far as a PID has been registered for them already and is on
record in the source schema, or they are registered to begin with and
the resulting PID is added to the source schema.

Note that types, enums, classes and even slots must be added to the
TypeRegistrySubset in order to get processed by the generator,
otherwise they are simply ignored. Only (abstract) parent classes will
be silently added to the TypeRegistrySubset if a non-abstract child
was part of it already.

Also, be aware that the range of every slot processed by the generator
must itself be explicitly defined as a type, enum or class. This is
because slots translate into properties of InfoTypes and the type of
such a property must always be the PID of some other InfoType or
BasicInfoType.

Briefly, LinkML concepts are represented in the Data Type Registry as
follows:
*   LinkML types are mapped to BasicInfoTypes in a fairly straight
    forward way. Additional constraints known to the Type Registry but
    not to LinkML can be added under data_type_properties in the
    annotations section.
*   Enumerations are duplicated as json files in the repository and then
    referenced via the `$ref` property of BasicInfoTypes in the Type
    Registry.
*   A LinkML class will yield one InfoType containing one Property for
    each slot or attribute of the class and possibly an additional
    wrapper InfoType if there are subclasses defined in the source
    schema.

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

[typeregistry]: https://fc4e-t4-3.github.io/
[linkml_gen]: https://linkml.io/linkml/generators/index.html
