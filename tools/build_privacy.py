"""Builds the privacy pages under privacy/ from one template.

Literally Emergency: read from the app's strings.xml (en, nl, de, fr) through the project's own
scripts/make_privacy_page.py, so this site always shows what the app's Privacy screen shows.
Literally Just a Scanner and Literally Plantscan: the texts below, copied from the apps' in-app
privacy screens. Change them here when the app changes, then run this script again.

Usage:  python tools/build_privacy.py [path to LiterallyEmergency project]
"""
import html
import importlib.util
import os
import sys

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
EMERGENCY = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/AndroidStudioProjects/LiterallyEmergency')
EMAIL = 'ulliemoekeproductions@gmail.com'
GOOGLE = '<a href="https://policies.google.com/privacy">Google Privacy Policy</a>'
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'

ADS = ('The Android app uses Google AdMob for ads that you choose to watch, and Google’s User Messaging Platform to '
       'manage advertising privacy choices. These services may process your IP address (including approximate '
       'location), device or advertising identifiers, ad interactions and diagnostic information for advertising, '
       'analytics and fraud prevention. Consent-related requests may occur when the app starts; ads are requested '
       'when you choose to watch one. {}')
ADS_CHOICES = ('Where applicable, you can change consent using “Ad privacy choices” in Support. You can also manage '
               f'your advertising ID in Android settings. Google describes its data handling at {GOOGLE}.')
DONATIONS = ('Donations open PayPal. PayPal handles your payment information under its own privacy policy. The app '
             'does not receive your card or bank details and stores only a local flag to ask whether you completed '
             'the donation. We may receive donor and transaction details through PayPal to manage donations.')
CONTACT = f'For privacy questions or requests concerning information you have provided to us: {MAIL}.'

# Each app: slug, name, icon, accent colour, updated line, short summary tiles, sections [(heading, [html paragraphs])].
APPS = {
    'literally-just-a-scanner': dict(
        name='Literally Just a Scanner', icon='scanner.png', accent='#2f6fe0',
        updated='Updated 18 September 2026',
        summary=[('On your device', 'Scans and PDFs are made on your phone, never uploaded to us.'),
                 ('No account', 'No sign-up or email address needed.'),
                 ('Ads are optional', 'Only when you choose to watch one for a cookie.')],
        sections=[
            ('Your scans', ['Photos, document cropping and PDF creation are processed on your device. We do not upload '
                            'your scans to our servers. Saved files remain in your chosen folder until you delete them. '
                            'When you import from a cloud photo app or share a file, the service you choose handles that '
                            'transfer under its own privacy policy.']),
            ('Optional advertising', [ADS.format('Scanning does not require watching an ad.'), ADS_CHOICES]),
            ('Optional donations', [DONATIONS]),
            ('Accounts, retention and choices', [
                'No scanner account or email address is required. App settings, your digital-cookie collection count '
                'and the donation reminder are stored locally. Digital cookies are in-app collectibles, not browser '
                'tracking cookies. Clearing app data removes these settings and collectibles; files saved in Downloads '
                'or another shared folder must be deleted separately. Advertising and payment providers manage their '
                'own retention. If you contact us by email, we use your message and address to respond and retain '
                'correspondence as needed to handle your request.']),
            ('Contact', [CONTACT]),
        ]),
    'literally-plantscan': dict(
        name='Literally Plantscan', icon='plantscan.svg', accent='#1f9a55',
        updated='Updated 25 September 2026',
        summary=[('Offline recognition', 'Plants are identified on your phone; photos are never uploaded.'),
                 ('No account', 'No sign-up or email address needed.'),
                 ('Ads are optional', 'Only when you choose to watch one for a cookie.')],
        sections=[
            ('Your photos', ['The camera is used only to photograph plants you choose to identify. Plant identification '
                             'runs entirely on your device; photos are never uploaded to our servers or any '
                             'identification service. Scans in your history, including their photos, are stored '
                             'privately inside the app until you delete them.']),
            ('Optional advertising', [ADS.format('Scanning plants does not require watching an ad.'), ADS_CHOICES]),
            ('Optional donations', [DONATIONS]),
            ('Accounts, retention and choices', [
                'No account or email address is required. Your scan history, digital-cookie collection count and the '
                'donation reminder are stored locally. Digital cookies are in-app collectibles, not browser tracking '
                'cookies. Deleting a scan removes it and its photo; clearing app data removes everything. Advertising '
                'and payment providers manage their own retention. If you contact us by email, we use your message and '
                'address to respond and retain correspondence as needed to handle your request.']),
            ('Contact', [CONTACT]),
        ]),
}

EMERGENCY_SUMMARY = {
    'en': [('Stays on your phone', 'Medical info is never sent to us and is left out of backups.'),
           ('End-to-end encrypted', 'Paired alarms and messages can’t be read by our relay.'),
           ('No account', 'No sign-up or email address needed.')],
    'nl': [('Blijft op je telefoon', 'Medische info wordt nooit naar ons gestuurd en zit niet in back-ups.'),
           ('End-to-end versleuteld', 'Gekoppelde alarmen en berichten kan onze relay niet lezen.'),
           ('Geen account', 'Geen registratie of e-mailadres nodig.')],
    'de': [('Bleibt auf deinem Handy', 'Medizinische Infos werden nie an uns gesendet und nicht gesichert.'),
           ('Ende-zu-Ende-verschlüsselt', 'Gekoppelte Alarme und Nachrichten kann unser Relay nicht lesen.'),
           ('Kein Konto', 'Keine Registrierung oder E-Mail-Adresse nötig.')],
    'fr': [('Reste sur votre téléphone', 'Les infos médicales ne nous sont jamais envoyées ni sauvegardées.'),
           ('Chiffré de bout en bout', 'Notre relais ne peut pas lire les alertes et messages appairés.'),
           ('Aucun compte', 'Ni inscription ni adresse e-mail.')],
}
HOME = {'en': 'Home', 'nl': 'Home', 'de': 'Startseite', 'fr': 'Accueil'}


def page(*, lang, depth, title, app, icon, accent, meta, summary, body, switcher=''):
    up = '../' * depth
    tiles = ''.join(f'<div><b>{html.escape(t)}</b>{html.escape(d)}</div>' for t, d in summary)
    return f'''<!doctype html>
<html lang="{lang}" style="--accent:{accent}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} · {html.escape(app)}</title>
  <meta name="description" content="{html.escape(title)} for {html.escape(app)} by UllieMoeke Productions.">
  <link rel="icon" href="{up}assets/favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Inter:wght@400..700&display=swap">
  <link rel="stylesheet" href="{up}assets/style.css">
  <script>try{{var t=localStorage.getItem('theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
  <script src="{up}assets/main.js" defer></script>
</head>
<body>
<div class="progress" aria-hidden="true"></div>
<header class="nav">
  <div class="wrap">
    <a class="logo" href="{up}"><img src="{up}assets/favicon.svg" alt=""><span>UllieMoeke <small>Productions</small></span></a>
    <nav class="nav-links" aria-label="Main">
      <a href="{up}#apps" class="hide-sm">Apps</a>
      <a href="{up}privacy/">Privacy</a>
      <button class="theme-toggle" type="button" aria-label="Toggle theme"></button>
    </nav>
  </div>
</header>
<main>
  <section class="policy-hero">
    <div class="hero-bg" aria-hidden="true"><div class="blob b1"></div><div class="blob b2"></div></div>
    <div class="policy-wrap">
      <div class="crumbs"><a href="{up}">{HOME.get(lang, 'Home')}</a><span>/</span><a href="{up}privacy/">Privacy</a><span>/</span><span>{html.escape(app)}</span></div>
      <div class="policy-title reveal in"><img src="{up}assets/icons/{icon}" alt=""><div><h1>{html.escape(title)}</h1><p class="policy-meta">{html.escape(app)} · {html.escape(meta)}</p></div></div>
      {switcher}
      <div class="summary">{tiles}</div>
    </div>
  </section>
  <article class="policy policy-wrap">
{body}
  </article>
</main>
<footer>
  <div class="wrap legal" style="margin-top:0;border-top:0;padding-top:0">
    <span>© 2026 UllieMoeke Productions</span>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
  </div>
</footer>
</body>
</html>
'''


def write(rel, text):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('wrote', rel)


def build_static_apps():
    for slug, a in APPS.items():
        body = []
        for heading, paras in a['sections']:
            body.append(f'    <h2>{html.escape(heading)}</h2>')
            body += [f'    <p>{p}</p>' for p in paras]  # paragraphs are trusted HTML written above
        write(f'privacy/{slug}/index.html', page(
            lang='en', depth=2, title='Privacy policy', app=a['name'], icon=a['icon'], accent=a['accent'],
            meta=f'UllieMoeke Productions · {a["updated"]}', summary=a['summary'], body='\n'.join(body)))


def build_emergency():
    script = os.path.join(EMERGENCY, 'scripts', 'make_privacy_page.py')
    if not os.path.exists(script):
        print(f'skipped Literally Emergency: {script} not found')
        return
    spec = importlib.util.spec_from_file_location('make_privacy_page', script)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    en = m.load_strings('en')
    for lang in m.LANGUAGES:
        s = m.load_strings(lang) if lang != 'en' else en
        t = lambda key: html.escape(s.get(key) or en[key])
        meta = s.get('ulliemoeke_productions_updated_29_september_2026') or en['ulliemoeke_productions_updated_29_september_2026']
        body = []
        note = s.get('privacy_translation_note', '').strip()
        if lang != 'en' and note:
            body.append(f'    <p class="note">{html.escape(note)}</p>')
        for kind, key in m.SECTIONS:
            if kind == 'h':
                body.append(f'    <h2>{t(key)}</h2>')
            elif kind == 'p':
                body.append(f'    <p>{t(key)}</p>')
            elif kind == 'google':
                body.append(f'    <p>{t(key)}<a href="https://policies.google.com/privacy">{t("google_privacy_policy")}</a>.</p>')
            elif kind == 'mail':
                body.append(f'    <h2>{t("contact")}</h2>')
                body.append(f'    <p>{t(key)}{MAIL}.</p>')
        file = 'index.html' if lang == 'en' else f'{lang}.html'
        links = ''.join(
            f'<b>{name}</b>' if code == lang else f'<a href="{"./" if code == "en" else code + ".html"}" hreflang="{code}">{name}</a>'
            for code, name in m.LANGUAGES.items())
        write(f'privacy/literally-emergency/{file}', page(
            lang=lang, depth=2, title=s.get('privacy_policy') or en['privacy_policy'], app='Literally Emergency',
            icon='emergency.png', accent='#e5322d', meta=meta, summary=EMERGENCY_SUMMARY[lang],
            body='\n'.join(body), switcher=f'<nav class="lang" aria-label="Language">{links}</nav>'))


if __name__ == '__main__':
    build_static_apps()
    build_emergency()
