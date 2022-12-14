#!/bin/sh

cd /RusticiEngine/Installer
java -Dlogback.configurationFile=logback.xml -cp "lib/*" RusticiSoftware.ScormContentPlayer.Logic.Upgrade.ConsoleApp mysql "jdbc:mysql://db:3306/RusticiEngineDB?user=root&password=password1|com.mysql.jdbc.Driver"
catalina.sh run