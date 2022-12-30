"""
@ARTHUR:rkp
"""

class TableCreationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class MultipleValueReturn(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

