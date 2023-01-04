#!/bin/sh

cd /RusticiEngine/Installer
java -Dlogback.configurationFile=logback.xml -cp "lib/*" RusticiSoftware.ScormContentPlayer.Logic.Upgrade.ConsoleApp mysql "jdbc:mysql://$DB_HOST/RusticiEngineDB?user=$DB_USER&password=$DB_PASSWORD|com.mysql.cj.jdbc.Driver"
catalina.sh run