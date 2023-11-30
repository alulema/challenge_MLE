class InvalidMonthValueException(Exception):
    """Exception raised when an invalid month value is encountered in the data."""
    def __init__(self, message="Invalid month value detected in data"):
        self.message = message
        super().__init__(self.message)


class InvalidTipoVueloValueException(Exception):
    """Exception raised when an invalid TIPOVUELO value is encountered in the data."""
    def __init__(self, message="Invalid TIPOVUELO value detected in data"):
        self.message = message
        super().__init__(self.message)
