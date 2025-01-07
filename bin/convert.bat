@echo off
:: Cambiamos la codificación a UTF8
chcp 65001

setlocal enabledelayedexpansion

for %%f in (data\*.xlsx) do (
    for %%s in ("palabras" "no palabras") do (
        :: Generamos un hash MD5 por cada fichero
        for /f "tokens=1 delims= " %%h in ('certutil -hashfile "%%f" MD5 ^| find /v "hash" ^| find /v "CertUtil"') do (
            set "hash=%%h"
            :: Eliminamos los espacios en el nombre de las páginas
            set "sheet=%%s"
            set "sheet=!sheet: =!"
            in2csv -f xlsx -I --skip-lines 1 --sheet %%s "%%f" > "!hash!_!sheet!.csv"
        )
    )
)

move *_palabras.csv converted
move *_nopalabras.csv converted

endlocal