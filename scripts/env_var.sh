export HADOOP_HOME=/usr/lib/hadoop
export HADOOP_HDFS_HOME=$HADOOP_HOME
#source ${HADOOP_HOME}/libexec/hadoop-config.sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${JAVA_HOME}/jre/lib/amd64/server
export CLASSPATH=$(${HADOOP_HOME}/bin/hadoop classpath --glob)