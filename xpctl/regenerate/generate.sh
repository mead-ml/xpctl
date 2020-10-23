# for some reason if you want to regenerate the server and client. Not recommended 
cp ../xpserver/__main__.py static/__main__.py
#cp ../xpserver/controllers/xpctl_controller.py static/xpctl_controller_back.py
cp ../xpclient/configuration.py static/configuration.py
rm -rf ../xpserver
rm -rf ../xpclient
wget http://repo.jenkins-ci.org/public/io/swagger/swagger-codegen-cli/2.4.5/swagger-codegen-cli-2.4.5.jar -O swagger-codegen-cli.jar
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

cp static/__main__.py ../xpserver/__main__.py
#cp static/xpctl_controller.py ../xpserver/controllers/xpctl_controller.py
cp static/configuration.py ../xpclient/configuration.py

