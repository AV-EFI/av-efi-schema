# Controlled Vocabularies

This folder contains the controlled vocabularies used in the schemas.
References to definitions and descriptions outside of the project will be added later.
The vocabularies can be used in JSON schema by using the correct URL, e.g., for the "titleType" 
https://raw.githubusercontent.com/AV-EFI/av-efi-schema/main/Controlled_Vocabularies/work_1.1_titleType.json

The terms used are all given in upper CamelCase notation.

Example how to make use of the controlled vocabularies in a JSON Schema:
```
{
  "properties": {
    "genres": {
      "description": "implicitly created because of multiple occurence of child type genre: The name of  genre, which characterise the general style of a cinematographic work.",
      "items": {
        "description": "A descriptor or descriptors, preferably from a controlled vocabulary which characterise the general style of a cinematographic work.",
        "$ref": "https://raw.githubusercontent.com/AV-EFI/av-efi-schema/main/Controlled_Vocabularies/work_12_genre.json",
        "type": "string"
      },
      "type": "array"
    }
  },
  "required": [
    "genres"
  ],
  "type": "object",
  "$schema": "http://json-schema.org/draft-04/schema#",
  "description": "Schema for type instances derived from type description hdl:21.T11148/cee386b04503398bc6ca"
}
