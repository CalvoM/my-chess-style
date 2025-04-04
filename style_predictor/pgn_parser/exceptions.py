class PGNError(Exception):
    def __init__(self, message: str | None) -> None:
        self.message = message
        super().__init__(self.message)


class PGNLexerError(PGNError):
    pass


class PGNParserError(PGNError):
    pass
