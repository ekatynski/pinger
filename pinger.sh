mkdir -p output
ping -w60 google.com >> output/google_ping.txt &
ping -w60 stackoverflow.com >> output/so_ping.txt &
ping -w60 npr.org >> output/npr_ping.txt &
ping -w60 nasa.gov >> output/nasa_ping.txt &
ping -w60 umich.edu >> output/umich_ping.txt &

