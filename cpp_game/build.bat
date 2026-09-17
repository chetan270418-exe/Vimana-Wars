@echo off
setlocal
cd /d "%~dp0"

echo ========================================================
echo   BUILDING VIMANA WARS // NATIVE C++ DESKTOP ENGINE
echo ========================================================

if not exist bin mkdir bin

set CC=..\tools\w64devkit\bin\gcc.exe
set CXX=..\tools\w64devkit\bin\g++.exe

if not exist "%CXX%" set CC=gcc.exe
if not exist "%CXX%" set CXX=g++.exe

set INCLUDES=-Iinclude -I..\tools\raylib-6.0_win64_mingw-w64\include
set LIB_DIRS=-L..\tools\raylib-6.0_win64_mingw-w64\lib
set LIBS=-lraylib -lopengl32 -lgdi32 -lwinmm -lwinhttp -lws2_32
set CFLAGS=-O2
set CXXFLAGS=-std=c++20 -O2 -Wall -Wno-missing-braces -Wno-unused-variable

if not exist bin\sqlite3.o (
    echo Compiling SQLite3 C engine...
    "%CC%" %CFLAGS% -c src\sqlite3.c -o bin\sqlite3.o
)

echo Compiling C++ source files...
"%CXX%" %CXXFLAGS% src\main.cpp bin\sqlite3.o %INCLUDES% %LIB_DIRS% %LIBS% -o bin\VimanaWars.exe

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================================
    echo   [SUCCESS] Binary generated at bin\VimanaWars.exe!
    echo ========================================================
    echo.
) else (
    echo.
    echo [FAIL] Compilation failed with error code %ERRORLEVEL%.
    exit /b %ERRORLEVEL%
)

endlocal
