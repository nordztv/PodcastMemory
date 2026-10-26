# Game design notebook: Scott's Godot game

Everything Scott has told the show about his 2D top-down action RPG in Godot 4 (Secret of Mana meets Stardew Valley), in his words where possible, so he has one place to design from. Started 26 Oct 2026 (weekly review f1, approved). Updated by the daily run from his answers, notes, the "What I built this week" box and chats. Scott can edit anything here. Never delete his ideas.

## The pitch
- A 2D top-down action RPG in Godot 4 on his MacBook Pro: Secret of Mana meets Stardew Valley (chose Godot over SpriteKit).

## Monsters
- The radish monster (20 Oct): the more radishes you pull while farming, the likelier a radish monster bursts out; it scales from weak (1) to strong (25); a random hidden counter that resets after it appears. Liked the host's turnip-with-teeth idea it grew from.
- 23 Oct: liked the "You've been harvested" game over screen idea; the radish monster isn't implemented yet.

## Spirits and summons
- Farm spirit summons (26 Oct): "japanese yokai with all different personalities so every time you summoned one you wouldnt know what to expect."

## World and places
- The Dark World farm (21 Oct): "Like a cattle farm but it is humans being fattened for meat."
- Mode 7 moment (22 Oct): getting shot out of a cannon, like Secret of Mana's cannon travel.

- Monster from another sphere (26 Oct): "murlocs from world of warcraft. i love the noise those things make."

## Characters and merchants
- Travelling merchant (23 Oct): Chen Stormstout (Warcraft), selling Stout and telling jokes about being hungry.

## Mechanics and decisions
- Look (26 Oct, decomp answer): would rebuild Secret of Mana with the "HD-2D" look.
- Progress (26 Oct, built box): "I didnt really work on any project but the podcast. i really want to add the raddish to my game though, i just need to find the time to do it."
- Bullet time (23 Oct): he wouldn't add it.

## Open questions from the show (not answered yet)
- Signature item and what it lets the player do (19 Oct).
- The strongest radish tier's colour and name (27 Oct).
- Which yokai knocks on the farmhouse door at 2am, and what it wants (27 Oct).

## Suggestions the show has given
- 21 Oct: a tell before the radish monster spawns; randi_range threshold; scale stats.
- 23 Oct: radish spawn counter + AStarGrid2D chase; CanvasModulate day-night cycle; Resource save/load; fake-height cannon arc with a shrinking shadow.
- 26 Oct: build the smallest radish in one evening (counter, threshold, a red-square CharacterBody2D that chases with move_and_slide, burrows after ten seconds); procedural scatter with a seeded RandomNumberGenerator and FastNoiseLite.
- 27 Oct: palette swap shader for radish tiers (greyscale sprite, palette texture with one row per tier, nearest filter, material Local to Scene, hit-flash and warning rows); YokaiPersonality Resource with weights picked by RandomNumberGenerator.rand_weighted (helpful one waters a crop, prankster moves the hoe).
