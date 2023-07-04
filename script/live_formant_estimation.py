import pyaudio
import os
import sys
import wave
import praat_formants_python as pfp
import numpy as np

demo_path = sys.argv

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.5


WAVE_OUTPUT_FILENAME = "script/buf.wav"
WAVE_OUTPUT_FILENAME = os.path.join(demo_path[1], WAVE_OUTPUT_FILENAME)

OUT_FILE = "script/out"
OUT_FILE = os.path.join(demo_path[1], OUT_FILE)

DISTANCE_THRESHOLD = 200


VOWEL_COORDINATES = [[730, 1090], # aa
                     [270, 2290], # ii
                     [300, 870]]  # oo


aud_port = pyaudio.PyAudio()
stream = aud_port.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
); print("* recording")




def measure_formants_pfp(audio_path: str, start_sec: float, end_sec: float) -> dict:
    formants: list = pfp.formants_at_interval(
        audio_path, start_sec, end_sec, maxformant=5500, winlen=1, preemph=50
    )

    formants_mean = formants.mean(axis=0)
    formants_mean = list(formants_mean)[1:]  # skip time
    formants_mean = np.round(formants_mean, 2)  # round

    # formants_median = np.median(formants, axis=0)
    # formants_median = list(formants_median)[1:]  # skip time
    # formants_median = np.round(formants_median, 2)  # round

    return formants_mean[:2]

def main():
    i = 0
    frames = []
    formants_array = VOWEL_COORDINATES.copy()
    while True:
        try:
            data = stream.read(CHUNK)
            frames.append(data); i += 1

            if i % np.floor(RATE / CHUNK * RECORD_SECONDS) == 0:
                with wave.open(WAVE_OUTPUT_FILENAME, "wb") as wf:
                    wf.setframerate(RATE)
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(aud_port.get_sample_size(FORMAT))
                    wf.writeframes(b"".join(frames))
                    frames = []
                
                i = 0


                pfp.clear_formant_cache()
                # [F1, F2]
                cur_formant = measure_formants_pfp(WAVE_OUTPUT_FILENAME, 0, RECORD_SECONDS)

                is_inbound = lambda o, p: np.linalg.norm(o - p) < DISTANCE_THRESHOLD

                if is_inbound(VOWEL_COORDINATES[0], cur_formant):
                    formants_array[0] = cur_formant

                elif is_inbound(VOWEL_COORDINATES[1], cur_formant):
                    formants_array[1] = cur_formant

                elif is_inbound(VOWEL_COORDINATES[2], cur_formant):
                    formants_array[2] = cur_formant

                else: continue

                np.save(OUT_FILE, formants_array)

                print("formant array\n", formants_array)

        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            aud_port.terminate()
            print("* done recording")

            break

if __name__ == "__main__":
    main()