import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import override

from style_predictor.pgn_parser.exceptions import PGNLexerError

movetext_pattern = re.compile(
    r"(?P<movenumber>\d+\.{1,3})\s*"
    r"(?P<whitemove>[a-hxRNBQKO1-8#+=]{2,}|O-O-O[#+]?|O-O[#+]?)?\s*"
    r"(?P<whitecomment>\{[^}]*\})?\s*"
    r"(?:(?P<black_num>\d+)\.\.\.)?\s*"  # Optional black move number
    r"(?P<blackmove>[a-hxRNBQKO1-8#+=]{2,}|O-O-O[#+]?|O-O[#+]?)?\s*"
    r"(?P<blackcomment>\{[^}]*\})?\s*"
)
game_term_pattern = re.compile(r"(?P<gameterm>\*|0-1|1/2-1/2|1-0)")


class TokenType(Enum):
    STRING = auto()
    NEWLINE = auto()
    NUMBER = auto()
    PERIOD = auto()
    STAR = auto()
    LSQB = auto()
    RSQB = auto()
    TAGNAME = auto()
    TAGVALUE = auto()
    MOVENUMBER = auto()
    GAMETERM = auto()
    CASTLEKINGSIDE = auto()
    CASTLEQUEENSIDE = auto()
    DRAW = auto()
    CHECK = auto()
    CHECKMATE = auto()
    PROMOTIONINDICATOR = auto()
    PROMOTIONPIECE = auto()
    CAPTURE = auto()
    INVALID = auto()


class Position:
    linenumber: int
    column: int

    def __init__(self, lnumber: int, column: int) -> None:
        self.linenumber = lnumber
        self.column = column

    @override
    def __repr__(self) -> str:
        return f"Position({self.linenumber}, {self.column})"


@dataclass
class Token:
    tvalue: str
    ttype: TokenType
    tpos: Position


@dataclass
class MoveToken(Token):
    twhitemovecomment: str | None = None
    tblackmovecomment: str | None = None
    tmovesuffix: str | None = None
    twhitemove: str | None = None
    tblackmove: str | None = None


class Lexer:
    def __init__(self, data: str):
        self._buffer = data
        self._buffer_pos: int = 0
        self._loc = Position(1, 1)
        self._tokens: list[Token] = list()

    def lex(self) -> None | list[Token]:
        while True:
            match self.peek():
                case "[":
                    self.lex_tag_pair()
                case "\n":
                    _ = self.read()
                    self._cr_pos()
                    if self.peek() and self.peek().isdigit():
                        self.lex_movetext()
                        # break
                case None:
                    break
                case _:
                    _ = self.read()
        return self._tokens

    def lex_tag_pair(self):
        # r"\[([A-Za-z0-9\_\+\=\-\:]*)\s\"(.*)\"\]"
        c = self.read()
        self._expect(str(c), "[", "TagPair Not correctly structured")
        self._tokens.append(
            Token(
                str(c), TokenType.LSQB, Position(self._loc.linenumber, self._loc.column)
            )
        )
        self._incr_pos_column()
        self.lex_tag_name()
        self.lex_tag_value()
        c = self.read()
        self._expect(str(c), "]", "TagPair Not correctly structured")
        self._tokens.append(
            Token(
                str(c), TokenType.RSQB, Position(self._loc.linenumber, self._loc.column)
            )
        )
        self._incr_pos_column()

    def lex_tag_name(self):
        tag_name: str = ""
        while (
            not (self.peek()) == '"'
            and not (self.peek()) == "\n"
            and not (self.peek()) == "]"
        ):
            if data := self.read():
                tag_name += data
                self._incr_pos_column()
        self._tokens.append(
            Token(
                tag_name.strip(),
                TokenType.TAGNAME,
                Position(self._loc.linenumber, self._loc.column - len(tag_name)),
            )
        )

    def lex_tag_value(self):
        tag_value: str = ""
        c = self.read()
        self._expect(str(c), '"', "TagPair Not correctly structured")
        self._incr_pos_column()
        while not (self.peek()) == '"':
            if data := self.read():
                tag_value += data
                self._incr_pos_column()
        self._tokens.append(
            Token(
                tag_value.strip(),
                TokenType.TAGVALUE,
                Position(self._loc.linenumber, self._loc.column - len(tag_value)),
            )
        )
        c = self.read()
        self._expect(str(c), '"', "TagPair Not correctly structured")
        self._incr_pos_column()

    def lex_movetext(self):
        while True:
            match = movetext_pattern.match(
                self._buffer[self._buffer_pos :].replace("\n", " ")
            )
            if match:
                movenumber = match.groupdict().get("movenumber")
                tok: MoveToken | None = None
                if movenumber:
                    tok = MoveToken(
                        movenumber,
                        TokenType.MOVENUMBER,
                        Position(self._loc.linenumber, self._loc.column),
                    )
                if not tok:
                    return
                whitemove = match.groupdict().get("whitemove")
                if whitemove:
                    tok.twhitemove = whitemove
                whitecomment = match.groupdict().get("whitecomment")
                if whitecomment:
                    tok.twhitemovecomment = whitecomment
                blackmove = match.groupdict().get("blackmove")
                if blackmove:
                    tok.tblackmove = blackmove
                blackcomment = match.groupdict().get("blackcomment")
                if blackcomment:
                    tok.tblackmovecomment = blackcomment
                self._tokens.append(tok)
                self._buffer_pos += match.end()
            else:
                term = game_term_pattern.match(
                    self._buffer[self._buffer_pos :].replace("\n", " ")
                )
                if term:
                    gameterm = term.groupdict().get("gameterm")
                    if gameterm:
                        self._tokens.append(
                            Token(
                                gameterm,
                                TokenType.GAMETERM,
                                Position(self._loc.linenumber, self._loc.column),
                            )
                        )

                break

    def read(self) -> str | None:
        if self._buffer_pos >= len(self._buffer):
            return None
        res = self._buffer[self._buffer_pos]
        self._buffer_pos += 1
        return res

    def decr_pos_column(self, count: int = 1):
        self._loc.column -= count

    def _incr_pos_column(self, count: int = 1):
        self._loc.column += count

    def _cr_pos(self):
        self._loc.linenumber += 1
        self._loc.column = 1

    def backup(self):
        self._buffer_pos -= 1

    def peek(self) -> str | None:
        if self._buffer_pos >= len(self._buffer):
            return None
        return self._buffer[self._buffer_pos]

    def _expect(self, actual: str, expected: str, msg: str):
        if actual != expected:
            raise PGNLexerError(msg)
