import argparse
import os
import subprocess
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from glob import glob
from os import path

import numpy as np
from tqdm import tqdm

from models import audio

parser = argparse.ArgumentParser()
parser.add_argument("--process_num", type=int, default=6)  # number of process to preprocess the audio
parser.add_argument("--data_root", type=str, help="Root folder of the LRS2 dataset", required=True)
parser.add_argument("--out_root", help="output audio root", required=True)
args = parser.parse_args()
sample_rate = 16000  # 16000Hz
template = "ffmpeg -loglevel panic -y -i {} -strict -2 {}"


def process_audio_file(vfile, args):
    vidname = os.path.basename(vfile).split(".")[0]
    dirname = vidname.split("_")[0]

    fulldir = path.join(args.out_root, dirname, vidname)
    os.makedirs(fulldir, exist_ok=True)
    wavpath = path.join(fulldir, "audio.wav")

    command = template.format(vfile.replace(" ", r"\ "), wavpath.replace(" ", r"\ "))
    subprocess.run(command, shell=True)
    wav = audio.load_wav(wavpath, sample_rate)
    orig_mel = audio.melspectrogram(wav).T
    np.save(path.join(fulldir, "audio"), orig_mel)


def mp_handler_audio(job):
    vfile, args = job
    try:
        process_audio_file(vfile, args)
    except KeyboardInterrupt:
        exit(0)
    except Exception:
        traceback.print_exc()


def main(args):
    print("looking up paths.... from", args.data_root)
    filelist = glob(path.join(args.data_root, "*/*.wav"))

    jobs = [(vfile, args) for vfile in filelist]
    p_audio = ProcessPoolExecutor(args.process_num)
    futures_audio = [p_audio.submit(mp_handler_audio, j) for j in jobs]

    _ = [r.result() for r in tqdm(as_completed(futures_audio), total=len(futures_audio))]
    print("complete, output to", args.out_root)


if __name__ == "__main__":
    main(args)
