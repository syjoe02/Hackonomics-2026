class SimulationResult:
    def __init__(
        self,
        currency: str,
        period: str,
        monthly_amount: float,
        deposit_rate: float,
        total_invested: float,
        usd_final: float,
        deposit_final: float,
        winner: str,
        diff_percent: float,
        summary: str,
    ):

        self.currency = currency
        self.period = period
        self.monthly_amount = monthly_amount
        self.deposit_rate = deposit_rate

        self.total_invested = total_invested
        self.usd_final = usd_final
        self.deposit_final = deposit_final

        self.winner = winner
        self.diff_percent = diff_percent
        self.summary = summary

    def is_usd_winner(self) -> bool:
        return self.winner == "usd"

    def is_deposit_winner(self) -> bool:
        return self.winner == "deposit"

    def to_dict(self) -> dict:
        return {
            "currency": self.currency,
            "period": self.period,
            "monthly_amount": round(self.monthly_amount, 2),
            "deposit_rate": round(self.deposit_rate, 2),
            "usd": {
                "invested": round(self.total_invested, 2),
                "final": round(self.usd_final, 2),
            },
            "deposit": {
                "invested": round(self.total_invested, 2),
                "final": round(self.deposit_final, 2),
            },
            "winner": self.winner,
            "diff_percent": round(self.diff_percent, 2),
            "summary": self.summary,
        }
