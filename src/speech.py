import os
import re
import subprocess
import tempfile
import threading
from urllib.parse import unquote


class Speech:
    """Neural TTS (Piper) on the USB speaker, with a slightly scared delivery."""

    # Relative to repo root (parent of src/)
    PIPER_BIN = os.path.join("..", "tools", "piper", "piper")
    VOICES = {
        "male": os.path.join("..", "voices", "en_US-ryan-medium.onnx"),
        "female": os.path.join("..", "voices", "en_US-amy-medium.onnx"),
    }

    # Threatened / terrified delivery: rushed, high, shaky voice
    PIPER_LENGTH_SCALE = "0.78"   # speak faster (panicked)
    PIPER_NOISE_SCALE = "0.95"    # less stable tone
    PIPER_NOISE_W = "1.05"
    SOX_SCARED = {
        # pitch in cents, tempo>1 = faster, tremolo freq/depth = voice quiver
        "male": [
            "pitch", "220",
            "tempo", "1.12",
            "tremolo", "8", "40",
            "gain", "-1",
            "bass", "-2",
            "treble", "3",
        ],
        "female": [
            "pitch", "280",
            "tempo", "1.14",
            "tremolo", "9", "45",
            "gain", "-1",
            "bass", "-3",
            "treble", "4",
        ],
    }

    def __init__(self):
        self._base = os.path.abspath(os.path.dirname(__file__))
        self._proc = None
        self._device = self._find_usb_device()
        self._set_volume(95)
        self._piper = os.path.normpath(os.path.join(self._base, self.PIPER_BIN))
        self._voice_paths = {
            name: os.path.normpath(os.path.join(self._base, path))
            for name, path in self.VOICES.items()
        }

    def _find_usb_device(self):
        """Prefer the Jieli USB speaker; fall back to any USB Audio card."""
        try:
            out = subprocess.check_output(["aplay", "-l"], text=True, stderr=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "plughw:3,0"

        preferred = None
        usb_fallback = None
        for line in out.splitlines():
            m = re.match(r"^card (\d+): .*\[([^\]]+)\].*device (\d+):", line)
            if not m:
                continue
            card, name, device = m.group(1), m.group(2), m.group(3)
            label = name.lower()
            if "uacdemo" in label or "jieli" in label:
                preferred = f"plughw:{card},{device}"
                break
            if "usb" in label or "usb-audio" in line.lower():
                usb_fallback = f"plughw:{card},{device}"

        return preferred or usb_fallback or "plughw:3,0"

    def _card_number(self):
        m = re.search(r"plughw:(\d+),", self._device)
        return m.group(1) if m else "3"

    def _set_volume(self, percent):
        try:
            subprocess.run(
                ["amixer", "-c", self._card_number(), "set", "PCM", f"{percent}%", "unmute"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            pass

    def stop(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        self._proc = None
        subprocess.run(
            ["pkill", "-f", "aplay -D plughw"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return "SPEAK STOPPED"

    def status(self):
        busy = self._proc is not None and self._proc.poll() is None
        engine = "piper" if os.path.isfile(self._piper) else "missing"
        return f"device={self._device} engine={engine} speaking={'yes' if busy else 'no'}"

    def speak(self, voice, text):
        voice = (voice or "").lower().strip()
        if voice not in self._voice_paths:
            return f"Unknown voice '{voice}'. Use male or female."

        text = unquote(text or "").strip()
        if not text:
            return "No text to speak."
        if len(text) > 500:
            text = text[:500]

        model = self._voice_paths[voice]
        if not os.path.isfile(self._piper):
            return f"Piper binary missing at {self._piper}"
        if not os.path.isfile(model):
            return f"Voice model missing at {model}"

        self.stop()
        self._device = self._find_usb_device()
        self._set_volume(95)

        raw_path = None
        out_path = None
        try:
            fd, raw_path = tempfile.mkstemp(suffix=".wav", prefix="carpi_tts_raw_")
            os.close(fd)
            fd, out_path = tempfile.mkstemp(suffix=".wav", prefix="carpi_tts_")
            os.close(fd)

            # Piper needs its shared libs from the tools/piper directory
            env = os.environ.copy()
            piper_dir = os.path.dirname(self._piper)
            env["LD_LIBRARY_PATH"] = piper_dir + (":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")

            gen = subprocess.run(
                [
                    self._piper,
                    "--model", model,
                    "--length_scale", self.PIPER_LENGTH_SCALE,
                    "--noise_scale", self.PIPER_NOISE_SCALE,
                    "--noise_w", self.PIPER_NOISE_W,
                    "--sentence_silence", "0.15",
                    "--output_file", raw_path,
                    "--quiet",
                ],
                input=text + "\n",
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )
            if gen.returncode != 0 or not os.path.isfile(raw_path) or os.path.getsize(raw_path) == 0:
                err = (gen.stderr or gen.stdout or "piper failed").strip()
                return f"TTS failed: {err}"

            # Scared coloring via sox (fallback to raw wav if sox missing)
            sox_fx = self.SOX_SCARED.get(voice, self.SOX_SCARED["female"])
            scared = subprocess.run(
                ["sox", raw_path, out_path] + sox_fx,
                check=False,
                capture_output=True,
                text=True,
            )
            play_path = out_path if scared.returncode == 0 and os.path.getsize(out_path) > 0 else raw_path

            self._proc = subprocess.Popen(
                ["aplay", "-D", self._device, "-q", play_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            def _cleanup(raw=raw_path, out=out_path, proc=self._proc):
                try:
                    proc.wait()
                finally:
                    for path in (raw, out):
                        try:
                            if path:
                                os.remove(path)
                        except OSError:
                            pass

            threading.Thread(target=_cleanup, daemon=True).start()
            return f"SPEAKING ({voice}): {text}"
        except FileNotFoundError as e:
            for path in (raw_path, out_path):
                if path:
                    try:
                        os.remove(path)
                    except OSError:
                        pass
            return f"TTS tool missing: {e}"
        except Exception as e:
            for path in (raw_path, out_path):
                if path:
                    try:
                        os.remove(path)
                    except OSError:
                        pass
            return f"TTS error: {e}"
