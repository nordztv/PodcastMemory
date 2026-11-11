# Morning Briefing, 2026-11-09 (Monday)

## Running order
- **Opening and world:** Cold, showery and windy: Sydney after the cold front; New Zealand election too close to call; special votes decide; Herzog asks Eisenkot, not Netanyahu, to form Israel's government; Stephen Miller replaces Susie Wiles; Iran, Hormuz mines and a US reward; Krakow market square shooting
- **Australia:** Victoria Barracks sale scrapped; Albanese: Iran war and tariffs shaped the midterms; MYEFO savings ahead; Cooks River AI data centre scrapped after backlash; Round-up: Helen Haines stable, Eva Geller, NSW Health cyber incident, Bathla sites, T8 every four minutes
- **Tech:** Kospi's Black Friday: down 6%, Hynix and Samsung slide again; The data-centre backlash, Nvidia's $450bn day and Friday's rebound; Report: TSMC drafting 3D DRAM plans for Nvidia; Memory is the bottleneck: GPUs still 2 to 4 times MSRP; First touchscreen Mac on sale; M6 MacBook Pro reviewed; Jensen Huang asked to meet House committee chairs; Tesla ends the Cybertruck; Starship Flight 15 targets Friday; Quick hits: Z2RAM memory start-up, Hyundai
- **Games:** GTA VI pre-load Tuesday, launch 19 Nov; Take-Two reports; Ocarina: Master Quest datamined, Star Fox remake passes 1M; Miyamoto unwell, expected back soon; Switch 2 third-party slate: FFVII Revelation dated 8 April 2027; SEGA Sammy results; Metaphor on Switch 2 Thursday; WoW Forever's first level 60; Quick hits and retro corner: Unity talks, Neil Broadley, FFXIV 7.58, Physint, recomps, VF2 model viewer; Retro Game of the Week: Crusader of Centy (Mega Drive)
- **Movies:** Godzilla Minus Zero: record foreign-language opening in America; Korea: Final Interview ends foreign films' run at No. 1; 1408 sequel; Paranormal Activity moves; Sleepy Hollow's Ichabod
- **Lore:** The mandrake, and why Lanternfall's radishes wake up
- **Game tech:** The week's task (the radish wakes up) and spawning scenes with signals
- **Effects:** Tremors: how the Graboids were built
- **Director:** Michael Mann's Heat: the downtown shootout
- **Workshop:** Build step 1: a radish monster bursts out of the ground
- **Chat and goodbye:** Dogs, mandrakes and John Wick; Your answers and the goblin compost suggestion

## Deep dives
- Lore: the mandrake (Theophrastus, Josephus' dog, the medieval scream, Galgenmannlein, Harry Potter) as the case study for the week's theme, 'the soil remembers': goblin compost wakes the radishes; Radish Rules, the tell, goblin compost item, the dog-on-a-rope idea
- Game tech: week's fallback task 'The radish wakes up' (Mon spawn, Tue chase, Wed bite, Thu tiers, Fri review); instancing scenes (preload, instantiate, add_child then global_position), GameState signal radish_awakened(where), call_deferred, warning shake + scale tween with TRANS_BACK
- Effects: Tremors (1990) Graboids
- Director: Michael Mann's Heat, the downtown shootout
- Workshop: RadishMonster scene, burst tween, GameState signal, register_pull(where), Farm spawner, test with threshold 2; stretch: the shake tell
- Chat: dogs, mandrakes and John Wick

## Today's questions (with the host's joke answers)
1. Lanternfall's dog-on-a-rope: one rule or trick to pull a radish safely. Host: send Chen Stormstout; if the radish eats him, it's a balanced meal.
2. The radish's first action and sound when it bursts out. Host: it sees the compost sack with the smiling goblin, and screams.
3. A farm animal companion and its one ability (Crusader of Centy style). Host: a very old goose whose ability is judging you.

## Answer reaction and suggestion
- 6 Nov answers (goblin bodies as fertiliser; Neo v Smith subway boss; John Wick kept forever) acknowledged briefly (reacted in Sunday special). Suggestion: a fertilised bool per radish; fertilised pulls count double in register_pull (compost = bigger radishes, faster monsters). Thanked for lore 5 and the note.

## Challenge
- Forty five push-ups and sixty bodyweight squats (rate 9 of 13, 69%; 3-6 Nov all done).

## Topics hot today
- None newly marked hot; Major world news (NZ, Israel) and chipmakers carry the big news.

## Notes
- Weather: BoM pages were not machine-readable tonight; Monday figures from Weatherzone's latest snapshot (about 11 to 19, showers, strong southerlies) and ABC's report of hazardous southerlies; Tuesday not given.
- BBC, Reuters and DW could not be fetched; world and Australian news from ABC, SBS and NSW ministerial releases only.
- No weekly task file from the Mac (last sync 3 Nov, task file empty): fallback week 'The radish wakes up'.

## Sources
- [ABC: Cold, showery and windy: Sydney after the cold front](https://www.abc.net.au/news/2026-11-08/snow-falls-parts-of-nsw-after-strong-cold-front/107361014)
- [ABC: New Zealand election too close to call; special votes decide](https://www.abc.net.au/news/2026-11-08/new-zealand-election-results-key-takeaways/107359778)
- [SBS: New Zealand election too close to call; special votes decide](https://www.sbs.com.au/news/article/new-zealand-election-hangs-on-special-votes/gewcwy3hw)
- [ABC: Herzog asks Eisenkot, not Netanyahu, to form Israel's government](https://www.abc.net.au/news/2026-11-08/israel-president-prime-minister-government-picked-eisenkot/107360472)
- [SBS: Herzog asks Eisenkot, not Netanyahu, to form Israel's government](https://www.sbs.com.au/news/article/israel-election-eisenkot-form-government/ez0jqmif2)
- [ABC: Stephen Miller replaces Susie Wiles; Iran, Hormuz mines and a US reward](https://www.abc.net.au/news/2026-11-07/donald-trump-cos-susie-wiles-to-be-replaced-by-stephen-miller/107358840)
- [ABC: Stephen Miller replaces Susie Wiles; Iran, Hormuz mines and a US reward](https://www.abc.net.au/news/2026-11-08/iran-strait-of-hormuz-update-explosions-talks/107360730)
- [ABC: Krakow market square shooting](https://www.abc.net.au/news/2026-11-08/deadly-shooting-in-krakow-market-poland/107360360)
- [SBS: Krakow market square shooting](https://www.sbs.com.au/news/article/poland-krakow-shooting/qz6f03jno)
- [ABC: Victoria Barracks sale scrapped](https://www.abc.net.au/news/2026-11-08/federal-politics-pm-scraps-sale-of-victoria-barracks-defence/107360530)
- [ABC: Victoria Barracks sale scrapped](https://www.abc.net.au/news/2026-11-08/sydney-victoria-barracks-sale-scrapped/107361044)
- [ABC: Albanese: Iran war and tariffs shaped the midterms; MYEFO savings ahead](https://www.abc.net.au/news/2026-11-07/albanese-trump-iran-war-midterms-chogm-budget/107356124)
- [ABC: Cooks River AI data centre scrapped after backlash](https://www.abc.net.au/news/2026-11-08/sydney-ai-data-centre-scrapped-after-community-backlash/107360592)
- [SBS: Round-up: Helen Haines stable, Eva Geller, NSW Health cyber incident, Bathla sites, T8 every four minutes](https://www.sbs.com.au/news/article/helen-haines-attack-condition-update-stable/g8hrpx6j3)
- [SBS: Round-up: Helen Haines stable, Eva Geller, NSW Health cyber incident, Bathla sites, T8 every four minutes](https://www.sbs.com.au/news/article/cybercrime-squad-investigating-major-nsw-health-data-breach/jhbcaq0q4)
- [ABC: Round-up: Helen Haines stable, Eva Geller, NSW Health cyber incident, Bathla sites, T8 every four minutes](https://www.abc.net.au/news/2026-11-08/collapsed-bathla-property-projects-risk-becoming-wastelands/107358154)
- [NSW Government: Round-up: Helen Haines stable, Eva Geller, NSW Health cyber incident, Bathla sites, T8 every four minutes](https://www.nsw.gov.au/ministerial-releases/major-rail-service-boost-for-southern-sydney-and-south-coast)
- [Korea Herald: Kospi's Black Friday: down 6%, Hynix and Samsung slide again](https://www.koreaherald.com/article/10928857)
- [Korea Times: Kospi's Black Friday: down 6%, Hynix and Samsung slide again](https://www.koreatimes.co.kr/economy/20261106/ai-investment-fears-spark-panic-selling-in-samsung-sk-hynix)
- [TechTarget: The data-centre backlash, Nvidia's $450bn day and Friday's rebound](https://www.techtarget.com/news/data-center-boom-could-hit-a-political-wall-after-midterms/874019/)
- [Fox Business: The data-centre backlash, Nvidia's $450bn day and Friday's rebound](https://foxbusiness.com/markets/stocks-11-6-2026)
- [hwbusters: Report: TSMC drafting 3D DRAM plans for Nvidia](https://hwbusters.com/news/tsmc-3d-dram-plans-reportedly-drafted-at-nvidias-request-as-the-memory-crunch-drags-on/)
- [Tom's Hardware: Memory is the bottleneck: GPUs still 2 to 4 times MSRP](https://www.tomshardware.com/pc-components/gpus/lowest-gpu-prices-tracking)
- [MacRumors: First touchscreen Mac on sale; M6 MacBook Pro reviewed](https://www.macrumors.com/2026/11/06/oled-macbook-pro-hands-on/)
- [Engadget: First touchscreen Mac on sale; M6 MacBook Pro reviewed](https://www.engadget.com/2307614/apple-macbook-pro-m6-review/)
- [Tom's Hardware: Jensen Huang asked to meet House committee chairs](https://www.tomshardware.com/tech-industry/big-tech/nvidias-jensen-huang-officially-called-to-congress-due-to-reports-of-a-chinese-spy-plot-officials-mention-growing-concerns-over-national-security)
- [Not a Tesla App: Tesla ends the Cybertruck; Starship Flight 15 targets Friday](https://notateslaapp.com/news/4954/tesla-will-end-cybertruck-production-to-make-more-cybercabs)
- [Tesla North: Tesla ends the Cybertruck; Starship Flight 15 targets Friday](https://teslanorth.com/2026/11/05/starship-flight-15-nov-13)
- [Tom's Hardware: Quick hits: Z2RAM memory start-up, Hyundai](https://tomshardware.com/tech-industry/this-week-in-toms-hardware-premium-november-7-2026-micron-roadmap-apples-touchscreen-ambitions-globalfoundries-interview-and-much-more)
- [Rockstar: GTA VI pre-load Tuesday, launch 19 Nov; Take-Two reports](https://www.rockstargames.com/newswire/article/k4ak9okk485712/grand-theft-auto-vi-pre-load-begins-on-november-10)
- [VICE: GTA VI pre-load Tuesday, launch 19 Nov; Take-Two reports](https://www.vice.com/en/article/gta-6-midnight-release-times-file-size-preload/)
- [Nintendo Life: Ocarina: Master Quest datamined, Star Fox remake passes 1M](https://www.nintendolife.com/news/2026/11/rumour-data-found-in-zelda-ocarina-of-time-may-hint-at-master-quest-dlc)
- [VGC: Ocarina: Master Quest datamined, Star Fox remake passes 1M](https://www.videogameschronicle.com/news/zelda-ocarina-of-time-switch-2-remake-review-published-in-famitsu/)
- [Nintendo Life: Miyamoto unwell, expected back soon](https://www.nintendolife.com/news/2026/11/sudden-illness-sees-miyamoto-miss-nintendos-financial-briefing-but-hes-expected-to-make-a-quick-recovery)
- [Nintendo Life: Switch 2 third-party slate: FFVII Revelation dated 8 April 2027](https://www.nintendolife.com/news/2026/11/nintendo-highlights-multiple-major-third-party-releases-on-the-way-to-switch-2-in-2027)
- [Gaming.net: SEGA Sammy results; Metaphor on Switch 2 Thursday](https://www.gaming.net/sega-sammy-profit-jumps-as-pachislot-offsets-entertainment-decline/)
- [VICE: WoW Forever's first level 60](https://www.vice.com/en/article/world-of-warcraft-forever-has-its-first-level-60-player/)
- [VGC: Quick hits and retro corner: Unity talks, Neil Broadley, FFXIV 7.58, Physint, recomps, VF2 model viewer](https://www.videogameschronicle.com/news/saudi-arabias-pif-and-investment-firm-silver-lake-have-reportedly-been-in-talks-to-buy-unity/)
- [Recomp Haven: Quick hits and retro corner: Unity talks, Neil Broadley, FFXIV 7.58, Physint, recomps, VF2 model viewer](https://recomphaven.com/releases/)
- [Noisy Pixel: Quick hits and retro corner: Unity talks, Neil Broadley, FFXIV 7.58, Physint, recomps, VF2 model viewer](https://noisypixel.net/ryu-ga-gotoku-kenzan-complete-english-fan-translation/)
- [Time Extension: Retro Game of the Week: Crusader of Centy (Mega Drive)](https://www.timeextension.com/features/the-making-of-soleil-crusader-of-centy-segas-answer-to-zelda)
- [Gematsu: Retro Game of the Week: Crusader of Centy (Mega Drive)](https://gematsu.com/2023/06/sega-genesis-nintendo-switch-online-adds-crusader-of-centy-ghouls-n-ghosts-landstalker-and-the-revenge-of-shinobi)
- [Variety: Godzilla Minus Zero: record foreign-language opening in America](https://variety.com/2026/film/box-office/box-office-godzilla-minus-zero-previews-1236941301/)
- [Forbes: Godzilla Minus Zero: record foreign-language opening in America](https://www.forbes.com/sites/markhughes/2026/11/07/godzilla-minus-zero-is-1-all-time-foreign-language-opening-weekend/)
- [Star News: Korea: Final Interview ends foreign films' run at No. 1](https://www.starnewskorea.com/en/movie/2026/11/05/2026110508294498934)
- [JoBlo: 1408 sequel; Paranormal Activity moves; Sleepy Hollow's Ichabod](https://www.joblo.com/1408-sequel/)
- [Dread Central: 1408 sequel; Paranormal Activity moves; Sleepy Hollow's Ichabod](https://www.dreadcentral.com/box-office/597009/paranormal-activity-moves-to-october-2027-taking-us-back-to-the-original-house-for-halloween/)
- [Fangoria: 1408 sequel; Paranormal Activity moves; Sleepy Hollow's Ichabod](https://www.fangoria.com/)
- [Wikipedia: The mandrake, and why Lanternfall's radishes wake up](https://en.wikipedia.org/wiki/Mandrake)
- [Godot docs: The week's task (the radish wakes up) and spawning scenes with signals](https://docs.godotengine.org/en/stable/tutorials/scripting/nodes_and_scene_instances.html)
- [Monster Legacy: Tremors: how the Graboids were built](https://monsterlegacy.net/2014/09/20/subterranean-terror-tremors/)
- [Wikipedia: Tremors: how the Graboids were built](https://en.wikipedia.org/wiki/Tremors_(1990_film))
- [/Film: Michael Mann's Heat: the downtown shootout](https://www.slashfilm.com/903330/how-michael-mann-made-heats-massive-shootout-work)
- [ASC: Michael Mann's Heat: the downtown shootout](https://theasc.com/articles/hot-set-shooting-heat)
- [ABC: Victoria Barracks background](https://www.abc.net.au/news/2026-11-07/inside-the-battle-over-defence-real-estate/107352438)
- [SBS: Eva Geller](https://www.sbs.com.au/news/article/bondi-shooting-victim-eva-geller-90-dies-nearly-a-year-after-terror-attack/j6tt8guvf)
- [ABC: Who Gives A Crap breach](https://www.abc.net.au/news/2026-11-08/who-gives-a-crap-hack/107359858)
- [SBS: Stephen Miller / Dana White](https://www.sbs.com.au/news/article/dana-white-donald-trump-press-secretary/12d59nzjm)
- [SBS: Iran reward](https://www.sbs.com.au/news/article/iran-says-its-military-is-stronger-than-before-war-as-us-offers-20m-reward-for-nuclear-info/n0spllf2i)
- [Weatherzone Sydney](https://www.weatherzone.com/au/nsw/sydney/sydney)
