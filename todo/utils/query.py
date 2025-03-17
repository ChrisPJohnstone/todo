from argparse import Namespace


class QueryUtil:
    @staticmethod
    def parse_criteria(args: Namespace) -> str:
        if args.include_completed:
            output: str = "WHERE completed"
        else:
            output: str = "WHERE not completed"
        if not args.criteria:
            return output
        if args.criteria[0].lower() == "where":
            args.criteria.pop(0)
        if not args.criteria:
            return output
        return f"{output} AND {' '.join(args.criteria)}"
