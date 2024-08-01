Prototype for Arena Shmup mobile concept using kivy/python

Testing performance of kivy with somewhat complex game concepts.

Added some free graphics found on itch.io for testing purposes. Art assets not final.

Version 0.0.1
- Battle scene that handles base combat
- Player ship with WASD movement controls
- Player automatically aims and fires at closest enemy
- Bullets are pooled in inactive group, then activated and repositioned upon player firing
- 3 layers of parallax background - Background recycles images to create pseudo looping effect

- Issues: Current version stutters every 10-15 seconds with massive FPS drops, even without any changes happening in game that would cause stuttering effect.
- Disabling parallax background, bullets, and enemy still contains stuttering although weaker
