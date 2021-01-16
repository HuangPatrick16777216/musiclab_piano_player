# Musiclab Piano Player
This project is neither related to nor sponsored by [Musiclab](https://musiclab.chromeexperiments.com/Shared-Piano/).

## How To Use
1. Go to [Musiclab Shared Piano](https://musiclab.chromeexperiments.com/Shared-Piano/).
2. Follow this code format:
```python
from version1 import Player

player = Player()
player.midi_paths.append("midi1.mid")
player.midi_paths.append("midi2.mid")
player.play(init_pause=1, key_pause=0, speed=1)
```
