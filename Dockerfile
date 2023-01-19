FROM tomcat:8.0-jre8

WORKDIR /rustici

# Copy the WAR file in the webapps directory
ADD resources/rustici/RusticiEngine/RusticiEngine.war /usr/local/tomcat/webapps

# Copy the properties file in the Tomcat lib directory
ADD config/RusticiEngineSettings.properties /usr/local/tomcat/lib

# Copy the customised installer (with the mySQL JAR) into the container
ADD resources/rustici/RusticiEngine/Installer /RusticiEngine/Installer

# Tomcat also needs access to the MySQL connector JAR
RUN cp /RusticiEngine/Installer/lib/mysql-connector-*.jar /usr/local/tomcat/lib

# Add the installer script
ADD config/installScript.sh .

# Provide permissions to the installer script and ensure LF endings
RUN sed -i 's/\r$//' installScript.sh  && \  
        chmod +x installScript.sh

EXPOSE 8080

# The 'run command', will install Rustici onto the database and start catalina
ENTRYPOINT ["./installScript.sh"]