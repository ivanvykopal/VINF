from pyspark import SparkConf,SparkContext
from pyspark.sql import SparkSession
from parser import parse_line, get_non_types
import sys
from io import open

# argumenty <input_file> <output_file> <spark_executor_uri>

if len(sys.argv) < 3:
    print('Nespravny pocet argumentov')
    exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

#spark_executor_memory = "512m"          # tu zmenit hodnotu
#spark_driver_memory = "512m"            # tu zmenit hodnotu
#spark_cores = "16"                      # tu zmenit hodnotu

if len(sys.argv) == 4:
    spark_executor = sys.argv[3]
else:
    spark_executor = None

if spark_executor:
    spark = (
                SparkSession.builder
                    .appName("Freebase parser")
                    .config("spark.executor.uri", spark_executor)
                    #.config("spark.executor.memory", spark_executor_memory)
                    #.config("spark.driver.memory", spark_driver_memory)
                    #.config("spark.cores.max", spark_cores)
                    .getOrCreate()
            )
else:
    spark = (
                SparkSession.builder
                    .appName("Freebase parser")
                    #.config("spark.executor.memory", spark_executor_memory)
                    #.config("spark.driver.memory", spark_driver_memory)
                    #.config("spark.cores.max", spark_cores)
                    .getOrCreate()
            )

freebase_file = spark.sparkContext.textFile(input_file, use_unicode=False)

non_types = get_non_types()
data = (
    freebase_file.map(lambda line: parse_line(line, non_types))
                .filter(lambda x: (x is not None))
                .reduceByKey(lambda a,b: a + b)
                .filter(lambda x: (x[1].title is not None))
                .map(lambda x: x[1].to_string())
                .distinct()
    )

data.saveAsTextFile(output_file)