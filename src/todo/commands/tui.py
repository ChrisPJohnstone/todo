from argparse import ArgumentParser, Namespace



def command_parsers() -> list[ArgumentParser]:
    return []


def main(args: Namespace) -> None:
    print(args)
