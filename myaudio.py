import sys, os
import threading as TH
import glob
import subprocess
from scipy.io import wavfile
import scipy.signal as sps
import numpy as np


def __voice_send(user_id: int, file_path: str, func_msg, message, st:str):
    pathdir = 'voice/' + str(user_id)
    if not os.path.exists(pathdir) and not os.path.isdir(pathdir):
        os.mkdir(pathdir)
    files = glob.glob(pathdir + '/audio_message_*')
    out_path = pathdir + '/%d-audio_message_%d.wav' % (user_id, len(files))
    print(os.path.realpath(file_path), os.path.realpath(out_path))
    process = subprocess.run([
        'C:\\Program Files\\ffmpeg-20200720-43a08d9-win64-static\\bin\\ffmpeg.exe',
        '-i',
        os.path.realpath(file_path),
        os.path.realpath(out_path)]
    )
    new_rate = 16000
    sr, data = wavfile.read(out_path)
    print(len(data))
    number_of_samples = round(len(data) * float(new_rate) / sr)
    data = sps.resample(data, number_of_samples)
    wavfile.write(out_path, new_rate, np.array(data, dtype=np.int16))
    os.remove(file_path)
    func_msg(message.chat.id, st + 'Saved to "%s"'%out_path)


def voice_send(user_id: int, file_path: str, func_msg, message, st:str):
    thread = TH.Thread(target=__voice_send, args=(user_id, file_path, func_msg, message, st))
    thread.start()
