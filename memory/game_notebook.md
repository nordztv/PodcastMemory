# Game design notebook: Scott's Godot game

Everything Scott has told the show about his 2D top-down action RPG in Godot 4 (Secret of Mana meets Stardew Valley), in his words where possible, so he has one place to design from. Started 26 Oct 2026 (weekly review f1, approved). Updated by the daily run from his answers, notes, the "What I built this week" box and chats. Scott can edit anything here. Never delete his ideas.

## The pitch
- A 2D top-down action RPG in Godot 4 on his MacBook Pro: Secret of Mana meets Stardew Valley (chose Godot over SpriteKit).

## Monsters
- The radish monster (20 Oct): the more radishes you pull while farming, the likelier a radish monster bursts out; it scales from weak (1) to strong (25); a random hidden counter that resets after it appears. Liked the host's turnip-with-teeth idea it grew from.
- 23 Oct: liked the "You've been harvested" game over screen idea; the radish monster isn't implemented yet.

## World and places
- The Dark World farm (21 Oct): "Like a cattle farm but it is humans being fattened for meat."
- Mode 7 moment (22 Oct): getting shot out of a cannon, like Secret of Mana's cannon travel.

## Characters and merchants
- Travelling merchant (23 Oct): Chen Stormstout (Warcraft), selling Stout and telling jokes about being hungry.

## Mechanics and decisions
- Bullet time (23 Oct): he wouldn't add it.

## Open questions from the show (not answered yet)
- Signature item and what it lets the player do (19 Oct).
- A spirit summoned from something on the farm (26 Oct).
- A monster from another sphere dropped into the valley (26 Oct).

## Suggestions the show has given
- 21 Oct: a tell before the radish monster spawns; randi_range threshold; scale stats.
- 23 Oct: radish spawn counter + AStarGrid2D chase; CanvasModulate day-night cycle; Resource save/load; fake-height cannon arc with a shrinking shadow.
- 26 Oct: build the smallest radish in one evening (counter, threshold, a red-square CharacterBody2D that chases with move_and_slide, burrows after ten seconds); procedural scatter with a seeded RandomNumberGenerator and FastNoiseLite.
