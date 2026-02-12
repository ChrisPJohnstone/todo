import os
import sys


if not __package__:
    """
    Using src layout is recommended for Python packages however it is not possible
    to run the package without installing unless you manipulate the sys.path.

    More details:
    https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
    """
    package_source_path: str = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

    from cli import main  # type: ignore[unresolved-import]

    main()
