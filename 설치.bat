@echo off
chcp 65001 >nul
setlocal
title 냥코 대전쟁 세이브 에디터 (한국어판) 설치
cd /d "%~dp0"

set "PY="
where python >nul 2>nul && set "PY=python"
if not defined PY (
    where py >nul 2>nul && set "PY=py -3"
)
if not defined PY (
    echo [오류] 파이썬이 설치되어 있지 않습니다.
    echo https://www.python.org/downloads/ 에서 설치하고, "Add python.exe to PATH" 를 꼭 체크하세요.
    start "" "https://www.python.org/downloads/"
    pause
    exit /b 1
)

echo 한국어판(bcsfekorea)을 설치합니다. 잠시만 기다려 주세요...
echo (원본 bcsfe 가 설치되어 있으면 먼저 제거합니다)
%PY% -m pip uninstall -y bcsfe >nul 2>nul
echo.
%PY% -m pip install --disable-pip-version-check -r requirements.txt
%PY% -m pip install --disable-pip-version-check --force-reinstall --no-deps "%~dp0."
if errorlevel 1 (
    echo.
    echo [오류] 설치에 실패했습니다. 위의 오류 메시지를 확인해 주세요.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  설치 완료! 이제부터는 명령 프롬프트에서
echo.
echo      python -m bcsfe
echo.
echo  만 입력하면 한국어판 에디터가 실행됩니다.
echo ============================================================
pause
