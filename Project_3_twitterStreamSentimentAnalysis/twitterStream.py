from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import matplotlib.pyplot as plt

def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")
   
    counts = stream(ssc, pwords, nwords, 100)
    make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    # YOUR CODE HERE
    pCounts = []
    nCounts = []
    for i in counts:
      if i != []:
        pCounts.append(i[0][1])
        nCounts.append(i[1][1])
    countPlot = plt.figure()
    a = countPlot.add_subplot(1,1,1)
    a.plot(pCounts, marker="o", label="positive", color="blue")
    a.plot(nCounts, marker="o", label="negative", color="green")
    a.set_xlim([-1, len(pCounts)])
    a.xaxis.set_ticks(range(0, len(pCounts)))
    a.set_xlabel("Time-Step")
    a.set_ylabel("Word-Count")
    plt.legend(loc="upper left")
    plt.show()



def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """
    # YOUR CODE HERE
    with open(filename, "r") as ifile:
      return set([line.strip() for line in ifile])



def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1])

    # Each element of tweets will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).
    # YOUR CODE HERE
    words = tweets.flatMap(lambda l: l.split()).map(lambda w: w.lower())
    data = {word:"positive" for word in pwords}
    for word in nwords:
      data[word]="negative"
    
    pnWords = words.filter(lambda w: w in data).map(lambda w: (data[w],1))
    pnWords = pnWords.reduceByKey(operator.add)
    
    def updateFunc(new_values, global_sum):
      return sum(new_values) + (global_sum or 0)
    pnTotals = pnWords.updateStateByKey(updateFunc)
    pnTotals.pprint()
    
    
    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]
    counts = []
    pnWords.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))
    
    ssc.start()                         # Start the computation
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)

    return counts


if __name__=="__main__":
    main()
