<?php
/* ============================================================
   Réception des formulaires — sevrage-tunisie.com
   Envoie la demande à contact@sevrage-tunisie.com puis renvoie
   le visiteur sur merci.html.

   Hébergement Namecheap Stellar (cPanel, PHP + mail()).
   ============================================================ */

declare(strict_types=1);

const DEST    = 'contact@sevrage-tunisie.com';
const EXPED   = 'contact@sevrage-tunisie.com';   // doit être sur le domaine, sinon spam
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
    /* On garde quand même une trace : la demande n'est pas perdue. */
    @file_put_contents(
        __DIR__ . '/demandes.log',
        '[DOUBLON] ' . date('c') . "\n"
            . mb_substr((string) json_encode($_POST, JSON_UNESCAPED_UNICODE), 0, 4000, 'UTF-8')
            . "\n\n" . str_repeat('=', 60) . "\n\n",
        FILE_APPEND | LOCK_EX
    );
    header('Location: ' . $merci, true, 303);
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
$lignes[] = 'Page   : ' . clean('page', 200);
$lignes[] = 'IP     : ' . $ip;

$corps = implode("\n", $lignes);
$sujet = sprintf('[%s] %s — %s', $type, $nom, $motif !== '' ? $motif : 'sans motif');

/* ── En-têtes ───────────────────────────────────────────── */
$headers = [
    'From: Site sevrage-tunisie.com <' . EXPED . '>',
    'Reply-To: ' . ($email !== '' ? $nom . ' <' . $email . '>' : EXPED),
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: PHP/' . phpversion(),
];

$ok = @mail(
    DEST,
    '=?UTF-8?B?' . base64_encode($sujet) . '?=',
    $corps,
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
