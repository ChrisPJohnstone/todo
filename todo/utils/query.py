class QueryUtil:
    @staticmethod
    def parse_criteria(criteria: list[str], include_completed: bool) -> str:
        constructor: list[str] = []
        if not include_completed:
            constructor.append("not completed")
        if criteria:
            if criteria[0].lower() == "where":
                criteria.pop(0)
            constructor.append(" ".join(criteria))
        output: str = " AND ".join(constructor)
        return f"WHERE {output}" if output else ""
