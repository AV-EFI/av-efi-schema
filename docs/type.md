

# Slot: type

URI: [avefi:type](https://av-efi.net/schema/av-efi-schema/type)



<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Format](Format.md) | FIAF Moving Image Cataloguing Manual 2 |  no  |
| [Activity](Activity.md) | FIAF Moving Image Cataloguing Manual 1 |  yes  |
| [Optical](Optical.md) | FIAF Moving Image Cataloguing Manual D |  yes  |
| [Audio](Audio.md) | FIAF Moving Image Cataloguing Manual D |  yes  |
| [WorkVariant](WorkVariant.md) | FIAF Moving Image Cataloguing Manual 1 |  yes  |
| [Film](Film.md) | FIAF Moving Image Cataloguing Manual D |  yes  |
| [Agent](Agent.md) | Agent involved in some activity related to the moving image resource |  yes  |
| [DigitalFile](DigitalFile.md) | FIAF Moving Image Cataloguing Manual D |  yes  |
| [Title](Title.md) | FIAF Moving Image Cataloguing Manual 1 |  yes  |
| [DigitalFileEncoding](DigitalFileEncoding.md) | FIAF Moving Image Cataloguing Manual D |  yes  |
| [Video](Video.md) | FIAF Moving Image Cataloguing Manual D |  yes  |
| [Event](Event.md) | Significant event in the lifecycle of moving image work / variant, manifestat... |  yes  |
| [Manifestation](Manifestation.md) | FIAF Moving Image Cataloguing Manual 2 |  yes  |







## Properties

* Range: [Uriorcurie](Uriorcurie.md)





## Identifier and Mapping Information







### Schema Source


* from schema: https://av-efi.net/schema/av-efi-schema




## LinkML Source

<details>
```yaml
name: type
from_schema: https://av-efi.net/schema/av-efi-schema
rank: 1000
alias: type
domain_of:
- WorkVariant
- Activity
- Agent
- Event
- Title
- Format
- Manifestation
range: uriorcurie

```
</details>