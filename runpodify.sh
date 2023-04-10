pip install runpod
wget https://raw.githubusercontent.com/therealadityashankar/replicate2runpod/main/runpod_infer.py
wget https://raw.githubusercontent.com/therealadityashankar/replicate2runpod/main/test_input.json
python -m cog.server.http &
python runpod_infer.py