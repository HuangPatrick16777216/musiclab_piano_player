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
    def __init__(self):
        self.midi_paths = []

    def play(self):
        time.sleep(2)

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
                    if msg.volume == 0:
                        notes.append((note, starts[note], curr_time))
                    else:
                        starts[note] = curr_time

        print(notes)
