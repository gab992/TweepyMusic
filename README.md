# TweepyMusic  
For this project, I use the Tweepy python library to live stream tweets into a python script given a user-chosen hashtag. I then use some standard NLP techniques and Google News word embeddings to convert the text information from tweets into numeric values. The word embedding vectors for each tweet are manipulated and piped into SonicPi via OSC to trigger synth sounds and drum hits. The logic connecting the word embedding vectors and the sound is not particularly meaningful and is a result of experimentation.  

# Music  
To hear what this project sounds like, you can listen to a recording of the twitter stream with the hashtag "BLM" [here](https://soundcloud.com/glorptron/tweepy-music-blm)

# Included Files  
**twitter_instrument.py**: Python script to stream tweets, convert them to word embedding vectors, and send these vectors as OSC messages.  
**tweepy_sonicpy.rb**: SonicPi code (very similar to Ruby) for receiving the word embedding vectors via OSC and making music with them! This can be run from SonicPi using the following line of code...  
'''Ruby
run_file get(:rfpath)+"tweepy_sonicpy.rb"
'''  

# Necessary Tools For Replication  
In order to run this project on your own, you need (in addition to the files in this repository) the following...

- [SonicPi](https://sonic-pi.net/)  
- [Twitter API Credentials](https://developer.twitter.com/en/docs/getting-started)  
- The following python libraries:  
  - Tweepy  
  - Numpy  
  - NLTK  
  - Gensim  
  - pythonosc  
  - sys  
  - os
  - pickle  
  - re  

# Replication Steps  
- Open twitter_instrument.py in a text editor and add your twitter api credentials in lines 19-22.  
- Open SonicPi and either copy and paste tweepy_sonicpi.rb into a buffer and run it, or run a buffer with the line of code specified in the earlier description of tweepy_sonicpi.rb.  
- Run twitter_instrument.py from the command line using "python twitter_instrument.py" and follow the command line prompts!  

**note** the first run will take a long time because it will save the word embeddings as a pickle file in the directory you are working in. On subsequent runs the code will just use the pickle file and thus will run much faster.  
