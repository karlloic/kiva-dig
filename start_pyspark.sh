SPARK_DIR="spark-2.0.1-bin-hadoop2.7"
SPARK_URL="http://apache.claz.org/spark/spark-2.0.1/spark-2.0.1-bin-hadoop2.7.tgz"

if [ ! -d "$SPARK_DIR" ]; then
    echo "Downloading Spark distribution..."
    wget "$SPARK_URL" -O - | tar xzf -
fi

PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook" "./$SPARK_DIR/bin/pyspark"
