@echo off
chcp 65001 >nul
setlocal
title 냥코 대전쟁 세이브 에디터 (한국어판)
cd /d "%~dp0"

set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

rem --- 파이썬 찾기 ---
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (
    where python >nul 2>nul && set "PY=python"
)
if not defined PY (
    echo.
    echo [오류] 파이썬이 설치되어 있지 않습니다.
    echo.
    echo  1. https://www.python.org/downloads/ 에서 파이썬을 설치하세요.
    echo  2. 설치 화면 맨 아래 "Add python.exe to PATH" 를 꼭 체크하세요.
    echo  3. 설치가 끝나면 이 파일을 다시 실행하세요.
    echo.
    start "" "https://www.python.org/downloads/"
    pause
    exit /b 1
)

rem --- 필요한 라이브러리 설치 (처음 한 번만) ---
if not exist "data\.deps_ok" (
    echo 처음 실행이라 필요한 라이브러리를 설치합니다. 잠시만 기다려 주세요...
    %PY% -m pip install --disable-pip-version-check -q -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [오류] 라이브러리 설치에 실패했습니다. 인터넷 연결을 확인하고 다시 실행해 주세요.
        pause
        exit /b 1
    )
    if not exist "data" mkdir "data"
    echo ok> "data\.deps_ok"
)

rem --- 에디터 실행 (설정과 데이터는 이 폴더의 data 안에 저장됨) ---
set "PYTHONPATH=%~dp0src"
%PY% -m bcsfe --data-dir "%~dp0data" --config-path "%~dp0data\config.yaml" %*

echo.
pause
