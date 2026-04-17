import time
import board
import analogio
import busio
import audiocore
import adafruit_pcm51xx
import audiobusio

# Initialize I2C
i2c = board.I2C()

# Initialize PCM5122
print("Initializing PCM5122...")
dac = adafruit_pcm51xx.PCM51XX(i2c)
print("Found PCM5122!")
dac.mute = False

# Initialize potentiometer on A2
pot = analogio.AnalogIn(board.A2)

# Initialize I2S audio
audio = audiobusio.I2SOut(board.D9, board.D10, board.D11)

# Load and play WAV on loop
wav = audiocore.WaveFile("StreetChicken.wav")
audio.play(wav, loop=True)

def pot_to_db(raw):
    # Map 0–65535 to -60.0 dB (near silent) to 0.0 dB (full volume)
    return -60.0 + (raw / 65535.0) * 60.0

last_db = None

while True:
    raw = pot.value                  # 0–65535
    db = round(pot_to_db(raw), 1)   # one decimal place

    # Only update DAC if value changed, avoids unnecessary I2C writes
    if db != last_db:
        dac.volume_db = (db, db)
        print(f"Volume: {db} dB")
        last_db = db

    time.sleep(0.05)
