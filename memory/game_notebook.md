# Game design notebook: Scott's Godot game

Everything Scott has told the show about his 2D top-down action RPG in Godot 4 (Secret of Mana meets Stardew Valley), in his words where possible, so he has one place to design from. Started 26 Oct 2026 (weekly review f1, approved). Updated by the daily run from his answers, notes, the "What I built this week" box and chats. Scott can edit anything here. Never delete his ideas.

## Status
- 2 Nov 2026: Scott scrapped his game_prototype project to start again, but wants everything about it remembered (this whole notebook is kept). He wants the radish monster and the yokai ideas carried into the new game: keep recommending them.

- 3 Nov 2026: the current project is Game-Prototype, which has a weekly task. The show now follows it daily (bible 5c); weekly snapshots land in memory/game_project/.
- 3 Nov 2026 (sync): the new project is called Lanternfall (Godot 4.7), just created.

## The pitch
- A 2D top-down action RPG in Godot 4 on his MacBook Pro: Secret of Mana meets Stardew Valley (chose Godot over SpriteKit).

## Monsters
- Strongest radish, tier 25 (27 Oct): "Big white radish with a red top".
- The radish monster (20 Oct): the more radishes you pull while farming, the likelier a radish monster bursts out; it scales from weak (1) to strong (25); a random hidden counter that resets after it appears. Liked the host's turnip-with-teeth idea it grew from.
- 23 Oct: liked the "You've been harvested" game over screen idea; the radish monster isn't implemented yet.

## Forms and crests
- Form-changing crest (2 Nov, answer page): "tiger defend the farm from golbins." (the hero becomes a tiger that defends the farm from goblins)

## Spirits and summons
- Yokai (27 Oct): "I don't know yokai names, I just enjoy there existence".
- Farm spirit summons (26 Oct): "japanese yokai with all different personalities so every time you summoned one you wouldnt know what to expect."

## World and places
- The Dark World farm (21 Oct): "Like a cattle farm but it is humans being fattened for meat."
- Mode 7 moment (22 Oct): getting shot out of a cannon, like Secret of Mana's cannon travel.

- Monster from another sphere (26 Oct): "murlocs from world of warcraft. i love the noise those things make."

- Night-only crafting recipe (30 Oct): "Moon-cakes, tears from stars".

## Characters and merchants
- Nurikabe (28 Oct): "i would make him barrier between treasure so you would need to make him a recipe of a cake or something."
- Travelling merchant (23 Oct): Chen Stormstout (Warcraft), selling Stout and telling jokes about being hungry.

## Mechanics and decisions
- Look (26 Oct, decomp answer): would rebuild Secret of Mana with the "HD-2D" look.
- Progress (27 Oct, built box): "Nothing yes".
- Progress (26 Oct, built box): "I didnt really work on any project but the podcast. i really want to add the raddish to my game though, i just need to find the time to do it."
- Bullet time (23 Oct): he wouldn't add it.

## Radish build-along (f1 approved 31 Oct; one step each Friday)
- Steps: 1 pull counter, 2 spawn, 3 chase, 4 tiers (palette rows), 5 game over screen, 6 polish.
- Given: step 1 pull counter (6 Nov: GameState autoload, radish_pulls, random hidden threshold 8-15, register_pull() resets). Next: steps 2-4 (spawn, chase, tiers) are this week's fallback task (9-12 Nov), so Friday 13 Nov skips the build-along; then step 5 game over screen. Done: none reported yet.

## Lanternfall festival and the village's memory
- 6 Nov (answer page): who finds the goblins first: "Farmers and they use the bodies for fertiliser."
- 6 Nov (answer page): a film fight scene as a Lanternfall boss fight: "The original Matrix movie, neo vs agent smith in the subway".
- 6 Nov (answer page note): "Maybe you can ask questions that have answers that can integrate into my game project."
- 6 Nov (built box): "Nothing I was on holidays".
- 5 Nov (answer page): what the village would bring up as evidence at a trial after the festival: "Leaving dead goblins everywhere".

## Open questions from the show (not answered yet)
- Who in the village finds the goblins first, and what they say (6 Nov).
- A film fight scene he'd turn into a Lanternfall boss fight (6 Nov).
- What the Lanternfall really is (4 Nov).
- What a zashiki-warashi in the farmhouse loves, and what makes it leave (4 Nov).
- Signature item and what it lets the player do (19 Oct).
- Chen Stormstout's first line at his stall (29 Oct).
- A weapon hidden in an everyday farm object, and who carries it (3 Nov).
- The goblin leader's name and what he wants (3 Nov).

## Suggestions the show has given
- 9 Nov: fallback week "The radish wakes up" (spawn, chase, bite, tiers); spawning via preload/instantiate and a GameState radish_awakened(where) signal; burst tween; story: goblin compost is why radishes wake (mandrake), Radish Rules, compost item; suggestion: a fertilised flag so compost-grown radishes count double in register_pull.
- 5 Nov: interaction (a Reach Area2D on the farmer masking an interactable layer, interact action with is_action_just_pressed, get_overlapping_areas + an "interactable" group, interact() on each object, signal pulled, tween pop + queue_free); a pullable Radish scene ready for Friday's pull counter; a Lanternfall Festival where the village remembers what you did (lost lantern, radish contest, the nurikabe at the edge), Chrono Trigger style, stored as GameState flags.
- 4 Nov: top-down movement (CharacterBody2D, feet-only collision, Input Map, Input.get_vector, move_and_slide, short move_toward ramp, facing animations); try viewport stretch + nearest filter and the Compatibility renderer; Lanternfall night as falling star tears with chochin-obake red lanterns to avoid; a hidden house-luck value for a zashiki-warashi.
- 21 Oct: a tell before the radish monster spawns; randi_range threshold; scale stats.
- 23 Oct: radish spawn counter + AStarGrid2D chase; CanvasModulate day-night cycle; Resource save/load; fake-height cannon arc with a shrinking shadow.
- 26 Oct: build the smallest radish in one evening (counter, threshold, a red-square CharacterBody2D that chases with move_and_slide, burrows after ten seconds); procedural scatter with a seeded RandomNumberGenerator and FastNoiseLite.
- 27 Oct: palette swap shader for radish tiers (greyscale sprite, palette texture with one row per tier, nearest filter, material Local to Scene, hit-flash and warning rows); YokaiPersonality Resource with weights picked by RandomNumberGenerator.rand_weighted (helpful one waters a crop, prankster moves the hoe).
- 28 Oct: game feel for the radish (Camera2D trauma shake with FastNoiseLite, hit stop via Engine.time_scale and an ignore-time-scale timer, squash-and-stretch tween, hit flash row); make tier 25 look like a plain white radish with a red top, with one flickering palette row as its only tell.
- 30 Oct: inventory and crafting with Resources (ItemData with id, icon and max stack; Inventory Resource with slots and a changed signal; Recipe Resource with ingredients dictionary, can_craft/craft; radish cake = 3 radishes + rice flour + sugar for the NurikabeGate; greyed-out recipes; save by item id; drop items when full; Chen's shop as an inventory with prices).
- 2 Nov: save system (persist group with save/load Dictionaries, JSON via FileAccess to user://, version field, save when sleeping, save the radish counter and RNG seed; avoid loading untrusted Resource files); Git for the project; falling-star night event with star tear items and a night_only flag on recipes (moon-cakes).
- 3 Nov: tiger crest (CrestData Resource with sprite frames, speed and move; swap AnimatedSprite2D frames; Area2D roar puts goblins in a 3-second scared state running directly away, with a cooldown timer and screen shake); day-night lighting (CanvasModulate + Gradient, PointLight2D lanterns, UI on a CanvasLayer, TimeOfDay autoload with is_night for night-only recipes and star tears, save the time of day).
- 29 Oct: dialogue system (DialogueLine/DialogueChoice Resources, typewriter RichTextLabel with skip, choice Buttons, GameState autoload flags such as met_chen); radish-cake NurikabeGate (StaticBody2D + Area2D, exported wanted item, flag nurikabe_fed, tween modulate alpha, collision off with set_deferred).
