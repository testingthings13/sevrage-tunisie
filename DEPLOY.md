# Mettre le site en ligne — sevrage-tunisie.com sur Namecheap Stellar

Le site est statique : aucun serveur, aucune base de données, aucun build à faire
sur l'hébergeur. On copie des fichiers, on active le HTTPS, c'est tout.

Comptez **une heure**, plus le temps de propagation DNS (de 30 minutes à 24 heures).

---

## 1 · Le domaine

Si `sevrage-tunisie.com` n'est pas encore acheté : achetez-le chez **Namecheap**, même
compte que l'hébergement. Cela évite toute manipulation DNS — les deux se relient seuls.

Si vous l'achetez ailleurs, il faudra pointer les nameservers vers ceux que Namecheap
affiche dans **Hosting List → Manage → Server Information** (du type
`dns1.namecheaphosting.com`, `dns2.namecheaphosting.com`).

## 2 · Rattacher le domaine à l'hébergement

Dans le tableau de bord Namecheap :

1. **Hosting List → Manage → Go to cPanel**.
2. Si `sevrage-tunisie.com` est le **domaine principal** de l'offre Stellar, il n'y a rien
   à faire : sa racine est déjà `public_html`.
3. Sinon, cPanel → **Domains → Create A New Domain**, saisissez `sevrage-tunisie.com`,
   **décochez** « Share document root » et laissez le dossier proposé
   (`/home/…/sevrage-tunisie.com`). Retenez ce chemin : c'est là qu'iront les fichiers.

## 3 · Envoyer les fichiers

cPanel → **File Manager** → ouvrez `public_html` (ou le dossier de l'étape 2).

Le plus simple : compressez le dossier du projet en `.zip` **sans le dossier parent**,
envoyez-le avec **Upload**, puis clic droit → **Extract**.

### À envoyer

```
index.html   ar.html   en.html   404.html
.htaccess    robots.txt   sitemap.xml
assets/      (css, js, fonts, img, logo)
```

### À NE PAS envoyer

```
logos.html   logo-derive.html   ref-logo.png     ← pages de travail
build-langs.py   README.md   DEPLOY.md   PRODUCT.md   IMAGE-CREDITS.md
.claude/   .git/
```

> Le File Manager masque les fichiers commençant par un point. Pour voir `.htaccess` :
> **Settings** (en haut à droite) → cochez **Show Hidden Files (dotfiles)**.
> Sans ce fichier, pas de redirection HTTPS et pas de page 404 personnalisée.

## 4 · Activer le HTTPS

cPanel → **SSL/TLS Status** → sélectionnez le domaine → **Run AutoSSL**.
Attendez que la pastille passe au vert (quelques minutes). Le certificat est gratuit
et se renouvelle seul.

Vérifiez ensuite que `http://sevrage-tunisie.com` bascule bien sur
`https://sevrage-tunisie.com` — c'est le `.htaccess` qui s'en charge.

## 5 · L'adresse e-mail

cPanel → **Email Accounts → Create** → `contact@sevrage-tunisie.com`.

> C'est l'adresse écrite partout sur le site : formulaire de contact, pied de page,
> données structurées, lettres d'admission des confrères. **Tant que la boîte n'existe
> pas dans cPanel, les messages rebondissent** — créez-la avant d'annoncer le site.

Pour recevoir sur Gmail : cPanel donne les réglages IMAP/SMTP dans
**Email Accounts → Connect Devices**.

## 6 · Vérifier que tout répond

Dans l'ordre, sur votre téléphone et sur un ordinateur :

- [ ] `https://sevrage-tunisie.com` s'affiche, cadenas vert
- [ ] `http://` et `www.` redirigent bien vers l'adresse unique
- [ ] `https://sevrage-tunisie.com/ar.html` s'affiche de droite à gauche
- [ ] `https://sevrage-tunisie.com/en.html` s'affiche en anglais
- [ ] `https://sevrage-tunisie.com/robots.txt` et `/sitemap.xml` répondent
- [ ] une adresse inventée (`/nimportequoi`) affiche la page 404 du site
- [ ] le bouton **Appeler** compose bien le numéro depuis un téléphone

## 7 · Déclarer le site à Google

1. **Google Search Console** → *Add property* → **Domain** → `sevrage-tunisie.com`.
   La validation demande un enregistrement TXT : Namecheap → **Domain List → Manage →
   Advanced DNS → Add New Record → TXT Record**, hôte `@`, valeur fournie par Google.
2. Une fois validé : **Sitemaps** → soumettez `sitemap.xml`.
3. **URL Inspection** sur la page d'accueil → *Request indexing*.
4. Faites de même sur **Bing Webmaster Tools** (import direct depuis Search Console).

## 8 · La fiche Google — l'étape la plus rentable

Créez la **fiche d'établissement Google** de la clinique :
nom réel, adresse exacte à El Menzah 9, catégorie *Centre de désintoxication* ou
*Hôpital psychiatrique*, horaires **ouvert 24 h/24**, téléphone, photos (l'entrée et la
réception sont déjà dans `assets/img/`), et le site `https://sevrage-tunisie.com`.

Google vérifie l'adresse par courrier ou par téléphone. Pour les recherches locales du
type « clinique psychiatrique Tunis », c'est cette fiche qui décide du classement —
pas le site. Aucune optimisation de page ne remplace cette étape.

---

## Mettre à jour le site plus tard

1. Modifiez `index.html` (le français est la source de vérité).
2. Ajoutez la traduction de toute phrase nouvelle dans le tableau `T` de `build-langs.py`.
3. `python3 build-langs.py` régénère `ar.html` et `en.html`.
4. Si vous avez touché au CSS ou au JS, incrémentez le `?v=` (10 → 11, etc.) dans `index.html`,
   puis relancez le script — sinon les visiteurs gardent l'ancienne version en cache.
5. Renvoyez les fichiers modifiés dans le File Manager.
