@echo off
setlocal

rem ============================================================
rem  compile_game.bat - Nand2Tetris Project 9 build script
rem  Compiles the Space Invaders Jack files and (optionally)
rem  opens the VM Emulator.
rem  If you ever move the folders, just update the 2 paths below.
rem ============================================================

set "TOOLS=C:\Users\simao\OneDrive\Documents\first degree\school\forth year\second semester\NAND to Tetris\nand2tetris\tools"
set "GAME=C:\Users\simao\OneDrive\Documents\first degree\school\forth year\second semester\NAND to Tetris\nand2tetris\projects\09\space invaders"

rem --- the nand2tetris tools must be run from inside the tools dir ---
pushd "%TOOLS%"
echo Compiling Jack files in:
echo   %GAME%
echo.
call JackCompiler.bat "%GAME%"
set ERR=%ERRORLEVEL%
popd

echo.
if %ERR% NEQ 0 (
    echo ============================================
    echo  Compilation FAILED - see the errors above.
    echo ============================================
) else (
    echo ============================================
    echo  Done! .vm files were written to the game folder.
    echo ============================================
    echo.
    choice /M "Open the VM Emulator now"
    if not errorlevel 2 (
        pushd "%TOOLS%"
        start "" VMEmulator.bat
        popd
    )
)

echo.
pause
