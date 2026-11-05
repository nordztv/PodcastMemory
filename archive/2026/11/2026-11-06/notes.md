# Episode 2026-11-06 (Friday)

Recorded for Scott in Brisbane (South Bank) until Sunday 8 Nov, at his request: Brisbane weather and walk, Brisbane weekend ideas, no Sydney commute.

## Running order
- Opening and world: Brisbane weather for the weekend at South Bank; US midterms aftermath: Hinojosa wins Texas, Vance blames the Iran war; Trump says US military aid to Israel will stop; Israel's election certified; Russian strike on a Zaporizhzhia school shelter kills at least 33
- Australia: Education ministers agree the biggest school shake-up in years; NAB profit falls, Woodside cuts jobs, David Jones enters administration; Scanlon social cohesion survey: worried but holding together; CHOGM wraps with a consensus statement on slavery; Queensland: the $116 million police building nobody moved into; 3,000 more weekly Sydney bus services; 343 and 370 go 24/7; Moore Park South upgrade starts next to Green Square; Mardi Gras party returns; whale scientist is NSW Australian of the Year
- Tech: Chip rout: Kospi -5.3%, Hynix -9.5%, Tokyo Electron -9%; Apple at a record; Qualcomm and Arm results: the memory squeeze reaches phones; Samsung's Project Kairos HBM fab; Hynix gains DRAM share; AMD on track to out-earn Intel for the first time; Report: Intel may drop the Arc B580 to make more Arc Pro AI cards; Musk stocks fall; SpaceX picks Qualcomm for a Starlink ground network; Fujifilm X-T6 reportedly delayed again; Quick hits: Final Cut Pro 13 in November, TrueNAS 27 RC, Micron strike, Taiwan GDP, Hyundai record
- Games: Ocarina of Time remake scores 96 on Metacritic, 60fps; WoW Forever's smooth launch, layering complaints and the Oceanic RP bug; Nintendo half-year: Switch 2 at 26.35 million; Macronix leaves ROMs; The Elder Scrolls VI is Sentinel; the Fallout 3 trailer tease; Arkane Studios bids and the union's 'sabotage' claim; MediEvil recomp 1.0 and a Symphony of the Night SNES demake; Quick hits: PS5 near 98M, God of War Laufey and Duskbloods delayed, GTA VI preload, MGS4 patch, Yakuza Blocks; Next week: Metaphor: ReFantazio and Pikmin 4 on Switch 2
- Movies: Godzilla Minus Zero heads to America: $60m+ worldwide opening projected; Clayface passes The Substance as top body-horror film; AFM horror: Nervous, Nether Station, Violet; Radiance's February slate: Let's Scare Jessica to Death 4K, Shinobi Vol. 3; Resident Evil 4K; Korean November: Tristes Tropiques and White Blast; Japan's When You Open the Door
- Lore: Lanternfall in three acts: the week's story pulled together
- Game tech: Week review: test checklist, the silent area, ghost radish and shimmer bugs
- Effects: Crouching Tiger, Hidden Dragon: the bamboo forest wire-work
- Director: Sergio Leone's The Good, the Bad and the Ugly
- Workshop: Camera follow, pop sound, and radish build-along step 1: the pull counter
- Chat and goodbye: The week in a nutshell and the awards; A Brisbane weekend: the giant rubber duck, South Bank, Kurilpa and GOMA; Defending the picks: Lady Snowblood and Demon's Crest; Project check-in: the T330 (Jellyfin extras, snapshots, config backup)

## Deep dives
- Lore: Lanternfall in three acts (ordinary days with flags; festival night with gold lanterns as gifts and red chochin obake as trouble, Chen's stall, radish contest, the nurikabe; the morning after, the village remembers; zashiki-warashi house-luck)
- Game tech: Friday review of the week (movement + interaction): five-step test checklist; bugs: silent area (layers/masks), ghost radish (reference after queue_free), shimmer (nearest filter, stretch, pixel snap); stretch goal: pull animation, dust, radish label
- Effects: Crouching Tiger, Hidden Dragon's bamboo forest (real bamboo, harnesses, cranes, Yuen Woo-ping, digital wire removal, Tan Dun/Yo-Yo Ma; lesson: film moving surroundings; ease-out/ease-in jump tween)
- Director: Sergio Leone, The Good, the Bad and the Ugly (Techniscope wides and extreme close-ups, Sad Hill standoff, Morricone, Kill Bill link; lesson: wide-then-extreme-close pairs, cut to music markers in Final Cut)
- Workshop: Camera2D with position smoothing, AudioStreamPlayer2D pop; radish build-along step 1: GameState autoload with radish_pulls, random hidden threshold (randi_range 8-15), register_pull() resets, "Something stirs in the soil"
- Chat: week in a nutshell (irony of the week: the best new game of 2026 is from 1998; most predictable headline: memory shortage delays thing); Brisbane weekend; defending the picks; T330 check-in (Jellyfin extras folders, TrueNAS periodic snapshots, config backup, wait for TrueNAS 27 stable)

## Today's questions (host's joke answers)
1. Your village has seen you leave goblins all over the place. Who in Lanternfall village is the first to find them, and what do they say? (It's Chen, and he asks if they're for sale.)
2. If you could turn one fight scene from any film into a boss fight in Lanternfall, which scene would it be? (The bamboo forest from Crouching Tiger, but on very tall radishes.)
3. If your server could only keep one film forever, everything else gone, which film would it be, and why that one? (A 4K film of rain. Ninety minutes. No plot.)

## Answer reaction
- 5 Nov answers: trial evidence "Leaving dead goblins everywhere"; Lady Snowblood "I loved the fight scenes" (watched, liked); one-colour scene "Don't know". Suggestion: goblin remains sprite + GameState goblins_defeated, villager line the morning after Lanternfall.
- Thanked for 5s (opening and world, lore); Australia 3 noted (fewer stories told properly today).

## Hot today
- Major world news (US midterms aftermath), Chipmakers (rout), Nintendo (Ocarina 96), Warcraft and Blizzard (WoW Forever launch)

## Notes
- BBC, Reuters and DW were blocked for fetching; WebSearch with allowed domains failed; news used ABC, SBS and NSW ministerial releases only.
- Game thread: still the Lanternfall foundations fallback week (no weekly task file in the 3 Nov snapshot).

## Sources
- BoM: https://www.bom.gov.au/places/qld/south-brisbane/forecast
- ABC: https://www.abc.net.au/news/2026-11-05/us-midterm-elections-2026-live-updates/107257050
- ABC: https://www.abc.net.au/news/2026-11-05/us-midterm-texas-results-talarico-and-democrats-win-big/107348074
- SBS: https://www.sbs.com.au/news/article/donald-trump-us-military-aid-israel-midterms/tc0p7svih
- ABC: https://www.abc.net.au/news/2026-11-04/israeli-election-commission-fraud-investigation/107347454
- ABC: https://www.abc.net.au/news/2026-11-04/russian-strike-on-school-kills-dozens-n-ukraine/107343894
- ABC: https://www.abc.net.au/news/2026-11-05/education-ministers-agree-to-biggest-shake-up-in-years-of-school/107348312
- ABC: https://www.abc.net.au/news/2026-11-05/asx-markets-business-live-news-november-5-2026/107347286
- ABC: https://www.abc.net.au/news/2026-11-05/scanlon-foundation-social-cohesion-survey/107342800
- ABC: https://www.abc.net.au/news/2026-11-05/federal-politics-live-blog-screen-limits-nov-5/107346422
- ABC: https://www.abc.net.au/news/2026-11-05/corruption-watchdog-queensland-police-building/107349896
- NSW Government: https://www.nsw.gov.au/ministerial-releases/3000-more-weekly-bus-services-as-nsw-government-continues-to-rebuild-bus-network
- NSW Government: https://www.nsw.gov.au/ministerial-releases/new-community-facilities-on-way-for-one-of-australias-most-densely-populated-areas
- ABC: https://www.abc.net.au/news/2026-11-05/nsw-sydney-mardi-gras-party-2027-announcement/107346014
- ABC: https://www.abc.net.au/news/2026-11-04/nsw-australian-of-the-year-2027-nominees-announced/107345830
- Korea Times: https://www.koreatimes.co.kr/economy/20261105/kospi-tumbles-as-democrat-sweep-fuels-ai-infrastructure-concerns
- StockTitan: https://www.stocktitan.net/articles/stock-market-today-live-november-4-2026
- Focus Taiwan: https://focustaiwan.tw/business/202611050008
- The Elec: https://www.thelec.net/news/articleView.html?idxno=15303
- Investing.com: https://www.investing.com/news/earnings/arm-stock-slips-after-hours-despite-quarterly-results-and-guidance-beat-5001212
- Seoul Economic Daily: https://en.sedaily.com/finance/2026/11/04/samsung-to-build-advanced-foundry-fab-at-giheung-campus
- JoongAng Daily: https://www.koreajoongangdaily.com/business/samsung-keeps-dram-lead-as-sk-hynix-claws-back-global-share-in-q3/12958078
- PC Gamer: https://www.pcgamer.com/hardware/processors/amd-says-its-going-to-beat-intel-in-total-revenue-for-the-very-first-time-by-the-end-of-2026/
- VideoCardz: https://videocardz.com/newz/intel-arc-b580-may-reportedly-face-shortages-as-company-prioritizes-arc-pro-gpus-for-ai
- Via Satellite: https://www.satellitetoday.com/connectivity/2026/11/04/spacex-strikes-deal-with-qualcomm-for-terrestrial-component-of-starlink-mobile-network/
- Imaging Resource: https://www.imaging-resource.com/news/fujifilm-x-t6-rumored-to-be-delayed-again/
- Apple: https://www.apple.com/newsroom/2026/10/apple-creator-studio-adds-powerful-new-ai-features-and-even-more-creative-tools/
- FCP Cafe: https://fcp.cafe/
- TrueNAS: https://www.truenas.com/blog/truenas-27-is-here/
- GamesRadar: https://www.gamesradar.com/games/the-legend-of-zelda/the-legend-of-zelda-ocarina-of-time-remakes-metacritic-score-makes-it-the-highest-rated-game-of-2026-but-even-it-cant-reach-the-originals-near-perfect-score/
- Nintendo Life: https://www.nintendolife.com/reviews/nintendo-switch-2/the-legend-of-zelda-ocarina-of-time
- Nintendo Life (Digital Foundry): https://www.nintendolife.com/news/2026/11/worth-your-time-digital-foundry-delivers-its-tech-review-for-zelda-ocarina-of-time
- Time Extension: https://www.timeextension.com/news/2026/11/nintendo-got-the-original-zelda-ocarina-of-time-artist-to-draw-the-remakes-map
- Blizzard Watch: https://blizzardwatch.com/2026/11/04/world-warcraft-forever-servers-yet-absolutely-not/
- Icy Veins: https://www.icy-veins.com/wow-forever/news/where-did-everyone-go-wow-forever-players-blast-its-disruptive-layering/
- Wowhead: https://www.wowhead.com/forever/news/everything-you-need-to-know-for-wow-forevers-global-launch-383656
- Nintendo Life: https://www.nintendolife.com/news/2026/11/switch-2-surpasses-26-million-units-sold-hardware-sales-down-by-37-4percent
- Nintendo Life: https://www.nintendolife.com/news/2026/11/switch-cartridges-under-threat-as-key-rom-manufacturer-exits-business
- Gematsu: https://www.gematsu.com/2026/11/the-elder-scrolls-vi-sentinel-subtitle-announced
- OpenCritic: https://opencritic.com/news/39082/bethesda-disappoints-fans-with-an-oddly-timed-fallout-3-post
- Pure Xbox: https://www.purexbox.com/news/2026/11/report-xbox-has-had-multiple-offers-for-arkane-studios-marvels-blade-close-to-completion
- VGC: https://www.videogameschronicle.com/news/arkane-union-says-xbox-is-sabotaging-blade-development/
- Time Extension: https://www.timeextension.com/news/2026/11/we-have-the-skills-to-bring-love-to-these-old-games-after-last-months-beta-medievils-ai-free-recomp-hits-version-1-0
- Time Extension: https://www.timeextension.com/news/2026/11/castlevania-symphony-of-the-night-is-getting-an-ai-free-snes-port-and-you-can-play-it-now
- VGC: https://www.videogameschronicle.com/news/sony-says-playstation-6-development-is-progressing-as-scheduled-as-ps5-sales-hit-97-9m/
- VGC: https://www.videogameschronicle.com/news/god-of-war-laufey-has-officially-been-delayed/
- Pure Xbox: https://www.purexbox.com/news/2026/11/gta-6-download-size-and-preload-times-officially-revealed-for-xbox-series-xs
- RPG Site: https://www.rpgsite.net/news/19530-metaphor-refantazio-switch-2-release-date-direct
- Deadline (via Yahoo): https://www.yahoo.com/entertainment/movies/box-office-results/articles/godzilla-minus-zero-stomping-60m-000954405.html
- AV Club: https://www.avclub.com/godzilla-minus-zero-review-king-ghidorah-sequel
- Rotten Tomatoes: https://www.rottentomatoes.com/m/godzilla_minus_zero
- Filmofilia: https://www.filmofilia.com/clayface-passes-the-substance-worldwide-box-office-232357/
- Fangoria: https://www.fangoria.com/nervous-sarah-bolger/
- Fangoria: https://www.fangoria.com/paul-w-s-anderson-nether-station-adaptation/
- Fangoria: https://www.fangoria.com/creep-team-new-movie-violet/
- Blu-ray.com: https://www.blu-ray.com/news/?id=39284
- Screen Connections: https://screen-connections.com/2026/11/03/resident-evil-2026-4k-uhd-4k-steelbook-blu-ray-dvd-digital-details/
- NewsCulture: https://www.nc.press/news/articleView.html?idxno=630019
- Horror Historian: https://horrorhistorian.substack.com/p/asian-horror-film-news-november-1
- Godot docs: https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html
- Godot docs: autoloads: https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html
- Brisbane Kids: https://brisbanekids.com.au/event/rubber-duck/
- Visit South Bank: https://www.visitsouthbank.com.au/things-to-do/all-things-to-do
- QAGOMA: https://www.qagoma.qld.gov.au/whats-on/exhibitions/
- Queensland Museum: https://museum.qld.gov.au/kurilpa/plan-your-visit/hours-and-admission
- Jellyfin docs: https://jellyfin.org/docs/general/server/media/movies/
- ABC (Spain crash, NSW Australian of the Year): https://www.sbs.com.au/news/article/two-australians-among-the-deceased-from-high-speed-train-crash-in-spain/3061rc76s
- ABC (Brisbane weather background): https://www.abc.net.au/news/2026-11-04/qld-weather-southern-storms-ease-as-temperatures-rise/107341660
