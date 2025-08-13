# Using Python bindings for the AVefi schema

AVefi compliant JSON data can be transformed into native Python
objects and back again. This can be helpful when writing code that is
supposed to generate AVefi compliant data, especially when using an
IDE that supports auto-completion of objects defined in imported
modules.

In a virtual environment, you can install the language bindings with
pip like this:

```console
$ pip install "avefi_schema @ git+https://github.com/AV-EFI/av-efi-schema.git"
```

The module is then available as:

```python
>>> from avefi_schema import model_pydantic_v2 as efi
```

See [menschen_am_sonntag.py](./menschen_am_sonntag.py) in this
directory for sample code using those language bindings.

Please note that the generated JSON output is likely but not
guaranteed to be schema compliant. Particularly, formatting
requirements within a field (e.g. "has_date") or limits on the length
of field contents are not enforced. Besides, when generating data
export files intended for PID registration by another party, they
typically include local identifiers in order to express relationships
between the different data records. It is important that all
references to local identifiers can be resolved within the same file.
Please refer to the check module in the [efi-conv
repository](https://github.com/AV-EFI/efi-conv).

A dataclasses model of the AVefi schema is available too and can be used
as follows:

```python
>>> from avefi_schema import model as efi
```

This module has additional dependencies on the linkml-runtime library,
though. So, if you need this module, you will have to run the
following command in order to pull in those dependencies:

```console
$ pip install "avefi_schema[dataclasses] @ git+https://github.com/AV-EFI/av-efi-schema.git"
```

[LinkML loaders and
dumpers](https://linkml.io/linkml/developers/loaders-and-dumpers.html)
may come in handy when using the dataclasses module. The
[menschen_am_sonntag.py example](./menschen_am_sonntag.py) would have
to be modified along these lines:

```python
from avefi_schema import model as efi
from linkml_runtime.dumpers import JSONDumper
from linkml_runtime.loaders import JSONLoader

def main():
    # Initialise helpers
    dumper = JSONDumper()
    loader = JSONLoader()
    
    # ...

    # Write data to file
    dumper.dump([work, manifestation, item], json_file, inject_type=False)

    # Read data back again
    records = loader.load_any(json_file, efi.MovingImageRecord)
```
