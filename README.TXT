sudo apt-get update
sudo apt-get install libopencv-dev
git clone https://github.com/alyssaq/face_morpher.git
cd face_morpher
pip3 install -r requirements.txt
pip3 install opencv-python
python3 setup.py install
sudo apt-get install ffmpeg
pip3 install ffmpy