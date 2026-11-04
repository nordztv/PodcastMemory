# Episode 2026-11-05 (Thursday)

## Running order
- Opening and world: Democrats win both houses of Congress in the US midterms; Sydney weather: early showers clearing, sunny Friday; bus industrial action
- Australia: Big four banks pass on the rate rise from 13 November; Albanese v Taylor on spending and rates; Burnham backpacker talks; AFP charges five over $235 million alleged welfare and NDIS fraud; David Jones on the brink over unpaid Westfield rent; High Court: Uber must pay $81 million in NSW payroll tax; NSW Liberals' MP exodus as One Nation surges; NSW Health cyber breach declared a major incident; Call for a 7.5% short-stay rental levy; Western Harbour Tunnel nears halfway; underquoting laws start 17 November
- Tech: AMD's record quarter and '80% growth in 2027'; gaming down 40%; Kospi's 7% swing and Nikkei slide on the US blue wave; Nvidia's reported 51% non-China rule for cloud partners; New Macs in stores Friday; first touchscreen MacBook Pro impressions; Qualcomm and Arm report this morning; Kimi K3.1 Pro: a 2.8-trillion-parameter open model; Quick hits: Tesla Korea FSD complaint, Grok in cars, HBM smuggling, Arc Pro B70 prices
- Games: Ocarina of Time on Switch 2: Famitsu 37/40, the NPR leak, day-one update; WoW Forever launches at 10am; Like a Dragon: Kenzan! gets an English fan translation; Cancelled Sega Mega Drive games preserved: Jester, Segapede, Treasure Tails; Snake's Japanese voice wants 'one more Metal Gear'; Godot 4.8 beta 2; Quick hits: GoldenEye leaves Game Pass, Dragon's Dogma 2 collab, Zero Parades, Witchbrook crossplay
- Movies: Godzilla Minus Zero opens in Australia; record Japan opening, big US projections; Tokyo festival top prize: Sister Brother Manhole Cover; Arrow's January 4K slate; Eureka's Scarlet Street 4K; Actress of the Month: the making of Lady Snowblood
- Lore: Chrono Trigger's Millennial Fair and the trial; Lanternfall: a festival that remembers what you did
- Game tech: Interaction in Godot: Area2D reach zone, groups, signals, tween pop
- Effects: Shin Godzilla: the first all-CG Toho Godzilla, performed by Mansai Nomura
- Director: Villeneuve and Deakins on Blade Runner 2049
- Workshop: Build step: a radish you can pull in Lanternfall
- Chat and goodbye: Launch day as a visit to who you used to be

## Deep dives
- Lore: Chrono Trigger's Millennial Fair and trial (case study) -> Lanternfall Festival ideas (lost lantern, radish contest with 'Sir', the nurikabe at the edge, a post-festival reckoning by the zashiki-warashi/elder/Chen; flags in GameState)
- Game tech: interaction in Godot 4.7 (Area2D reach zone on the farmer, interact action with is_action_just_pressed, get_overlapping_areas, "interactable" group, interact() on each object, custom signal pulled, collision layers/masks gotcha, tween pop + queue_free, show what's in reach)
- Effects: Shin Godzilla (2016): first all-CG Toho Godzilla, evolving forms, unused animatronic, maquette reference, Mansai Nomura mocap, archive roars, staged atomic breath
- Director: Villeneuve and Deakins on Blade Runner 2049
- Workshop: Lanternfall build step: a pullable radish (Area2D on layer 2, group, radish.gd with signal pulled + tween, Reach Area2D with mask 2, interact loop)
- Chat: launch day as a visit to who you used to be (Ocarina, WoW Forever, Godzilla on one day)

## Today's questions (host's joke answers)
1. If the Lanternfall village held a trial after the festival, Chrono Trigger style, what's the one small thing the player did that the villagers would bring up as evidence? (You talked to the scarecrow for forty five minutes. The scarecrow testified.)
2. Did you get to watch Lady Snowblood this week, and which moment has stayed with you since? (The umbrella. I haven't trusted an umbrella since.)
3. If you lit one scene in your travel videos with a single colour, like Deakins' orange Las Vegas, where would you film it, and what colour would it be? (A Sydney train platform at six in the morning. The colour is 'tired'.)

## Format notes
- Game thread: still the "Lanternfall foundations" fallback week (3 Nov snapshot, empty weekly_task.md); day 4 = interaction, setting up Friday's radish build-along step 1 (pull counter).
- No new answers, ratings, notes or challenge results since 2 Nov, so no answer reaction or suggestion.
- Challenge: 3 misses in a row -> stepped up (plank 105 s -> 120 s, rows instead of push-ups).
- Callbacks: lens spreadsheet with tabs, the tier 25 radish "Sir", the nurikabe's cake (Chen and murlocs rested after 4 Nov).
- News: only ABC, SBS and NSW ministerial releases were usable (Reuters/BBC/DW searches were rejected); no Iran item (nothing new found).
- Weather: BoM Moore Park forecast page (Sydney forecast page couldn't be fetched).

## Hot topics
- Major world news (until 7 Nov), Nintendo (Switch 2, Zelda) and Warcraft and Blizzard (until 8 Nov).

## Sources
- https://arri.com/news-en/lighting-blade-runner-2049-
- https://blackbird.chronocompendium.com/Term/Kingdom_Trial_Guide.html
- https://britishcinematographer.co.uk/roger-deakins-cbe-bsc-asc-blade-runner-2049/
- https://cdn.theasc.com/AC1217-Blade-Runner-2047.pdf
- https://docs.godotengine.org/en/stable/classes/class_area2d.html
- https://docs.godotengine.org/en/stable/classes/class_tween.html
- https://en.sedaily.com/finance/2026/11/04/kospi-swings-7-percent-before-closing-higher-as-us
- https://en.wikipedia.org/wiki/Lady_Snowblood_(film)
- https://en.wikipedia.org/wiki/Shin_Godzilla_(character)
- https://eurekavideo.co.uk/category/news/
- https://godotengine.org/blog/
- https://ir.amd.com/news-events/press-releases/detail/1303/amd-reports-third-quarter-2026-financial-results
- https://news.blizzard.com/en-us/article/24316094/prepare-for-forever-try-midnights-talebound-and-discover-sweet-treats-in-wow-weekly
- https://news.sbs.co.kr/english/article.do?news_id=N1008828674
- https://newsroom.arm.com/news/arm-announces-earnings-release-date-for-second-quarter-fiscal-year-ending-2027
- https://nintendolife.com/news/2026/11/dragons-dogma-2-dark-arisen-new-update-and-anime-collab-announced-here-are-the-full-patch-notes
- https://nobadmovie.com/2026/11/01/arrow-video-january-2027-titles-announced/
- https://screenrant.com/metal-gear-solid-6-no-kojima/
- https://strategywiki.org/wiki/Chrono_Trigger/The_Millennial_Fair
- https://thenextweb.com/news/moonshot-kimi-k3-1-pro-open-weight-cyber
- https://transportnsw.info/news/2026/sydney-bus-disruptions-due-to-industrial-action
- https://variety.com/2026/film/festivals/golden-lion-winner-sister-brother-manhole-cover-tokyo-1236893474/
- https://www.abc.net.au/news/2026-11-04/australian-banks-lift-interest-rates-after-rba-cash-rate-hike/107341858
- https://www.abc.net.au/news/2026-11-04/community-housing-body-calls-for-short-stay-levy/107341406
- https://www.abc.net.au/news/2026-11-04/cyber-security-nsw-police-investigate-cyber-breach-at-nsw-health/107344174
- https://www.abc.net.au/news/2026-11-04/david-jones-could-collapse-behind-on-westfield-rent/107345094
- https://www.abc.net.au/news/2026-11-04/democrats-claim-victory-over-republicans-2026-midterm-elections/107338138
- https://www.abc.net.au/news/2026-11-04/donald-trump-no-lame-duck-despite-us-midterm-results/107339272
- https://www.abc.net.au/news/2026-11-04/federal-police-five-charged-ndis-welfare-fraud/107344388
- https://www.abc.net.au/news/2026-11-04/federal-politics-live-blog-angus-taylor-rates/107342840
- https://www.abc.net.au/news/2026-11-04/high-court-rules-on-uber-81-million-tax-bill/107344014
- https://www.abc.net.au/news/2026-11-04/nsw-election-analysis-liberal-mp-exodus-amid-one-nation-surge/107342536
- https://www.abc.net.au/news/2026-11-04/us-midterms-democrats-win-majority-what-happens-next/107335330
- https://www.animenewsnetwork.com/interest/2016-08-11/get-up-close-and-personal-with-godzilla-in-behind-the-scenes-cg-video/.105271
- https://www.bom.gov.au/places/nsw/moore-park/forecast
- https://www.claimsjournal.com/news/national/2026/11/04/341114.htm
- https://www.criterion.com/films/28589-lady-snowblood
- https://www.freemalaysiatoday.com/category/business/2026/11/03/nvidia-orders-data-center-clients-to-reduce-china-exposure
- https://www.investing.com/news/earnings/amd-stock-jumps-after-hours-as-quarterly-results-revenue-guidance-beat-estimates-4996344
- https://www.japantimes.co.jp/culture/2026/11/04/entertainment-news/tiff-closing-film-tokyo/
- https://www.koimoi.com/box-office/godzilla-minus-zero-japan-box-office-delivers-a-monster-opening-day-sets-new-franchise-record/
- https://www.metacritic.com/movie/godzilla-minus-zero/critic-reviews/
- https://www.nintendolife.com/news/2026/11/the-first-review-for-zelda-ocarina-of-time-switch-2-is-in
- https://www.nintendolife.com/news/2026/11/the-legend-of-zelda-ocarina-of-time-on-switch-2-has-been-updated
- https://www.notebookcheck.net/Leaked-Zelda-Ocarina-of-Time-review-calls-Switch-2-game-safe-with-pacing-issues.1441138.0.html
- https://www.nsw.gov.au/ministerial-releases/full-steam-ahead-on-western-harbour-tunnel-as-boring-machines-near-halfway-mark
- https://www.nsw.gov.au/ministerial-releases/high-court-of-australia-ruling-on-uber-and-payroll-taxes
- https://www.nsw.gov.au/ministerial-releases/start-dates-set-for-minns-labor-governments-new-underquoting-laws
- https://www.purexbox.com/news/2026/11/three-xbox-games-are-shutting-down-their-servers-in-november-and-december-2026
- https://www.sbs.com.au/news/live-blog/us-midterm-elections-2026-live-results/1un8q7w91
- https://www.slashfilm.com/2298662/godzilla-minus-zero-box-office-preview/
- https://www.switchingtomac.com/apple-five-new-products-november-6-touchscreen-macbook-pro/
- https://www.thestreet.com/technology/mkbhd-review-apple-touchscreen-macbook-pro-proled-xdr-display
- https://www.timeextension.com/news/2026/11/former-sega-dev-shares-mega-drive-archive-inc-abandoned-code-for-segapede-jester-and-a-game-starring-sonics-pal-tails
- https://www.timeextension.com/news/2026/11/goldeneye-007-is-surprisingly-among-14-titles-being-removed-from-xbox-game-pass
- https://www.timeextension.com/news/2026/11/it-took-a-lot-of-work-the-elusive-ps3-title-like-a-dragon-kenzan-has-just-received-an-ai-free-fan-translation
- https://www.xtb.com/en/market-analysis/the-midterms-outcome
- https://www.timeextension.com/news/2026/11/goldeneye-007-is-surprisingly-among-14-titles-being-removed-from-xbox-game-pass
- https://en.wikipedia.org/wiki/Shin_Godzilla
- https://wikizilla.org/wiki/Shin_Godzilla/Credits
- https://filmmakermagazine.com/?p=103272
- https://chrono.fandom.com/wiki/Chrono_Trigger
- https://godotengine.org/blog/release
- https://www.metacritic.com/game/the-legend-of-zelda-ocarina-of-time-2026/critic-reviews/?platform=nintendo-switch-2
- https://www.wowhead.com/forever/news
