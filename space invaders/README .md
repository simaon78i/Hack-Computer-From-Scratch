# Space Invaders - Nand2Tetris Project 9

A complete Space Invaders game written in the Jack language for the Hack
platform (512x256 black-and-white screen, keyboard input).

NOTE: do not include this README in your course submission zip - submit
only the .jack files and the AUTHORS file, as the auto-grader expects.

## Files

| File                     | Responsibility                                            |
|--------------------------|-----------------------------------------------------------|
| Main.jack                | Entry point: creates, runs, and disposes the game.        |
| SpaceInvadersGame.jack   | Game engine: main loop, levels, collisions, pause, flow.  |
| Player.jack              | The player's ship: drawing, clamped movement, reset.      |
| Bullet.jack              | Generic bullet (used by both player and aliens).          |
| AlienGrid.jack           | Alien formation: marching, shooting, explosions, levels.  |
| Shield.jack              | Destructible bunkers carved block-by-block by bullets.    |
| GameUI.jack              | Title screen, HUD, level banners, pause and end screens.  |
| Random.jack              | LCG pseudo-random generator fed with gameplay entropy.    |

## How to compile and run

1. Compile the folder with the Jack compiler from the nand2tetris tools:
   JackCompiler <this folder>
2. Open the VM Emulator, load the entire folder, answer "Yes" to using
   the built-in OS implementation, set Animate to "No animation" and
   speed to Fast, then Run. Click inside the emulator screen so the
   keyboard is captured.

## Controls

- Left / Right arrows : move the ship
- Space               : fire (one player bullet on screen at a time)
- P                   : pause / resume
- Q                   : quit

## Gameplay

- 3 levels. Each level restores the full 3x6 alien formation and fresh
  shields, with faster marching and a higher alien fire rate.
- Each alien destroyed is worth (level * 10) points and explodes with a
  brief X-shaped flash.
- Three destructible shields protect the player. Bullets from BOTH sides
  carve blocks out of them (just like the original arcade game), so the
  player must shoot through the gaps they create.
- The formation speeds up as it shrinks (the movement delay is
  proportional to the number of alive aliens).
- Alien shots come from the lowest alive alien in a pseudo-randomly
  chosen column, so they always have a clear path.
- Win: clear all 3 levels. Lose: lives reach 0, or the formation
  descends to the shield line.

## Design notes

- OS Math class: Math.min / Math.max clamp the player's position and
  the difficulty pacing; Math.abs normalizes speeds and keeps the
  random generator state non-negative.
- No modulo in Jack: AlienGrid.mod(a, b) implements a - (a / b) * b.
- No operator precedence in Jack: every compound expression in the code
  is fully parenthesized.
- Manual memory management: every class has a dispose() method, and
  Main disposes the game on exit (the Jack OS has no garbage collector).
- Pseudo-randomness: the Hack platform has no random source, so a
  linear congruential generator (Random.jack) is perturbed with
  user-dependent entropy (player position at fire time).
- Rendering: objects erase only their own bounding box and redraw,
  instead of clearing the whole screen each frame.
