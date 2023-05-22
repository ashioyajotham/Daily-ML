import subprocess

scraping_path = '.\src\scraping.py'
spotify_streaming_data_path = '.\src\spotify-streaming-data.py'

subprocess.run(['python', scraping_path])
subprocess.run(['python', spotify_streaming_data_path])