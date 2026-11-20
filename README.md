# news-image-20261120

[![news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/VeeGee27/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/VeeGee27/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

One image that sums up Friday 20 November 2026 in world news: 36 stories
across 6 continents, every figure sourced, for make.fun's
[“Sum up 20 November's world news in one image”](https://make.fun/bounty/news-image-20261120)
bounty ($250 in USDC).

## The image

`entry.png` (1024×1024) is a newspaper front page: masthead and date,
a six-stat strip, three hero stories (Kyiv bridges hit, Cyclone Akvan,
COP31 ends with no deal), eight illustrated mid stories, a numbered world
map covering all 36 stories, and a 25-item also-on list — every story
carrying its source.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` is standard library only: it copies the pre-rendered
`entry.png` into the output directory (the grading container has no
third-party packages). `draw.py` renders the image with Pillow at build
time; running it twice produces byte-identical output.

## License

MIT. See [LICENSE](LICENSE).
