# Football All-in-One — working mockup

A browsable mockup of the platform described in the brief: live scores, player
and club profiles, a league table, and the recruitment search the brief calls
its commercial core. **Every club, player, match and figure is invented.**

```
donnees.py       the invented dataset, generated deterministically
build.py         writes the 257 pages
assets/site.css  one stylesheet, no framework, no font from anywhere else
tests/verif.py   197 checks in a real browser
```

`python3 build.py` regenerates everything. **Never edit a `.html` by hand** —
it is overwritten on the next build, and the corrected version would be the one
nobody looks at.

## Why the data is invented

Not for lack of time. Three reasons, in order of what they cost:

1. **Real football data is rented.** Live scores, statistics, xG, market
   values, transfers — nobody produces these themselves. They come from a
   provider under contract (Opta/Stats Perform, Sportradar, SportMonks,
   API-Football and others), with a monthly cost that scales with coverage and
   refresh rate. The brief says so itself at point 24.
2. **A player is a person.** Date of birth, wages, market value and above all
   **injuries** are personal data; injuries are health data under Article 9 of
   the GDPR. The brief already hedges this at point 4 — "if legally available".
3. **Clubs and competitions are trademarks.** Badges, names, shirts.

So: invented clubs, invented players, invented figures — and **every page says
so at the top, in red**. The brief named real people and real clubs as
examples; reproducing those would have published invented personal data about
people who exist. The suite checks all nine sampled pages for thirteen real
names and fails if one appears.

The numbers are still **internally consistent**: nobody scores more goals than
they had shots on target, plays more minutes than matches × 90, and every
league row satisfies `played = W+D+L` and `points = 3W+D`. A mockup with
impossible numbers does not get read — the eye stops on the absurdity instead
of judging the interface.

## What is actually working

The **recruitment filter** is not a picture. Fourteen criteria — position,
nationality, age range, foot, minimum height, maximum value, minimum goals,
contract end, availability, name — combine, run against all 240 players and
respond as you type. That is the part of the brief that depends on no
external provider, so it is the part worth showing first.

The live-score tabs (all / live / finished / upcoming) filter for real too.

## Verification

`python3 tests/verif.py http://127.0.0.1:8921` — **197 checks, 0 failures.**

The one that matters: the filter's results are compared against a **recomputation
done independently from `donnees.py`**, sharing no code with the page. Five
criteria combined the way a club would actually type them (centre-back, 18–24,
over 1.85 m, available) must return exactly the same set both ways, and every
name shown must genuinely satisfy all five.

### The suite is proved able to fail

One of the five conditions was neutralised in the built page. The combination
went from 2 matches to 6 and the suite named three players who did not belong
in the result. That is precisely the commercial failure mode — a club shown
players who do not meet its criteria — so it is the one that had to be proved
catchable.

Also checked: the truncated list **says how many it is hiding** ("240 match —
showing the first 40, 200 more not shown"), because a silently capped list
reads as a complete one; an empty result says so instead of showing a blank
column; and the mockup's vocabulary of blank (`To be sourced`) is never mixed
with the one belonging to another product.

One trap worth recording: `.tbd` carries `text-transform:uppercase`, so the
rendered text is `TO BE SOURCED`. A case-sensitive search failed the check that
looked for it — and, far worse, made six checks looking for *other* products'
wording pass without measuring anything, since those could not have been found
either. Everything compares in lower case now, with a positive control proving
the search can still find a label.

## What this cannot be until one decision is made

Which data provider, and at what coverage. It sets the database, the update
mechanism and the monthly cost, and sections 3, 4, 5, 11, 12 and 24 of the
brief all wait on it. The recruitment half — sections 6, 7, 9, 18, 19, 20, 21,
22 — waits on nobody.
