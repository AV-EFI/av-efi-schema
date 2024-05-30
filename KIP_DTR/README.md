# Schema in DTR

This folder contains information about the representation of the AV-EFI Schema in the EOSC Data Type Registry.

The current verions are referenced via 

work/variant: 21.T11148/31b848e871121c47d064

manifestation: 21.T11148/ef6836b80e4d64e574e3

item: 21.T11148/b0047df54c686b9df82a

To retrieve the JSON Schema for, e.g., the work you can use
```
curl -X 'GET' \
  'http://typeapi.pidconsortium.net/dtype/schema/JSON/21.T11148/31b848e871121c47d064/?cached=true' \
  -H 'accept: application/json'
```
