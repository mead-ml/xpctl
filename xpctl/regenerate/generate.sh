# for some reason if you want to regenerate the server and client. Not recommended 
rm -rf ../xpserver
rm -rf ../xpclient
wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.5/swagger-codegen-cli-2.4.5.jar -O swagger-codegen-cli.jar
JAR=swagger-codegen-cli.jar
java -jar ${JAR} generate \
  -i ../xpctl.yaml \
  -l python-flask \
  -o server \
  -D supportPython2=true \
  -D packageName=xpserver

mv server/xpserver ../
rm -rf server
java -jar ${JAR} generate \
  -i ../xpctl.yaml \
  -l python \
  -o client \
  -D packageName=xpclient

mv client/xpclient ../
rm -rf client

#cp static/server.py ../xpserver/server.py
#cp static/version.py ../xpserver/version.py
#cp static/setup.py ../xpserver/setup.py
cp static/configuration.py ../xpclient/configuration.py

