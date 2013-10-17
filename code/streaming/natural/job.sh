#!/bin/bash

MAPPER=/home/hadoop/tutorial/code/streaming/natural/mapper.py
REDUCER=/home/hadoop/tutorial/code/streaming/natural/reducer.py

$HADOOP_PREFIX/bin/hadoop jar $HADOOP_PREFIX/contrib/streaming/hadoop-*streaming*.jar \
    -file $MAPPER -file $REDUCER \
    -mapper $MAPPER -reducer $REDUCER -combiner $REDUCER \
    -input $1 -output $2
