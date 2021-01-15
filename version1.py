#  ##### BEGIN GPL LICENSE BLOCK #####
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import time
import pyautogui
import mido


class Player:
    keys = list("awsedftgyhuj")

    def __init__(self):
        self.midi_paths = []

    def note_to_info(self, note):
        key_ind = note + 9
        key = self.keys[key_ind % 12]
        octave = key_ind // 12
        return (key, octave)

    def play(self, init_pause=1, key_pause=0.001, speed=1):
        pyautogui.PAUSE = key_pause
        time.sleep(init_pause)

        notes = []
        for path in self.midi_paths:
            midi = mido.MidiFile(path)

            curr_time = 0
            tempo = 500000

            starts = [False] * 88

            for msg in midi.tracks[0]:
                curr_time += msg.time / midi.ticks_per_beat * tempo / 1000000
                if msg.is_meta and msg.type == "set_tempo":
                    tempo = msg.tempo
                elif not msg.is_meta and msg.type == "note_on":
                    note = msg.note - 21
                    if msg.velocity == 0:
                        notes.append([note, starts[note], curr_time, "NOT_PLAYED"])
                    else:
                        starts[note] = curr_time

        notes = sorted(notes, key=(lambda x: x[1]))

        curr_octave = 4
        time_start = time.time()
        while True:
            elapsed = time.time() - time_start
            elapsed *= speed

            for i, info in enumerate(notes):
                note, start, end, state = info

                if state == "NOT_PLAYED" and elapsed >= start:
                    key, octave = self.note_to_info(note)
                    oct_diff = abs(octave - curr_octave)

                    if octave > curr_octave:
                        pyautogui.typewrite("x"*oct_diff)
                    elif octave < curr_octave:
                        pyautogui.typewrite("z"*oct_diff)

                    pyautogui.typewrite(key)
                    notes[i][3] = "PLAYED"
                    curr_octave = octave

            if all([x[3]=="PLAYED" for x in notes]):
                break
