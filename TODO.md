* fix the issue that causes the character to hang above ground sometimes
* add support for scaling images to the screen or smth
* add a menu
* add support for multiple kinds of game loops ?
* improve the documentation
    * more and better docstrings!
* consider making the Stage more "scenegraphy"
    * multi-sprite and multi-collision-box-objects ?
    * rethink how are r- and b-boxes related
* animations
    * spritemaps
* add more direct entity-to-entity interaction possibly?
* easy sharing of state across many levels -- so a boss once killed
  stays dead and all that kinda stuff
* key bindings/mappings, changing *in* game
* add an event recording system
    * parameter optimisation tool based on it
    * replays ?
    * bugfix tool (record events and see whether they still trigger bugs
      after changes)
* invert the way obstacles work (make obstacles tell the characters how
  to behave)
    * possibly, represent obstacles as sets of bi- (or not) directionally
      impenetrable line segments
* change to a widescreen viewport (16:8, to be hip (yes, that's 2:1, of
  course I know that!))
* create a pyglet-based engine?
    * tests don't show big performance gap against PyGame/SDL
    * OpenGL?
