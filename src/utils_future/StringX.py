class StringX:
    def __init__(self, x: str) -> None:
        self.x = x

    @property
    def int(self) -> int:
        return int(self.x.replace(",", "").replace(" ", "")) if self.x else 0

    def get_float(self, ndigits) -> float:
        float_x = (
            float(self.x.replace(",", "").replace(" ", "")) if self.x else 0.0
        )

        return round(float_x, ndigits)

    def get_percent(self, ndigits=2) -> float:
        return round(
            StringX(self.x[:-1]).get_float(ndigits + 2) / 100.0, ndigits
        )
