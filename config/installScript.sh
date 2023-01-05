#!/bin/sh

cd /RusticiEngine/Installer
java -Dlogback.configurationFile=logback.xml -cp "lib/*" RusticiSoftware.ScormContentPlayer.Logic.Upgrade.ConsoleApp mysql "$CONNECTION_STRING"
catalina.sh run