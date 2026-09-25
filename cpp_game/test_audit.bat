@echo off
setlocal
cd /d "%~dp0"

set CXX=..\tools\w64devkit\bin\g++.exe
if not exist "%CXX%" set CXX=g++.exe
set CC=..\tools\w64devkit\bin\gcc.exe
if not exist "%CC%" set CC=gcc.exe
set RAYLIB=..\tools\raylib-6.0_win64_mingw-w64
if not exist bin mkdir bin
if not exist bin\sqlite3.o "%CC%" -O2 -c src\sqlite3.c -o bin\sqlite3.o
if errorlevel 1 exit /b %ERRORLEVEL%

"%CXX%" -std=c++20 -O2 -Wall -Wno-missing-braces -Wno-unused-variable ^
  -Iinclude -I"%RAYLIB%\include" tests\audit_smoke.cpp ^
  bin\sqlite3.o -L"%RAYLIB%\lib" -lraylib -lopengl32 -lgdi32 -lwinmm -lwinhttp -lws2_32 ^
  -o bin\audit_smoke.exe
if errorlevel 1 exit /b %ERRORLEVEL%

bin\audit_smoke.exe
exit /b %ERRORLEVEL%
