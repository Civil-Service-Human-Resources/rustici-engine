FROM tomcat:9.0.105-jdk8-corretto-al2

WORKDIR /rustici

# ENV CATALINA_HOME="/usr/local/tomcat"
ENV APP_INSIGHTS_VERSION="3.4.9"
ENV APP_INSIGHTS_VERSION_JAR="applicationinsights-agent-$APP_INSIGHTS_VERSION.jar"
ENV APP_INSIGHTS_JAR="/rustici/appInsights/$APP_INSIGHTS_VERSION_JAR"

RUN rm -rf ${CATALINA_HOME}/webapps/* && \
	rm -rf ${CATALINA_HOME}/server/webapps/*

###
# Security enhanced web.xml
###
COPY config/web.xml ${CATALINA_HOME}/conf/

###
# Security enhanced server.xml
###
COPY config/server.xml ${CATALINA_HOME}/conf/

# Copy the WAR file in the webapps directory
ADD resources/rustici/RusticiEngine/RusticiEngine.war /usr/local/tomcat/webapps

# Copy the properties file in the Tomcat lib directory
ADD config/RusticiEngineSettings.properties /usr/local/tomcat/lib

# Copy the customised installer (with the mySQL JAR) into the container
ADD resources/rustici/RusticiEngine/Installer /RusticiEngine/Installer

# Logger
ADD config/logback.xml /RusticiEngine/Installer/

# Tomcat also needs access to the MySQL connector JAR
RUN cp /RusticiEngine/Installer/lib/mysql-connector-*.jar /usr/local/tomcat/lib

# Application insights
ADD https://github.com/microsoft/ApplicationInsights-Java/releases/download/$APP_INSIGHTS_VERSION/$APP_INSIGHTS_VERSION_JAR $APP_INSIGHTS_JAR
ADD config/setenv.sh /usr/local/tomcat/bin


# Add the installer script
ADD config/installScript.sh .

# Provide permissions to the installer script and ensure LF endings
RUN sed -i 's/\r$//' installScript.sh  && \  
        chmod +x installScript.sh

EXPOSE 8000

# The 'run command', will install Rustici onto the database and start catalina
ENTRYPOINT ["./installScript.sh"]