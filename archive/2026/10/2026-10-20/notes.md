# Morning Briefing - Tuesday 20 October 2026

Script written early, on Monday evening (about 8 to 10pm Sydney), at Scott's request in a chat session, so the news is as of Monday night. The 2:45am scheduled run may refresh it with overnight news. Audio NOT rendered: the voice engine install (engine/setup.sh) was blocked by the session's permission check, so build with `sh engine/build_episode.sh 2026-10-20` once the voice engine runs. About 12,100 words (a little over the usual length; the deep dives ran long).

## Running order
1. Opening and world: weather (BOM data API and Weatherzone; BOM forecast page didn't load), no trackwork found for Tuesday, weekend Central to Wynyard closure; France unrest (nearly 2,400 arrests, Macron address); Trump v Zelenskyy; WFP Gaza aid cuts; CFB Wainwright fire (Carney); Ebola in Kenya and Congo.
2. Australia: Helen Haines critically injured in alleged deliberate attack in Wangaratta (lead, serious); Greens Steele-John row; EU trade deal stalled; Ghost Shark armed (AUKUS Pillar Two); Grattan GST 15%; One Nation migration costings; ANSTO spyware targeting (Citizen Lab); Whyalla steel; Vanuatu and China police. NSW: Mount Pleasant coal mine bill; peptide warning; LECC Town Hall protest hearings; preschool funding; pink slip crackdown; Hunter's Hill councillor. Sport: 2nd Test rain, Boland; women's T20 tonight; Diamonds; RLWC Kangaroos.
3. Tech: chip sell-off (Nvidia -$365B, SOX -11.4%, CoreWeave financing stress); RTX 5090 $8,500; SK Hynix worst week since 2008; Intel LLM-Scaler-vLLM PV 1.5; $35 mining rig with 54 GB VRAM; Linux 7.3 (Samsung 990 workarounds); TrueNAS 27 / Jellyfin 12.2 status; Pi OS update; Gurman's four Fridays and iPhone Duo pre-order "mistake"; earnings week (Netflix, SpaceX, Tesla, Meta, Western Digital); Starship Flight 15; Godot 4.8 beta 1.
4. Games: FF Resonance length, preload, sizes; Switch Sports Resort; Ocarina remake display modes; Tuesday retro nudge (A Link to the Past, Pegasus Boots); ID@Xbox showcase and Shrek 2 remaster leak; MW4 Zampella tribute; WoW Forever stress test moved, 12.1.7 PTR; Dino Crisis 2 on PS Plus; Konami on AI and Silent Hill; CDPR roadmap; quick hits.
5. Movies: Australian box office (Street Fighter #1); Korean box office; Sitges winners; Garland and Zendaya; Kyotou O; 4K releases (Planet of the Vampires, Kubrick set, Chinese Ghost Story, Umbrella Cube). Actress of the Month starts: Sigourney Weaver; Tuesday pick Aliens (1986).
6. Lore: Warcraft III and the fall of Arthas.
7. Game tech: Ray tracing explained (Godot tip: PointLight2D, LightOccluder2D, CanvasModulate).
8. Effects: The Thing (1982) creature effects.
9. Director: Ridley Scott's Alien (1979).
10. Workshop: Upgrading to Jellyfin 12 safely on TrueNAS (snapshot first, remove plugins, check old clients).
11. Chat and outro: what makes a monster readable in a top-down game; workout (upper pull and core); week ahead; goodbye.

## Today's questions (with the host's joke answers)
1. First job you'd give a local AI model with a 32 GB card? Host: watch the Jellyfin logs and leave notes about him watching Alien three nights running.
2. Which classic FF party member would you drop into Resonance as a guest? Host: Kefka, to heckle every boss and take over the menu screen.
3. First monster in your game, and how will the player know to fight or run? Host: a turnip with legs that grows teeth when watered.

## Hot today
None marked. Chip sell-off is the biggest tech story but no topic hot flag applied. FF Resonance launches Thu 22 Oct (mark hot then).

## Assumptions and gaps
- Reuters, BBC and DW were blocked for fetching; WebSearch with allowed domains failed. News is from ABC, SBS and NSW Government releases only.
- The 1st Test result was not stated in the source, so it isn't mentioned.
- Retro reminder placed in games segment. October's Actress of the Month chosen today (no actress yet this month).

## Sources
News (allowed sources only):
- https://www.sbs.com.au/news/article/almost-2400-arrested-macron-france-unrest/l51gcezko
- https://www.abc.net.au/news/2026-10-19/france-reels-from-protest-violence-thousands-arrested/107281138
- https://www.sbs.com.au/news/article/zelenskyy-ukraine-russia-trump-criticism/uq610r8yy
- https://www.abc.net.au/news/2026-10-19/ukraine-relationship-with-us-and-trump-strained-amid-war/107273416
- https://www.abc.net.au/news/2026-10-19/un-world-food-programme-slashes-assistance-in-gaza/107282322
- https://www.abc.net.au/news/2026-10-19/canadian-military-fire-mark-carney/107281574
- https://www.abc.net.au/news/2026-10-19/kenya-ebola-outbreak-hits-eight-continues-spread-in-congo/107282278
- https://www.abc.net.au/news/2026-10-19/live-blog-victoria-indi-mp-helen-haines-injured-wangaratta/107285046
- https://www.sbs.com.au/news/article/helen-haines-injured-outside-wangaratta-office/8jahoxo1k
- https://www.abc.net.au/news/2026-10-19/helen-haines-injured-in-incident-near-wangaratta-office/107284764
- https://www.abc.net.au/news/2026-10-19/shoebridge-insists-steele-john-should-take-leave/107282442
- https://www.sbs.com.au/news/article/greens-senator-jordon-steele-john-response-to-misbehaviour-allegations/ympu0y1z7
- https://www.sbs.com.au/news/podcast-episode/labor-urges-coalition-to-support-eu-trade-deal-midday-news-bulletin-19-october-2026/m5le66idx
- https://www.sbs.com.au/news/podcast-episode/government-unveils-new-aukus-capabilities-as-eu-trade-deal-languishes/mr517cg6r
- https://www.abc.net.au/news/2026-10-19/ghost-shark-fleet-aerial-drones-sea-mines-defence/107283746
- https://www.abc.net.au/news/2026-10-19/nuclear-agency-targeted-in-cyber-attack-infecting-devices/107283804
- https://www.abc.net.au/news/2026-10-19/whyalla-blast-furnace-fail-gupta-to-blame-safety-issues/107282744
- https://www.abc.net.au/news/2026-10-19/vanuatu-expects-reduction-in-china-police-presence/107283618
- https://www.nsw.gov.au/ministerial-releases/minns-labor-government-steps-to-protect-400-hunter-jobs-ahead-of-christmas
- https://www.abc.net.au/news/2026-10-19/mount-pleasant-mine-nsw-government-legislation-jobs/107282908
- https://www.nsw.gov.au/ministerial-releases/nsw-health-warns-of-surge-hospital-presentations-linked-to-peptide-use
- https://www.abc.net.au/news/2026-10-19/lecc-town-hall-protest-public-examinations-nsw-police/107261744
- https://www.nsw.gov.au/ministerial-releases/more-childcare-places-and-fairer-pay-minns-labor-government-reforms-of-early-learning-sector-continue
- https://www.nsw.gov.au/ministerial-releases/nsw-government-cracks-down-on-operators-issuing-sight-unseen-pink-and-blue-slips
- https://www.abc.net.au/news/2026-10-19/sydney-councillor-resigns-hunters-hill-council/107282630
- https://www.abc.net.au/news/2026-10-19/test-cricket-live-updates-south-africa-vs-australia/107282378
- https://www.abc.net.au/news/2026-10-19/australia-sa-quick-hits-boland-ackerman-rain/107280916
- https://www.abc.net.au/news/2026-10-18/constellation-cup-netball-diamonds-silver-ferns-game-one/107280774
- https://www.abc.net.au/news/2026-10-19/rugby-league-world-cup-quick-hits/107282480

Weather and commute:
- https://api.weather.bom.gov.au/v1/locations/r3gx2f/forecasts/daily
- https://api.weather.bom.gov.au/v1/locations/r3gx2f/forecasts/hourly
- https://www.weatherzone.com/au/nsw/sydney/sydney
- https://transportnsw.info/news/2026/planned-trackwork-from-friday-23-to-sunday-25-october

Tech:
- https://invezz.com/news/2026/10/19/nvidia-stock-loses-365-billion-in-a-week-could-the-ai-boom-be-running-out-of-money/
- https://home.saxo/en-gb/content/articles/macro/market-quick-take---chipmakers-extend-their-slide-as-brent-holds-above-107---19-october-2026-19102026
- https://www.benzinga.com/markets/prediction-markets/26/10/62396367/nvidia-ai-demand-orders-jensen-huang
- https://invezz.com/news/2026/10/19/sk-hynix-stock-falls-another-3-after-brutal-24-rout-when-will-the-selling-stop/
- https://www.tomshardware.com/pc-components/gpus/nvidia-reportedly-insists-the-rtx-5090-isnt-dead-despite-severe-shortages-and-removed-listings-at-multiple-retailers-flagship-gpu-is-missing-from-nvidias-store-and-commands-usd8-500-on-amazon
- https://www.phoronix.com/news/Intel-LLM-Scaler-vLLM-PV-1.5
- https://www.tomshardware.com/pc-components/gpus/reddit-user-pays-usd35-for-a-crypto-mining-rig-left-in-a-garage-and-gets-54gb-of-vram-at-65-cents-per-gb-the-first-test-for-2017-era-gpus-a-35b-parameter-ai-model-running-locally-at-over-30-tokens-per-second
- https://www.tomshardware.com/pc-components/gpus/nvidia-doubles-dlss-5-performance-reduces-4k-vram-usage-by-20-percent-with-latest-model-october-update-cuts-footprint-by-24-percent-to-roughly-118-million-parameters
- https://www.phoronix.com/news/Linux-7.3-Released
- https://phoronix.com/news/TrueNAS-27-RC.1-Release
- https://releasebot.io/updates/jellyfin/jellyfin-server
- https://linuxiac.com/raspberry-pi-os-october-2026-update-gets-better-dock-handling-and-many-fixes/
- https://www.macrumors.com/2026/10/18/apple-product-releases-next-four-fridays/
- https://www.macrumors.com/2026/10/18/gurman-says-iphone-duo-preorders-major-mistake/
- https://www.tipranks.com/news/netflix-will-report-earnings-on-oct-20-options-traders-expect-a-large-move-in-nflx-stock-post-q3-results
- https://driveteslacanada.ca/spacex/spacex-q3-2026-earnings-october-20/
- https://www.spacelaunchschedule.com/news/starship-flight-15-launch-date-how-to-watch/
- https://www.tipranks.com/news/tesla-will-report-q3-earnings-on-oct-21-options-traders-bet-big-on-tsla-stock-swing-post-q3-earnings
- https://www.fool.com/investing/2026/10/15/teslas-cybercab-robotaxi-fleet-jumped-eightfold-in/
- https://tech-insider.org/tesla-spacex-meta-earnings-week-2026/
- https://godotengine.org/article/dev-snapshot-godot-4-8-beta-1/

Games:
- https://www.pushsquare.com/news/2026/10/first-final-fantasy-resonance-ps5-review-released-rough-campaign-length-revealed
- https://www.gamerfuzion.com/final-fantasy-resonance-download-size-preload-date-ps5-xbox-switch-pc/
- https://www.nintendolife.com/news/2026/10/round-up-the-final-previews-for-nintendo-switch-sports-resort-are-in
- https://nintendoeverything.com/zelda-ocarina-of-time-remake-reveals-new-display-modes-other-settings/
- https://windowsreport.com/id-xbox-october-2026-showcase-date-start-time-how-to-watch-expected-games/
- https://www.nintendolife.com/news/2026/10/surprise-aspyr-is-remastering-a-shrek-game
- https://www.purexbox.com/features/these-20plus-games-are-coming-to-xbox-next-week-october-19-23
- https://www.videogameschronicle.com/news/call-of-duty-modern-warfare-4-pays-tribute-to-late-cod-co-creator-and-infinity-ward-co-founder-vince-zampella/
- https://www.gamespot.com/articles/you-can-play-wow-forever-for-free-next-week-but-theres-a-catch/
- https://www.mmo-champion.com/content/14609-Patch-12-1-7-Echoes-of-the-Worldcore-Overview
- https://www.pushsquare.com/news/2026/10/ps1-classics-on-ps5-keep-on-coming-in-dino-crisis-2-out-next-week
- https://www.videogameschronicle.com/news/konami-boss-says-ai-cant-replace-the-human-chemistry-behind-great-games/
- https://godisageek.com/2026/10/silent-hill-future-games-konami
- https://opencritic.com/news/37836/witcher-studio-s-next-game-gets-major-official-update
- https://www.nintendolife.com/news/2026/10/cult-of-the-lamb-summons-a-switch-2-version-free-upgrade-path-confirmed
- https://www.purexbox.com/news/2026/10/insignia-brings-back-online-multiplayer-for-lots-more-xbox-games-including-burnout-3
- https://www.videogameschronicle.com/news/playstation-6s-memory-costs-alone-exceed-680-per-console-its-claimed/

Movies:
- https://au.variety.com/2026/film/news/australian-box-office-october-19th-street-fighter-41501/
- https://www.hancinema.net/korean_boxoffice.php
- https://sitgesfilmfestival.com/es/noticies/sanguine-marion-corroller-mejor-pelicula-sitges-2026
- https://filmstories.co.uk/news/alex-garland-to-make-a-new-sci-fi-film-at-a24-zendaya-to-star/
- https://horrorhistorian.substack.com/p/asian-horror-film-news-october-18
- https://hd-report.com/2026/10/18/4k-blu-ray-releases-oct-2026/
- https://www.blu-ray.com/news/?id=39202
- https://www.horrorsociety.com/2026/10/08/can-you-escape-the-cube-new-4k-release-from-umbrella-entertainment/
- https://digitalbits.com/reviews/item/aliens-2024-uhd
- https://www.justwatch.com/au/movie/aliens
