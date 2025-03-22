from datetime import datetime, timedelta
import re


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
    def offset(offset: str) -> timedelta:
        parts: list[str] = offset.split(" ")
        period: int = int(parts[0])
        unit: str = parts[1]
        if re.match(r"weeks?", unit):
            return timedelta(weeks=period)
        if re.match(r"days?", unit):
            return timedelta(days=period)
        if re.match(r"hours?", unit):
            return timedelta(hours=period)
        if re.match(r"minutes?", unit):
            return timedelta(minutes=period)
        raise ValueError(f"Invalid offset: {offset}")

    @staticmethod
    def parse(date_string: str) -> datetime | None:
        clean_string: str = date_string.lower()
        if clean_string in ["later"]:
            return datetime.now() + timedelta(hours=1)
        if clean_string in ["now", "today"]:
            return DateUtil.today()
        if clean_string == "tomorrow":
            return DateUtil.tomorrow()
        if re.match(r"\d* [a-z]*", clean_string):
            return datetime.now() + DateUtil.offset(clean_string)
        if clean_string in DateUtil.DAYS:
            weekday_index: int = DateUtil.DAYS.index(clean_string)
            delta: int = weekday_index - DateUtil.today().weekday()
            if delta <= 0:
                delta += 7
            return DateUtil.today() + timedelta(days=delta)
        for pattern in DateUtil.DATE_PATTERNS:
            try:
                return datetime.strptime(clean_string, pattern)
            except ValueError:
                pass
        if clean_string in ["never", "none", "na", "n/a"]:
            return None
        raise ValueError(f"Invalid due date: {date_string}")

    @staticmethod
    def format(date: datetime | None) -> str | None:
        if date:
            return date.strftime("%Y-%m-%d %H:%M:%S")
        return None
