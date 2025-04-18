# Using Python bindings for the AVefi schema

AVefi compliant JSON data can be transformed into native Python
objects and back again. This can be helpful when writing code that is
supposed to generate AVefi compliant data, especially when using an
IDE that supports auto-completion of objects defined in imported
modules.

In a virtual environment, you can install the language bindings with
pip like this:

```console
$ pip install "avefi_schema[dataclasses] @ git+https://github.com/AV-EFI/av-efi-schema.git"
```

The module is then available as:

```python
>>> from avefi_schema import model as efi
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

A pydantic model of the AVefi schema is available too and can be used
as follows:

```python
>>> from avefi_schema import model_pydantic_v2 as efi
```

This module only depends on pydantic and not on the linkml-runtime
library. So, if your application does not rely on certain polymorphism
features supported only by the dataclasses module, it may be desirable
to use this one instead and reduce dependencies by leaving out the
`[dataclasses]` qualifier from the installation command above.
