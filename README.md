# About

Quantee is an in-development platformer, intended to draw inspiration
from quantum mechanics (but not too heavily... it is foremost supposed
to be playable).

We're also trying to keep some of the code generic enought so that we
can rip it out and turn it into a framework without too much effort.

## Dependencies

* Python 2.7
* Pygame 1.9

Has been launched succesfully on both Linux and Windows. I'd assume
it'll also work on a Mac or any other Unix-like system supporting the
two aforementioned packages.

## Try it

Assuming your system recognises `python` as Python 2.7:

```bash
% python src/quantee.py
```

You should be able to run around, jump, collect a star and replay the
level. Use Escape to exit the game.

## Documentation

Sadly, far from completion. You can use pydoc to look at what's there. A
brief overview:

* `src/quantee.py` -- main project file contains a messy bunch of
  classes
* `src/game.py` -- `Game` the which manages the entire
  main loop
* `src/engine.py` -- `Engine` an abstract base class for backends
* `src/sdl.py`
  * `SDL` a PyGame-based backend
  * `AssetManager` an abstract base class for assets-loading objects
* `src/assets.py` -- `QAssets` an asset loader for `SDL`
* `src/qengine.py` -- `QEngine` an `SDL` subclass wrapping the PyGame
  events with more convenient (in our case) wrapper methods
* `src/level.py` -- `Level` the class guiding the interactions of
  everything that composes a game level
* `src/entity.py` -- `Entity` a base class for all on-screen objects
  that an user might see
* `src/behaviour.py` -- `Behaviour` an abstact base class for things
  that control `Entities'` actions
* `src/stage.py` -- `Stage` collection of layered `Entities` tied to a
  particular level
* `src/director.py` -- `Director` abstract base class for things bossing
  everyone in a given `Level` around
* `src/boxes.py` -- `Box` class for axis alligned bounding boxes
* `src/drawing_strategy.py` -- considered for deprecation
  * `DrawingStrategy` abstract base class for objects deciding what to
    draw onscreen
  * `Everything` -- the simplest one possible
  * `DirtyWholes` -- draws less than Everything in some cases, but
    always redraws a whole `Entity`

## Versioning

The scheme is `major.minor.release-optional_suffix`. For versions below
`1.0.0` we allow breaking backward compatibility when the minor changes
and introducing new API elements when the release changes. Post `1.0.0`
we'll break compatibility only each major version, add new stuff each
minor and fix bugs each release.

## Change history

See [CHANGES.md](CHANGES.md).

## License

See [LICENSE](LICENSE).

## Contact

Karol Marcjan: @szabba on both twitter and github

Bartosz Boguniewicz: @drBradley on github
