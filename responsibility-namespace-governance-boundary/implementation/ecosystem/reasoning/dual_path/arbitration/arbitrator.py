"""Arbitrator placeholder for MNGA dual-path reasoning arbitration."""


class Arbitrator:
    """Stub arbitrator selecting between internal and external results."""

    def choose(self, internal_result, external_result):
        return internal_result if internal_result is not None else external_result
