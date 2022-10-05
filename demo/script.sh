# deploy queue
docker pull redis:7.0.4
docker run --name my-first-redis -dp 6379:6379 redis:7.0.4

# run agent
nohup python3 recorder.py > /dev/null 2>&1 &
