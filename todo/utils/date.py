from datetime import datetime, timedelta


class DateUtil:
    DAYS: list[str] = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    DATE_PATTERNS: list[str] = [
        r"%Y-%m-%d",
        r"%Y-%m-%d %H",
        r"%Y-%m-%d %H:%M",
        r"%Y-%m-%d %H:%M:%S",
        r"%d/%m/%Y",
        r"%d/%m/%Y %H",
        r"%d/%m/%Y %H:%M",
        r"%d/%m/%Y %H:%M:%S",
    ]

    @staticmethod
    def today() -> datetime:
        return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def tomorrow() -> datetime:
        return DateUtil.today() + timedelta(days=1)

    @staticmethod
    def parse(date: str) -> datetime | None:
        clean_date: str = date.lower()
        if clean_date in ["never", "none", "na", "n/a"]:
            return None
        if clean_date in ["now", "today"]:
            return DateUtil.today()
        if clean_date == "tomorrow":
            return DateUtil.tomorrow()
        if clean_date in DateUtil.DAYS:
            weekday_index: int = DateUtil.DAYS.index(clean_date)
            delta: int = weekday_index - DateUtil.today().weekday()
            if delta <= 0:
                delta += 7
            return DateUtil.today() + timedelta(days=delta)
        for pattern in DateUtil.DATE_PATTERNS:
            try:
                return datetime.strptime(date, pattern)
            except ValueError:
                pass
        raise ValueError(f"Invalid due date: {date}")

    @staticmethod
    def format(date: datetime | None) -> str | None:
        if date:
            return date.strftime("%Y-%m-%d %H:%M:%S")
        return None
