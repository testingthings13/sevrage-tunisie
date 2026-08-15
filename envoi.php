<?php
/* ============================================================
   Réception des formulaires — sevrage-tunisie.com
   Envoie la demande à contact@psychiatrie-sevrage.com puis renvoie
   le visiteur sur merci.html.

   Hébergement Namecheap Stellar (cPanel, PHP + mail()).
   ============================================================ */

declare(strict_types=1);

const DEST    = 'contact@psychiatrie-sevrage.com';   // boîte principale : tout arrive ici
const EXPED   = 'contact@sevrage-tunisie.com';       // expéditeur sur le domaine qui héberge le site, sinon spam
const MERCI   = '/merci.html';
const ACCUEIL = '/';

/* Page de remerciement dans la langue du formulaire d'origine.
   Le champ caché « page » sert déjà à localiser les retours d'erreur. */
$page_origine = $_POST['page'] ?? '';
$mercis = [
    'accueil-ar'     => '/merci-ar.html',
    'rendez-vous-ar' => '/merci-ar.html',
    'accueil-en'     => '/merci-en.html',
    'rendez-vous-en' => '/merci-en.html',
];
$merci = is_string($page_origine) ? ($mercis[$page_origine] ?? MERCI) : MERCI;

/* ── Uniquement en POST ─────────────────────────────────── */
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: ' . ACCUEIL, true, 303);
    exit;
}

/* ── Pot de miel : un robot a rempli le champ caché ──────── */
if (!empty($_POST['site'])) {
    header('Location: ' . $merci, true, 303);   // on le remercie et on jette
    exit;
}

/* ── Petite limite de débit, par IP, sans base de données ── */
$ip   = preg_replace('/[^0-9a-f:.]/i', '', $_SERVER['REMOTE_ADDR'] ?? 'x');
$lock = sys_get_temp_dir() . '/rdv_' . md5($ip);
if (is_file($lock) && (time() - filemtime($lock)) < 30) {
    /* On garde quand même une trace : la demande n'est pas perdue.
       Le marqueur ?envoi=doublon permet au site de le dire honnêtement
       au visiteur, au lieu d'afficher une pleine confirmation. */
    @file_put_contents(
        __DIR__ . '/demandes.log',
        '[DOUBLON] ' . date('c') . "\n"
            . mb_substr((string) json_encode($_POST, JSON_UNESCAPED_UNICODE), 0, 4000, 'UTF-8')
            . "\n\n" . str_repeat('=', 60) . "\n\n",
        FILE_APPEND | LOCK_EX
    );
    header('Location: ' . $merci . '?envoi=doublon', true, 303);
    exit;
}

/* ── Nettoyage ──────────────────────────────────────────── */
function clean(string $k, int $max = 500): string {
    $v = $_POST[$k] ?? '';
    if (is_array($v)) { $v = implode(', ', $v); }
    $v = trim((string) $v);
    $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v);   // anti-injection d'en-tête
    return mb_substr($v, 0, $max, 'UTF-8');
}
function bloc(string $k, int $max = 4000): string {
    $v = trim((string) ($_POST[$k] ?? ''));
    return mb_substr($v, 0, $max, 'UTF-8');
}

$nom     = clean('nom', 120);
$tel     = clean('tel', 40);
$email   = clean('email', 160);
$motif   = clean('motif', 160);
$pour    = clean('pour', 80);
$jours   = clean('jours', 160);
$creneau = clean('creneau', 40);
$delai   = clean('delai', 60);
$med_nom     = clean('medecin_nom', 120);
$med_spec    = clean('medecin_specialite', 120);
$med_contact = clean('medecin_contact', 160);
$message = bloc('message');
$page    = clean('page', 200);
$consent = !empty($_POST['consent']);

/* ── Validation minimale ────────────────────────────────── */
if ($nom === '' || $tel === '' || !$consent) {
    /* Retour vers le formulaire d'origine (parcours sans JS) :
       app.js affiche le message ?erreur=champs dans la langue de la page. */
    $retours = [
        'accueil'        => ACCUEIL . '?erreur=champs#contact',
        'accueil-ar'     => '/ar.html?erreur=champs#contact',
        'accueil-en'     => '/en.html?erreur=champs#contact',
        'rendez-vous'    => '/rendez-vous.html?erreur=champs#form-rdv',
        'rendez-vous-ar' => '/ar-rendez-vous.html?erreur=champs#form-rdv',
        'rendez-vous-en' => '/en-appointment.html?erreur=champs#form-rdv',
    ];
    $retour = $retours[clean('page', 200)] ?? ACCUEIL . '?erreur=champs#contact';
    header('Location: ' . $retour, true, 303);
    exit;
}
@touch($lock);   /* la limite de débit ne s'arme qu'après une demande valide */
if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $email = '';
}

/* ── Le message ─────────────────────────────────────────── */
$type   = $jours !== '' || $creneau !== '' ? 'Demande de rendez-vous' : 'Message du site';
$lignes = [
    'Type          : ' . $type,
    'Nom           : ' . $nom,
    'Téléphone     : ' . $tel,
    'E-mail        : ' . ($email !== '' ? $email : '—'),
];
if ($pour    !== '') { $lignes[] = 'Pour          : ' . $pour; }
if ($motif   !== '') { $lignes[] = 'Motif         : ' . $motif; }
if ($jours   !== '') { $lignes[] = 'Jours         : ' . $jours; }
if ($creneau !== '') { $lignes[] = 'Créneau       : ' . $creneau; }
if ($delai   !== '') { $lignes[] = 'Délai         : ' . $delai; }
if ($med_nom !== '' || $med_spec !== '' || $med_contact !== '') {
    $lignes[] = 'Médecin réf.  : ' . implode(' — ', array_filter([$med_nom, $med_spec, $med_contact]));
}

$lignes[] = '';
$lignes[] = 'Message :';
$lignes[] = $message !== '' ? $message : '(aucun)';
$lignes[] = '';
$lignes[] = str_repeat('-', 46);
$lignes[] = 'Reçu le ' . date('d/m/Y à H:i');
$lignes[] = 'Page   : ' . ($page !== '' ? $page : '—');
$lignes[] = 'IP     : ' . $ip;

$corps = implode("\n", $lignes);

/* Objet lisible dans la liste des messages : de quoi rappeler sans ouvrir.
   « Rendez-vous — Amine Ben Salah — +216 52 247 043 — Sevrage alcool ». */
$sujet = $type . ' — ' . $nom . ' — ' . $tel . ($motif !== '' ? ' — ' . $motif : '');

/* Un objet accentué se transporte encodé, et chaque morceau encodé doit tenir
   dans 75 caractères (RFC 2047) : au-delà, certaines boîtes affichent la
   suite en clair, illisible. On coupe donc sur les caractères, jamais au
   milieu d'une lettre accentuée, et on plie avec un retour + espace. */
function objet_mime(string $s): string {
    $lettres = preg_split('//u', $s, -1, PREG_SPLIT_NO_EMPTY);
    if ($lettres === false) { $lettres = [$s]; }

    $morceaux = [];
    $courant  = '';
    foreach ($lettres as $lettre) {
        if (strlen($courant) + strlen($lettre) > 39) {   /* 39 octets → 52 caractères une fois encodés */
            $morceaux[] = $courant;
            $courant    = '';
        }
        $courant .= $lettre;
    }
    if ($courant !== '') { $morceaux[] = $courant; }

    $encodes = [];
    foreach ($morceaux as $morceau) {
        $encodes[] = '=?UTF-8?B?' . base64_encode($morceau) . '?=';
    }
    return implode("\r\n ", $encodes);
}

/* ── La même demande, mise en page ──────────────────────── */
function esc(string $v): string {
    return htmlspecialchars($v, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/* Une ligne du tableau : intitulé discret à gauche, réponse en gras à droite.
   $valeur arrive déjà échappée (elle contient parfois un lien). */
function ligne(string $intitule, string $valeur): string {
    return '<tr>'
        . '<td style="padding:7px 16px 7px 0;color:#5B6472;font-size:13px;white-space:nowrap;vertical-align:top;">'
        . esc($intitule) . '</td>'
        . '<td style="padding:7px 0;color:#12203A;font-size:15px;font-weight:bold;vertical-align:top;">'
        . $valeur . '</td>'
        . '</tr>';
}

$tel_href = preg_replace('/[^0-9+]/', '', $tel);
$rappel   = '<a href="tel:' . esc((string) $tel_href) . '" style="color:#12203A;text-decoration:none;">'
          . esc($tel) . '</a>';

$rangs  = ligne('Nom', esc($nom));
$rangs .= ligne('Téléphone', $rappel);
$rangs .= ligne(
    'E-mail',
    $email !== ''
        ? '<a href="mailto:' . esc($email) . '" style="color:#2B4B9B;">' . esc($email) . '</a>'
        : '<span style="color:#8A93A0;font-weight:normal;">non communiqué</span>'
);
if ($pour    !== '') { $rangs .= ligne('Pour',    esc($pour)); }
if ($motif   !== '') { $rangs .= ligne('Demande', esc($motif)); }
if ($jours   !== '') { $rangs .= ligne('Jours',   esc($jours)); }
if ($creneau !== '') { $rangs .= ligne('Créneau', esc($creneau)); }
if ($delai   !== '') { $rangs .= ligne('Délai',   esc($delai)); }
if ($med_nom !== '' || $med_spec !== '' || $med_contact !== '') {
    $rangs .= ligne('Médecin réf.', esc(implode(' — ', array_filter([$med_nom, $med_spec, $med_contact]))));
}

$bloc_message = $message !== ''
    ? '<div style="margin:22px 0 0;padding:14px 16px;background:#F4F6FB;border-left:3px solid #2B4B9B;'
        . 'border-radius:0 6px 6px 0;color:#12203A;font-size:15px;line-height:1.55;white-space:pre-wrap;">'
        . esc($message) . '</div>'
    : '';

$html = '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
    . '<meta name="viewport" content="width=device-width,initial-scale=1"></head>'
    . '<body style="margin:0;padding:24px 12px;background:#EEF1F7;'
        . 'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">'
    /* Aperçu affiché par la boîte mail avant l'ouverture. */
    . '<div style="display:none;max-height:0;overflow:hidden;opacity:0;">'
        . esc($nom . ' — ' . $tel . ($motif !== '' ? ' — ' . $motif : '')) . '</div>'
    . '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        . 'style="max-width:560px;margin:0 auto;background:#FFFFFF;border-radius:10px;'
        . 'overflow:hidden;border:1px solid #DDE3EF;"><tr><td>'
    . '<div style="padding:16px 24px;background:#2B4B9B;color:#FFFFFF;font-size:15px;font-weight:bold;">'
        . esc($type) . '</div>'
    . '<div style="padding:22px 24px 26px;">'
    . '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="width:100%;">'
        . $rangs . '</table>'
    . $bloc_message
    . '<div style="margin:24px 0 0;padding-top:14px;border-top:1px solid #E6EAF3;'
        . 'color:#8A93A0;font-size:12px;line-height:1.7;">'
        . 'Reçu le ' . esc(date('d/m/Y à H:i')) . '<br>'
        . 'Page : ' . esc($page !== '' ? $page : '—') . '<br>'
        . 'IP : ' . esc($ip)
        . '</div>'
    . '</div></td></tr></table></body></html>';

/* ── En-têtes ───────────────────────────────────────────── */
/* Le nom du visiteur peut porter des accents ou de l'arabe : on l'encode. */
$repondre = $email !== ''
    ? '=?UTF-8?B?' . base64_encode($nom) . '?= <' . $email . '>'
    : EXPED;

$frontiere = 'bnd_' . bin2hex(random_bytes(12));

$headers = [
    'MIME-Version: 1.0',
    'From: Site sevrage-tunisie.com <' . EXPED . '>',
    'Reply-To: ' . $repondre,
    'Content-Type: multipart/alternative; boundary="' . $frontiere . '"',
    'X-Mailer: PHP/' . phpversion(),
];

/* Deux versions du même message : le texte pour les boîtes qui refusent
   le HTML, la mise en page pour les autres. La dernière l'emporte. */
$corps_mime = '--' . $frontiere . "\r\n"
    . "Content-Type: text/plain; charset=UTF-8\r\n"
    . "Content-Transfer-Encoding: base64\r\n\r\n"
    . chunk_split(base64_encode($corps)) . "\r\n"
    . '--' . $frontiere . "\r\n"
    . "Content-Type: text/html; charset=UTF-8\r\n"
    . "Content-Transfer-Encoding: base64\r\n\r\n"
    . chunk_split(base64_encode($html)) . "\r\n"
    . '--' . $frontiere . "--\r\n";

$ok = @mail(
    DEST,
    objet_mime($sujet),
    $corps_mime,
    implode("\r\n", $headers),
    '-f' . EXPED
);

/* ── Trace locale : si l'e-mail échoue, rien n'est perdu ── */
$journal = __DIR__ . '/demandes.log';
@file_put_contents(
    $journal,
    ($ok ? "[OK] " : "[ÉCHEC MAIL] ") . date('c') . "\n" . $corps . "\n\n" . str_repeat('=', 60) . "\n\n",
    FILE_APPEND | LOCK_EX
);

header('Location: ' . $merci . ($ok ? '' : '?envoi=differe'), true, 303);
exit;
