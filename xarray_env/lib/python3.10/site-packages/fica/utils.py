class ConfigProcessingException(Exception):

    key: str
    message: str

    def __init__(self, key, message):
        super().__init__(f"An error occured while processing {key}: {message}")
        self.key = key
        self.message = message

    @classmethod
    def from_child(cls, key, e):
        if not isinstance(e, cls):
            raise TypeError(f"Child exception has invalid type: {type(e)}")
        return cls(f"{key}.{e.key}", e.message)
