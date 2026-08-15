#!/usr/bin/env python3
"""
Génère les pages secondaires du site à partir d'un gabarit unique.

Chaque page est décrite par un dict : slug, titre, description, et un corps
en HTML. Le gabarit apporte l'en-tête, la sortie rapide, le pied de page,
les métadonnées et le rappel du numéro.

    python3 build-pages.py
"""
import pathlib

HERE = pathlib.Path(__file__).parent
SITE = "https://sevrage-tunisie.com"
V = "?v=25"
TEL, TELH = "+216 00 000 000", "+21600000000"
MAIL = "contact@psychiatrie-sevrage.com"

TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Clinique Espoir, El Menzah 9</title>
<meta name="description" content="{desc}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#2B4B9B">
<link rel="canonical" href="{site}/{slug}.html">
<meta property="og:title" content="{title} — Clinique Espoir">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{site}/{slug}.html">
<meta property="og:image" content="{site}/assets/img/entree.jpg">
<link rel="icon" type="image/svg+xml" href="assets/logo/espoir-favicon.svg{v}">
<link rel="stylesheet" href="assets/fonts/fonts.css{v}">
<link rel="stylesheet" href="assets/css/style.css{v}">
</head>
<body>

<button class="quickexit" type="button" title="Quitter ce site immédiatement (ou appuyez deux fois sur Échap)">
  <svg class="ico" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
    <path d="M6 6l12 12M18 6L6 18"/>
  </svg>
  <span>Quitter</span>
</button>

<main class="doc">
  <div class="wrap wrap--narrow">
    <p class="doc__back"><a href="/">← Retour à l'accueil</a></p>
    <h1 class="h2">{h1}</h1>
{body}
    <aside class="doc__call">
      <p><strong>Une question, un doute, une urgence&nbsp;?</strong> Un soignant répond à toute heure.</p>
      <a class="btn btn--call btn--lg" href="tel:{telh}">Appeler le {tel}</a>
      <p class="doc__call-alt">ou écrire à <a href="mailto:{mail}">{mail}</a></p>
    </aside>
  </div>
</main>

<footer class="foot">
  <div class="wrap foot__legal">
    <p>© 2026 Clinique psychiatrique Espoir — El Menzah 9.</p>
    <p class="foot__legalnav">
      <a href="/">Accueil</a>
      <a href="mentions-legales.html">Mentions légales</a>
      <a href="confidentialite.html">Confidentialité</a>
    </p>
  </div>
</footer>

<script src="assets/js/app.js{v}"></script>
</body>
</html>
"""

PAGES = [
    {
        "slug": "il-refuse-de-venir",
        "title": "Il refuse de venir se soigner",
        "h1": "Il refuse de venir. Que faire&nbsp;?",
        "desc": "Un proche dépendant refuse de consulter : comment préparer la conversation, "
                "quoi dire, quoi éviter, et quand l'hospitalisation peut se faire sans son accord.",
        "body": """
    <p class="lede">C'est la situation la plus fréquente, et la plus épuisante. Voici ce que
    l'expérience clinique enseigne — et ce qui, au contraire, referme la porte.</p>

    <h2>Commencez par appeler pour vous</h2>
    <p>Vous n'avez pas besoin de son accord pour demander conseil. Un premier appel sert à
    décrire la situation, mesurer le degré d'urgence et préparer la suite. Beaucoup de familles
    appellent des semaines avant que le patient n'accepte quoi que ce soit&nbsp;: ce temps n'est
    pas perdu, il évite les faux pas.</p>

    <h2>Choisir le moment</h2>
    <ul class="doc__list">
      <li>Jamais pendant l'intoxication&nbsp;: rien de ce qui se dit ne sera retenu.</li>
      <li>Jamais pendant le manque non plus&nbsp;: l'irritabilité rend toute discussion explosive.</li>
      <li>Le meilleur moment est souvent le lendemain d'un épisode difficile, quand le regret
      est encore là — la fenêtre est courte.</li>
    </ul>

    <h2>Ce qui aide</h2>
    <ul class="doc__list">
      <li>Parler de faits, pas de jugements&nbsp;: «&nbsp;tu n'es pas rentré jeudi&nbsp;» plutôt
      que «&nbsp;tu es irresponsable&nbsp;».</li>
      <li>Dire l'effet sur vous, pas sur lui&nbsp;: «&nbsp;j'ai peur&nbsp;», «&nbsp;je ne dors plus&nbsp;».</li>
      <li>Proposer une seule chose, petite et concrète&nbsp;: un rendez-vous, pas une cure.</li>
      <li>Laisser une porte ouverte à chaque fois&nbsp;: «&nbsp;quand tu voudras, c'est possible&nbsp;».</li>
      <li>Se faire accompagner&nbsp;: un frère, un ami, le médecin de famille pèsent souvent
      plus que le conjoint.</li>
    </ul>

    <h2>Ce qui aggrave</h2>
    <ul class="doc__list">
      <li>L'ultimatum que vous ne tiendrez pas&nbsp;: il vous décrédibilise pour la fois suivante.</li>
      <li>Fouiller, jeter les bouteilles, compter les comprimés&nbsp;: cela déplace le conflit
      sur la surveillance et masque la maladie.</li>
      <li>Payer les dettes sans condition, mentir à l'employeur, couvrir les absences&nbsp;:
      chaque conséquence évitée retarde la décision.</li>
      <li>Discuter devant les enfants.</li>
    </ul>

    <h2>Quand l'urgence prime sur le consentement</h2>
    <p>Certains signes ne se négocient pas. Appelez immédiatement&nbsp;:</p>
    <ul class="doc__list doc__list--alert">
      <li>Convulsions, confusion, hallucinations, fièvre pendant un arrêt.</li>
      <li>Idées de mort exprimées, scénario précis, ou tentative évitée de peu.</li>
      <li>Refus total de boire et de manger depuis plus de 24 heures.</li>
      <li>Mise en danger d'autrui, notamment au volant.</li>
    </ul>
    <p>L'hospitalisation se fait en principe avec le consentement du patient. Lorsque son état
    ne le permet pas, la loi tunisienne encadre l'admission à la demande d'un proche&nbsp;:
    la procédure vous est expliquée au téléphone, et elle n'est jamais engagée à la légère.</p>

    <h2>Et si rien ne bouge&nbsp;?</h2>
    <p>Faites-vous suivre vous-même. L'entourage d'une personne dépendante développe
    fréquemment anxiété, insomnie et épuisement. Nous recevons aussi les familles seules,
    et c'est souvent par elles que le soin finit par commencer.</p>
""",
    },
    {
        "slug": "preparer-le-sejour",
        "title": "Préparer le séjour",
        "h1": "Préparer le séjour&nbsp;: ce qu'il faut apporter.",
        "desc": "Documents, affaires personnelles, traitements en cours, ce qui est fourni et ce qui "
                "reste à la maison : la liste complète avant une hospitalisation à la Clinique Espoir.",
        "body": """
    <p class="lede">Une admission se prépare en une demi-heure. Cette liste évite les
    allers-retours et les objets qu'il faudra repartir avec.</p>

    <h2>Les documents</h2>
    <ul class="doc__check">
      <li>Pièce d'identité (CIN ou passeport)</li>
      <li>Carte d'assurance ou de prise en charge, si vous en avez une</li>
      <li>La lettre d'admission du médecin traitant, si elle existe</li>
      <li>Les ordonnances en cours, même anciennes</li>
      <li>Les derniers examens&nbsp;: bilan sanguin, ECG, comptes rendus d'hospitalisation</li>
      <li>Le carnet de santé, si disponible</li>
    </ul>

    <h2>Les traitements</h2>
    <p>Apportez <strong>toutes les boîtes en cours</strong>, y compris celles que vous jugez sans
    importance et celles obtenues sans ordonnance. Le médecin doit connaître la totalité de ce
    qui est pris avant de décider du protocole — c'est une question de sécurité, pas de contrôle.</p>

    <h2>Les affaires personnelles</h2>
    <ul class="doc__check">
      <li>Vêtements confortables pour une semaine, dont une tenue chaude</li>
      <li>Pyjama, sous-vêtements, chaussons</li>
      <li>Nécessaire de toilette sans alcool&nbsp;: savon, shampoing, brosse à dents, dentifrice</li>
      <li>Serviette de toilette</li>
      <li>Lunettes, lentilles, appareil dentaire, appareil auditif</li>
      <li>Un livre, un carnet, un stylo</li>
      <li>Chargeur de téléphone</li>
    </ul>

    <h2>Ce qui reste à la maison</h2>
    <ul class="doc__list">
      <li>Alcool, produits, médicaments non déclarés — y compris «&nbsp;au cas où&nbsp;».</li>
      <li>Objets de valeur, bijoux, sommes importantes.</li>
      <li>Parfums, lotions et solutions hydroalcooliques&nbsp;: ils contiennent de l'alcool.</li>
      <li>Rasoirs et objets tranchants&nbsp;: ils sont mis à disposition et repris après usage.</li>
    </ul>

    <h2>Le téléphone</h2>
    <p>Il n'est pas confisqué. Son usage peut être aménagé les premiers jours, le temps que le
    sommeil se réinstalle et que la pression extérieure retombe — c'est discuté avec vous,
    jamais imposé sans explication.</p>

    <h2>Les visites</h2>
    <p>Les proches sont reçus, aux heures de visite, dès que l'état du patient le permet. Un
    entretien familial est proposé pendant le séjour&nbsp;: il fait partie du traitement, pas de
    la politesse.</p>
""",
    },
    {
        "slug": "glossaire",
        "title": "Glossaire du sevrage",
        "h1": "Les mots qu'on vous dira.",
        "desc": "Craving, delirium tremens, thymorégulateur, hôpital de jour, sevrage médicalisé : "
                "le vocabulaire de l'addictologie et de la psychiatrie, expliqué simplement.",
        "body": """
    <p class="lede">Le vocabulaire médical est une barrière de plus au moment où l'on en a le
    moins besoin. Voici ce que les mots veulent dire.</p>

    <dl class="glossaire">
      <dt>Addictologie</dt>
      <dd>La discipline médicale qui traite les dépendances, avec ou sans produit.</dd>

      <dt>Craving</dt>
      <dd>L'envie irrépressible de consommer. Elle survient par vagues, déclenchée par un lieu,
      une personne, une heure ou une émotion. Elle persiste longtemps après la désintoxication,
      et c'est elle que vise le travail thérapeutique.</dd>

      <dt>Delirium tremens</dt>
      <dd>Complication grave du sevrage alcoolique&nbsp;: confusion, hallucinations, tremblements
      intenses, fièvre, déshydratation. Survient en général entre 48 et 96 heures après l'arrêt.
      C'est une urgence médicale.</dd>

      <dt>Dépendance</dt>
      <dd>État dans lequel l'arrêt provoque des symptômes physiques ou psychiques. Différent de
      l'usage nocif, où la consommation cause des dommages sans syndrome de manque.</dd>

      <dt>Désintoxication</dt>
      <dd>La phase d'élimination du produit. Elle dure quelques jours. C'est la partie courte
      du traitement, souvent confondue avec sa totalité.</dd>

      <dt>Hôpital de jour</dt>
      <dd>Le patient vient le matin et rentre dormir chez lui. Ateliers, entretiens et
      traitements sur la journée, sans rupture avec la maison ni le travail.</dd>

      <dt>Rechute</dt>
      <dd>Reprise de la consommation après une période d'arrêt. Fait partie de l'histoire de la
      plupart des dépendances&nbsp;; ce qui compte est le délai avant de revenir consulter.</dd>

      <dt>Sevrage</dt>
      <dd>L'arrêt du produit et l'ensemble des symptômes qui l'accompagnent. «&nbsp;Sevrage
      médicalisé&nbsp;» signifie que ces symptômes sont traités et surveillés, pas seulement subis.</dd>

      <dt>Substitution</dt>
      <dd>Remplacement d'un opiacé par un médicament de même famille, à effet prolongé et à dose
      contrôlée (méthadone, buprénorphine), pour supprimer le manque sans l'euphorie.</dd>

      <dt>Syndrome de manque</dt>
      <dd>L'ensemble des troubles qui apparaissent à l'arrêt&nbsp;: tremblements, sueurs,
      anxiété, insomnie, nausées. Son intensité dépend du produit, des doses et de l'ancienneté.</dd>

      <dt>Thymorégulateur</dt>
      <dd>Médicament qui stabilise l'humeur, utilisé notamment dans le trouble bipolaire.</dd>

      <dt>TCC — thérapie cognitivo-comportementale</dt>
      <dd>Psychothérapie qui identifie les pensées et situations précédant la consommation, puis
      construit une autre réponse, préparée à l'avance.</dd>

      <dt>Entretien motivationnel</dt>
      <dd>Approche qui fait émerger les raisons propres du patient plutôt que de lui opposer
      celles du soignant. C'est celle qui obtient le plus d'adhésion en addictologie.</dd>

      <dt>Double diagnostic</dt>
      <dd>Association d'une addiction et d'un trouble psychiatrique. Traiter l'une sans l'autre
      expose à la rechute.</dd>
    </dl>
""",
    },
    {
        "slug": "medecins",
        "title": "Adresser un patient",
        "h1": "Vous êtes médecin&nbsp;: adresser un patient.",
        "desc": "Modalités d'adressage à la Clinique Espoir, El Menzah 9 : lettre d'admission, "
                "informations utiles, délais de prise en charge et retour d'information au confrère.",
        "body": """
    <p class="lede">Ligne directe pour les confrères, à toute heure&nbsp;:
    <a href="tel:+21600000000">+216 00 000 000</a>. Un psychiatre rappelle le jour même.</p>

    <h2>Ce que nous prenons en charge</h2>
    <ul class="doc__list">
      <li>Sevrages médicalisés&nbsp;: alcool, benzodiazépines et hypnotiques, opiacés, cannabis,
      cocaïne et stimulants, prégabaline et médicaments détournés, tabac.</li>
      <li>Décompensations psychiatriques aiguës nécessitant une mise à l'abri.</li>
      <li>Double diagnostic addiction / trouble psychiatrique.</li>
      <li>Hôpital de jour et consultations externes, en relais d'une hospitalisation.</li>
    </ul>

    <h2>La lettre d'admission</h2>
    <p>Un courrier bref suffit. Les éléments qui nous font gagner du temps&nbsp;:</p>
    <ul class="doc__check">
      <li>Produit ou produits, doses, ancienneté, dernière prise</li>
      <li>Antécédents de sevrage, de convulsions ou de delirium</li>
      <li>Traitement en cours, y compris automédication</li>
      <li>Antécédents psychiatriques et évaluation du risque suicidaire</li>
      <li>Comorbidités&nbsp;: hépatiques, cardiaques, métaboliques</li>
      <li>Dernier bilan biologique disponible</li>
      <li>Contexte familial et social, et qui est l'interlocuteur</li>
    </ul>
    <p>Adressez-la à <a href="mailto:contact@psychiatrie-sevrage.com">contact@psychiatrie-sevrage.com</a>
    ou remettez-la au patient.</p>

    <h2>Délais</h2>
    <ul class="doc__list">
      <li><strong>Urgence</strong>&nbsp;: évaluation le jour même, admission possible dans la foulée.</li>
      <li><strong>Sevrage programmé</strong>&nbsp;: consultation préalable sous quelques jours,
      puis date fixée avec le patient.</li>
      <li><strong>Consultation simple</strong>&nbsp;: sur rendez-vous.</li>
    </ul>

    <h2>Retour d'information</h2>
    <p>Vous recevez un compte rendu d'entrée, puis un compte rendu de sortie précisant le
    protocole conduit, le diagnostic retenu, le traitement de sortie et le suivi proposé. Le
    patient reste le vôtre&nbsp;: nous prenons le relais d'un épisode, pas de la relation.</p>

    <h2>Transmettre un document</h2>
    <p>Pour envoyer un bilan ou un compte rendu, écrivez à
    <a href="mailto:contact@psychiatrie-sevrage.com">contact@psychiatrie-sevrage.com</a>. Un espace de
    dépôt sécurisé est en préparation&nbsp;; en attendant, évitez d'envoyer des pièces
    identifiantes par messagerie non chiffrée.</p>
""",
    },
    {
        "slug": "rendez-vous",
        "title": "Demander un rendez-vous",
        "h1": "Demander un rendez-vous.",
        "desc": "Demandez un rendez-vous à la Clinique psychiatrique Espoir, El Menzah 9 à Tunis : "
                "consultation, sevrage programmé, hôpital de jour. Réponse le jour même, urgences 24 h/24.",
        "body": """
    <p class="lede">Remplissez ces quelques lignes&nbsp;: nous vous rappelons pour fixer l'heure.
    Si c'est urgent, n'attendez pas — appelez le
    <a href="tel:+21600000000">+216 00 000 000</a>, quelqu'un décroche à toute heure.</p>

    <form class="form form--doc" id="form-rdv" action="envoi.php" method="post" novalidate>\n      <input type="hidden" name="page" value="rendez-vous">
      <div class="form__row">
        <label for="r-pour">Le rendez-vous est pour</label>
        <select id="r-pour" name="pour">
          <option>Moi-même</option>
          <option>Un proche</option>
          <option>Mon patient (je suis médecin)</option>
        </select>
      </div>

      <div class="form__row">
        <label for="r-nom">Votre nom</label>
        <input id="r-nom" name="nom" type="text" autocomplete="name" required>
      </div>

      <div class="form__row form__row--two">
        <div>
          <label for="r-tel">Téléphone</label>
          <input id="r-tel" name="tel" type="tel" inputmode="tel" autocomplete="tel" required>
        </div>
        <div>
          <label for="r-mail">E-mail (facultatif)</label>
          <input id="r-mail" name="email" type="email" autocomplete="email">
        </div>
      </div>

      <div class="form__row">
        <label for="r-motif">Motif</label>
        <select id="r-motif" name="motif">
          <option>Consultation psychiatrique</option>
          <option>Sevrage programmé — alcool</option>
          <option>Sevrage programmé — benzodiazépines ou somnifères</option>
          <option>Sevrage programmé — opiacés</option>
          <option>Sevrage programmé — cannabis, cocaïne ou stimulants</option>
          <option>Sevrage programmé — prégabaline ou médicament détourné</option>
          <option>Addiction sans produit (jeu, écrans)</option>
          <option>Hôpital de jour</option>
          <option>Consultation de suivi après une hospitalisation</option>
        </select>
      </div>

      <fieldset class="form__set">
        <legend>Quels jours vous conviennent&nbsp;?</legend>
        <div class="chips">
          <label><input type="checkbox" name="jours" value="lundi"><span>Lundi</span></label>
          <label><input type="checkbox" name="jours" value="mardi"><span>Mardi</span></label>
          <label><input type="checkbox" name="jours" value="mercredi"><span>Mercredi</span></label>
          <label><input type="checkbox" name="jours" value="jeudi"><span>Jeudi</span></label>
          <label><input type="checkbox" name="jours" value="vendredi"><span>Vendredi</span></label>
          <label><input type="checkbox" name="jours" value="samedi"><span>Samedi</span></label>
        </div>
      </fieldset>

      <fieldset class="form__set">
        <legend>À quel moment&nbsp;?</legend>
        <div class="chips">
          <label><input type="radio" name="creneau" value="matin" checked><span>Matin (8 h – 12 h)</span></label>
          <label><input type="radio" name="creneau" value="apres-midi"><span>Après-midi (14 h – 18 h)</span></label>
          <label><input type="radio" name="creneau" value="indifferent"><span>Indifférent</span></label>
        </div>
      </fieldset>

      <div class="form__row">
        <label for="r-delai">Dans quel délai&nbsp;?</label>
        <select id="r-delai" name="delai">
          <option>Dès que possible</option>
          <option>Cette semaine</option>
          <option>La semaine prochaine</option>
          <option>Dans le mois</option>
        </select>
      </div>

      <div class="form__row">
        <label for="r-msg">Ce que vous souhaitez nous dire (facultatif)</label>
        <textarea id="r-msg" name="message" rows="3"
          placeholder="Quelques lignes suffisent. N'écrivez pas de données médicales détaillées ici."></textarea>
      </div>

      <div class="hp" aria-hidden="true">
        <label for="r-site">Ne remplissez pas ce champ</label>
        <input id="r-site" name="site" type="text" tabindex="-1" autocomplete="off">
      </div>

      <label class="check">
        <input type="checkbox" name="consent" required>
        <span>J'accepte d'être recontacté à propos de cette demande.</span>
      </label>

      <button class="btn btn--call btn--lg btn--block" type="submit">Envoyer la demande</button>
      <p class="form__status" role="status" aria-live="polite"></p>
      <p class="form__legal">Vos informations ne servent qu'à fixer le rendez-vous. Aucun dossier
      médical ne transite par ce formulaire.</p>
    </form>

    <h2>Ce qui se passe ensuite</h2>
    <ul class="doc__list">
      <li>Nous vous rappelons pour confirmer le jour et l'heure — en journée, sous deux heures.</li>
      <li>La première consultation dure environ quarante-cinq minutes.</li>
      <li>Apportez vos ordonnances en cours et vos derniers examens, s'il y en a.</li>
      <li>Un proche peut vous accompagner&nbsp;; il peut aussi rester en salle d'attente.</li>
    </ul>
""",
    },
    {
        "slug": "merci",
        "title": "Demande envoyée",
        "h1": "Votre demande est partie.",
        "robots": "noindex,follow",
        "desc": "Confirmation d'envoi. Un soignant de la Clinique Espoir vous rappelle.",
        "body": """
    <p class="form__status" id="merci-alerte" role="status"></p>

    <p class="lede">Un soignant vous rappelle. En journée, comptez moins de deux heures&nbsp;;
    la nuit, nous rappelons au plus tôt le matin — sauf si vous avez signalé une urgence,
    auquel cas c'est immédiat.</p>

    <h2>Si c'est urgent, n'attendez pas le rappel</h2>
    <p>Appelez directement le <a href="tel:+21600000000">+216 00 000 000</a>. Quelqu'un décroche
    à toute heure. En cas de danger vital, composez le <a href="tel:190">190</a> (SAMU).</p>

    <h2>En attendant</h2>
    <ul class="doc__list">
      <li><a href="preparer-le-sejour.html">Ce qu'il faut apporter</a>, si une hospitalisation
      est envisagée.</li>
      <li><a href="il-refuse-de-venir.html">Il refuse de venir</a>, si vous appelez pour un proche.</li>
      <li><a href="glossaire.html">Le glossaire</a>, pour les mots qu'on vous dira.</li>
    </ul>
    <p><strong>N'arrêtez rien seul en attendant l'appel.</strong> L'arrêt brutal de l'alcool ou
    des benzodiazépines expose à des convulsions.</p>
""",
    },
]


def build():
    for pg in PAGES:
        html = TEMPLATE.format(
            title=pg["title"], desc=pg["desc"], h1=pg.get("h1", pg["title"]),
            body=pg["body"], slug=pg["slug"], site=SITE, v=V,
            tel=TEL, telh=TELH, mail=MAIL,
            robots=pg.get("robots", "index,follow"),
        )
        (HERE / f"{pg['slug']}.html").write_text(html)
        print(f"  {pg['slug']}.html")


if __name__ == "__main__":
    print("Pages secondaires :")
    build()
