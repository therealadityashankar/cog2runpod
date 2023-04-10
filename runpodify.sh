pip install runpod

wget .../runpod_infer.py
wget .../test_input.json

python -m cog.server.http &
python runpod_infer.py