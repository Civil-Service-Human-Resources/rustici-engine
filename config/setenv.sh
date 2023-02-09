if [ ! -z "$APPLICATIONINSIGHTS_CONNECTION_STRING" ]
then
	CATALINA_OPTS="$CATALINA_OPTS -javaagent:$APP_INSIGHTS_JAR"
fi

CATALINA_OPTS="$CATALINA_OPTS -Dlogback.configurationFile=/RusticiEngine/Installer/logback.xml"