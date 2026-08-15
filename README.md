# Clinique psychiatrique Espoir — El Menzah 9

Site vitrine en français, statique (HTML + CSS + JS, aucun build).

## Lancer le site

```bash
python3 -m http.server 4319
```

Puis ouvrir <http://localhost:4319>. Le site fonctionne aussi en ouvrant `index.html`
directement, hors ligne : polices, images et styles sont tous locaux.

## Structure

```
index.html            la page entière
assets/css/style.css  le système visuel (couleurs, type, composants, motion)
assets/js/app.js      menu mobile, révélations au scroll, barre de progression,
                      tracé du parcours de sevrage, formulaire de contact
assets/img/           photographies
assets/fonts/         Bricolage Grotesque, Archivo, Noto Kufi Arabic (auto-hébergées)
PRODUCT.md            ce que le site affirme, et ce qui reste à confirmer
IMAGE-CREDITS.md      origine et licence de chaque image
```

## La palette vient de la clinique

Les couleurs sont échantillonnées directement sur la photographie de l'entrée :
le bleu de l'enseigne (`#2B4B9B`), le verre fumé de la porte (`#10222F`), la marche
en marbre et la façade (`#F5F7F6`, `#E8EBE6`), le ciel dans la vitre (`#8EACC6`).

## ⚠️ À vérifier avant mise en ligne

Le contenu médical a été rédigé pour que la page soit complète et crédible. Il doit
être relu et validé par la direction de la clinique. Concrètement :

| Où | Quoi |
|---|---|
| **Tout le contenu clinique** | Descriptions du manque, protocoles, molécules citées (benzodiazépines, vitamine B1, méthadone, buprénorphine), durées, descriptions des troubles : rédigés pour être justes et prudents, mais **à relire et valider par un médecin** avant publication. |
| Coordonnées | `+216 00 000 000` est le numéro provisoire fourni. L'adresse exacte (rue, numéro) manque : seul « El Menzah 9 » est indiqué. |
| E-mail | `contact@psychiatrie-sevrage.com` est l'adresse unique du site (pages, données structurées, destinataire des formulaires). La boîte doit exister dans cPanel, sinon les demandes se perdent. |
| Horaires | Le site n'affiche plus d'horaires&nbsp;: la clinique est présentée ouverte 24 h/24, 7 j/7, pour toute situation (demande du client, 2026-08-15). |
| Durées de sevrage | Jours 1–7, semaines 1–3, suivi 3–12 mois, et les durées par substance : indicatives, à valider. |
| Substances traitées | Vérifier que la clinique prend bien en charge chacune des sept lignes affichées. |
| Avant / après | L'illustration `Jour 0 / Semaine 6` est un dessin, pas un patient : elle représente un profil d'évolution, et la page le dit explicitement. Ne pas la remplacer par une photo de patient. |
| Questions fréquentes | La réponse sur l'admission à la demande d'un tiers renvoie au cadre légal tunisien sans le citer : à faire relire. |
| Tarifs | Aucun tarif n'est affiché — c'est volontaire. |
| Photos | Seules l'entrée et la réception sont les vraies photos. Voir `IMAGE-CREDITS.md`. |
| Plan | Le marqueur OpenStreetMap est centré sur El Menzah 9, pas sur l'adresse exacte. |
| 190 | Le numéro du SAMU tunisien est affiché deux fois — vérifier qu'il est toujours d'actualité. |

## Référencement (SEO)

### Ce qui est fait dans le code

- Titre et description orientés requêtes réelles («&nbsp;cure de sevrage alcool et drogue à Tunis&nbsp;»),
  différents dans les trois langues.
- `<h1>` porteur des mots-clés, en plus de la phrase d'accroche.
- Données structurées JSON-LD : `MedicalClinic` + `LocalBusiness` (adresse, géolocalisation,
  téléphone, ouverture 24 h/24, neuf actes listés, zones desservies) et `FAQPage` sur les six
  questions — c'est ce qui permet d'apparaître en résultat enrichi.
- `canonical` propre à chaque langue, `hreflang` croisés, `robots.txt`, `sitemap.xml`.
- Open Graph et Twitter Card avec une vraie photographie.
- Contenu long et spécifique (onze substances détaillées, sept troubles, protocole, FAQ) :
  c'est le principal atout face aux concurrents.

### ⚠️ À faire avant que ça serve à quelque chose

1. ~~Remplacer le domaine.~~ **Fait (2026-08-15).** L'adresse canonique du site est
   `https://psychiatrie-sevrage.com` — canonical, hreflang, Open Graph, JSON-LD, sitemap et
   robots.txt pointent tous vers elle. `sevrage-tunisie.com` (domaine principal du compte
   cPanel) et `psychiatrie-tunisie.com` font une 301 vers le site (`.htaccess`).
2. **Créer la fiche Google Business Profile** de la clinique (adresse exacte, horaires 24 h/24,
   photos, catégorie « hôpital psychiatrique » ou « centre de désintoxication »). Pour les
   requêtes locales du type « clinique psychiatrique Tunis », c'est la fiche qui décide du
   classement, pas le site. C'est l'action la plus rentable de la liste.
3. **Déclarer le site** dans Google Search Console et y soumettre `sitemap.xml`.
4. **Obtenir des liens** : annuaires médicaux tunisiens, ordre des médecins, presse locale,
   associations d'entraide. C'est le facteur qui manque le plus à un site neuf.

### Le paysage concurrentiel, en clair

Les requêtes «&nbsp;cure de désintoxication Tunisie&nbsp;» sont tenues par des **agences de tourisme
médical** (medespoir, tunisie-esthetic, aram-clinique, medassistance), pas par des cliniques.
Elles visent le prix et le patient européen. Deux conséquences :

- Sur ces requêtes commerciales, elles ont des années d'avance en netlinking.
- Sur les requêtes **informationnelles** («&nbsp;symptômes du sevrage alcoolique&nbsp;», «&nbsp;combien de
  temps dure un sevrage&nbsp;», «&nbsp;arrêter la prégabaline&nbsp;»), leur contenu est mince et le vôtre
  est nettement meilleur. C'est là que ce site peut gagner, et c'est de là que viennent les
  patients locaux.

Attention aussi : `clinique-lespoir.com` est aujourd'hui référencé comme clinique de **chirurgie
esthétique**. Un nom proche sur un autre métier rendra la distinction plus difficile ; le nom de
domaine et la fiche Google devront lever l'ambiguïté.

**Aucun prestataire ne peut garantir la première place sur Google.** Ce qui est livré ici est la
part technique et éditoriale, faite correctement. Le reste — fiche Google, liens, ancienneté du
domaine, avis patients — se construit sur plusieurs mois.

## Trois langues

| Page | Langue | Sens |
|---|---|---|
| `index.html` | Français (source de vérité) | LTR |
| `ar.html` | العربية | RTL, `dir="rtl"` |
| `en.html` | English | LTR |

Le sélecteur FR · ع · EN est dans l'en-tête et dans le menu mobile. Les trois pages
partagent la même feuille de style et le même script.

**Ne modifiez jamais `ar.html` ni `en.html` à la main** : ils sont générés.
Modifiez `index.html`, ajoutez la traduction de toute phrase nouvelle dans le tableau
`T` de `build-langs.py`, puis :

```bash
python3 build-langs.py
```

Le script signale toute phrase française qu'il n'a pas su retrouver. Les traductions
médicales arabe et anglaise sont à faire relire au même titre que le français.

## Le logo

« L'aube dans l'arche » : la porte de la clinique, avec un soleil qui se lève à l'intérieur.
Fichiers et règles d'usage dans [`assets/logo/`](assets/logo/README.md) — signe, version
réservée, pastille, logotype horizontal. Le signe est défini une seule fois, dans le
`<g id="mark">` en haut de `index.html` ; le changer là le change partout.

`logos.html` présente les quatre pistes étudiées (le point du jour, le battement qui
s'apaise, la boucle ouverte, l'aube dans l'arche), chacune testée en grand, en pastille,
en 18 px et en réserve. Page de travail : à supprimer avant mise en ligne.

## Le formulaire de contact

Il n'envoie rien à un serveur : à la validation, il ouvre la messagerie du visiteur
avec le message déjà rédigé vers l'adresse de la clinique. Pour un vrai envoi,
brancher `assets/js/app.js` sur un service de formulaire (Formspree, Vercel Functions,
etc.) à l'endroit marqué `Contact form`.

## Accessibilité et performance

- Lien d'évitement, navigation au clavier, focus visible, `aria-expanded` sur le menu.
- `prefers-reduced-motion` respecté : toutes les animations sont désactivées.
- Les révélations au scroll ont un filet de sécurité de 4 s — aucun contenu ne peut
  rester invisible si le JavaScript échoue ou est bloqué.
- Images en `loading="lazy"`, dimensions déclarées, polices auto-hébergées en woff2.
