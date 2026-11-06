"""bcsfekorea: 냥코 대전쟁 세이브 에디터(BCSFE) 한국어판.

실제 코드는 bcsfe 패키지에 있으며, 이 모듈은 `python -m bcsfekorea` 로도
실행할 수 있게 하는 별칭입니다.
"""

from bcsfe import __version__, run

__all__ = ["__version__", "run"]
