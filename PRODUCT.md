# PRODUCT.md — Clinique Espoir Menzah 9

> Written from the user's brief without an interview round (the user asked to build and ship in one pass).
> Lines marked **[À CONFIRMER]** are assumptions authored to make the surface complete; the user replaces them with real facts.

## What it is

**Clinique Psychiatrique Espoir — Menzah 9.** A private psychiatric clinic in El Menzah 9, Tunis,
Tunisia. It admits adults for inpatient stays, day-hospital programmes and outpatient consultations,
and answers emergencies day and night.

French is the primary language of the site (Tunisian private-health convention). Arabic and English
are future surfaces, not this build.

## The mechanism (one sentence)

A small, calm, residential-feeling clinic where a family can get a real human answer the same day —
and see, before they ever arrive, exactly what the place looks like and how admission works.

## Audience and scene

The visitor is almost never the patient. It is a spouse, an adult child, or a parent, on a phone,
at 22:00, after a bad week, frightened and ashamed of being frightened. They have one question:
*what do I do tonight, and will they be treated well?* Second audience: referring GPs and
psychiatrists who need the admission letter route and a phone number.

## What this surface must prove

1. Someone picks up, 24/7.
2. This is a place, not a facade: real rooms, real reception, real entrance.
3. Admission is three understandable steps, not a bureaucracy.
4. The clinic is discreet — no stigma, no clinical coldness.

## Truths

- Name: Clinique Psychiatrique Espoir — Menzah 9
- Domain: `psychiatrie-sevrage.com` (non-www canonical, since 2026-08-15). Hosted on Namecheap Stellar
  under the cPanel account whose primary domain is `sevrage-tunisie.com`; that domain and
  `psychiatrie-tunisie.com` 301-redirect to the site.
- Neighbourhood: El Menzah 9, Tunis
- Email: `contact@psychiatrie-sevrage.com` — the single contact address everywhere on the site, and where the
  forms deliver. Matches the site's own domain (mailbox created 2026-08-15, mail routing forced
  to local so the server delivers form mail directly).
  The form's *sender* stays `contact@sevrage-tunisie.com` (the hosting domain) so mail is not flagged as spam.
- Phone / emergency: `+216 00000000` (placeholder given by the user)
- Real photography supplied by the user: clinic **entrance** (facade with sign) and **reception**
  (lobby with plants and reception desk)

## [À CONFIRMER] — authored to complete the surface, user must verify

- Care lines: hospitalisation libre, hôpital de jour, consultations externes, urgences 24/7
- Conditions treated: troubles de l'humeur, troubles anxieux, troubles psychotiques, addictions,
  troubles du sommeil, troubles de la personnalité, burn-out
- Therapies: psychothérapie individuelle, TCC, thérapie de groupe, art-thérapie, musicothérapie,
  relaxation / méditation, activité physique adaptée
- Team composition and headcount, bed count, room categories, opening hours, insurance/CNAM
- Room photography is illustrative, not the actual rooms (see IMAGE-CREDITS.md)

## Constraints

- Static site, no build step, opens straight in a browser.
- Must read as calmer and more modern than the reference competitor (Clinique Averroès: lavender +
  lime Wix template, Space Grotesk / Poppins, stock-photo trio, one long scroll).
- Accessible: real contrast, keyboard reachable, reduced-motion respected.
- Never present the clinic as an emergency service that replaces SAMU; never invent medical claims.
