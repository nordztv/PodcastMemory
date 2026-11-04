# Game project thread: progress log

The show's own log of the Game-Prototype weekly task (bible section 5c): one heading per week with the task in a line, then one line per episode (the lesson, the build step, the story and lore ideas, any game question asked). Newest week first. The weekly snapshot from Scott's Mac is in `snapshot/` (see `snapshot_info.md`). Scott can edit anything here.

## Week of 2026-11-02: Lanternfall foundations (fallback: the 3 Nov sync brought a new, almost empty Godot 4.7 project called Lanternfall, but no weekly task file)

- 2026-11-05: Lesson: interaction (Area2D reach zone on the farmer, interact action + is_action_just_pressed, get_overlapping_areas, "interactable" group, interact() on each object, custom signal pulled, collision layer/mask gotcha, tween pop + queue_free, show what's in reach). Build step: a pullable Radish scene (Area2D on layer 2 in group interactable, radish.gd with signal pulled, is_pulled guard and tween pop; Player Reach Area2D masking layer 2; interact loop; print on pulled; commit). Story: Chrono Trigger's Millennial Fair and trial; the Lanternfall Festival where the village remembers (lost lantern, radish contest with Sir, the nurikabe at the edge, a post-festival reckoning; flags in GameState). Question: what the village would bring up at a trial.
- 2026-11-04: Lesson: top-down movement (CharacterBody2D, small feet collision, Input Map, Input.get_vector, velocity, move_and_slide, move_toward acceleration, facing animations; project notes: try viewport stretch + nearest filter, Compatibility renderer). Build step: Input Map, Player scene, three-line movement, Farm scene with a test fence, first commit. Story: Stardew Valley case study; Lanternfall = night of falling lanterns that are the stars' tears (moon-cakes), chochin obake red lanterns to avoid, festival rhythm, Chen at Lanternfall; zashiki-warashi in the farmhouse with a hidden house-luck value. Questions: what the Lanternfall really is; what the zashiki-warashi loves and what makes it leave.

## Waiting for the first sync

- 2026-11-03: Scott asked for the show to follow his Game-Prototype weekly task. Until the first Sunday sync arrives, the thread uses the game notebook (radish monster, yokai, tiger crest) and the radish build-along.
