FROM tomcat:9

ARG RUSTICI=RusticiEngine_java_engine_21.1.19.412
ARG MYSQL=mysql-connector-j-8.0.31

# Install packages

RUN apt update
RUN apt install -y unzip

# Copy var declarations
ADD vars.sh vars.sh

# Copy the Installer:
ADD resources/${RUSTICI}.zip /
RUN unzip /${RUSTICI}.zip -d /

# Copy the WAR file in the webapps directory
RUN cp /RusticiEngine/RusticiEngine.war /usr/local/tomcat/webapps

# Copy the properties file in the Tomcat lib directory
RUN cp /RusticiEngine/Config/RusticiEngineSettings.properties /usr/local/tomcat/lib

# Copy the MySQL JDBC Connector:
ADD resources/${MYSQL}.zip /
RUN unzip /${MYSQL}.zip -d /
RUN cp  /${MYSQL}/${MYSQL}.jar /RusticiEngine/Installer/lib

# Add the initialisation script:
ADD resources/rusticiInit.sh /bin

EXPOSE 8080

# Run the initialisation script:
CMD ["rusticiInit.sh"]