"""Value object for a program ID."""


class ProgramId(str):
    """Value object for a program ID."""

    @classmethod
    def __get_validators__(cls):
        """Returns one or more validators.

        Yields:
            One or more validator methods.
        """
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("Program ID must be string")

        return v

    def __repr__(self):
        return f"Program ID: {super().__repr__()}"
