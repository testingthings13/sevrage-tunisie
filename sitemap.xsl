<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:sm="http://www.sitemaps.org/schemas/sitemap/0.9"
                xmlns:xhtml="http://www.w3.org/1999/xhtml"
                exclude-result-prefixes="sm xhtml">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html lang="fr">
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>Plan du site — Clinique Espoir, El Menzah 9</title>
        <style>
          :root{
            --bleu:#2B4B9B; --bleu-vif:#3F6BD4; --bleu-wash:#EDF2FA;
            --pierre:#F5F7F6; --trait:#DDE2DE; --ink:#101B22; --ink-2:#4E5D66; --teal:#0E9BA8;
          }
          *{ box-sizing:border-box }
          body{
            margin:0; background:var(--pierre); color:var(--ink);
            font:400 15px/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
            padding:clamp(16px,4vw,48px);
          }
          .card{
            max-width:980px; margin:0 auto; background:#fff;
            border:1px solid var(--trait); border-radius:18px; overflow:hidden;
            box-shadow:0 2px 6px rgba(16,34,47,.08), 0 28px 50px -32px rgba(16,34,47,.35);
          }
          header{
            background:linear-gradient(135deg, var(--bleu) 0%, var(--bleu-vif) 100%);
            color:#fff; padding:clamp(20px,4vw,36px);
          }
          header h1{ margin:0 0 .3rem; font-size:clamp(1.3rem,2.6vw,1.8rem); letter-spacing:-.02em }
          header p{ margin:0; opacity:.85; font-size:.92rem }
          table{ width:100%; border-collapse:collapse }
          th{
            text-align:left; font-size:.72rem; letter-spacing:.08em; text-transform:uppercase;
            color:var(--ink-2); background:var(--bleu-wash);
            padding:.7rem 1.1rem; border-bottom:1px solid var(--trait);
          }
          td{ padding:.65rem 1.1rem; border-bottom:1px solid var(--trait); vertical-align:middle }
          tr:last-child td{ border-bottom:0 }
          tr:hover td{ background:var(--bleu-wash) }
          a{ color:var(--bleu); text-decoration:none; font-weight:500; word-break:break-all }
          a:hover{ text-decoration:underline }
          .date{ white-space:nowrap; color:var(--ink-2); font-variant-numeric:tabular-nums }
          .prio{
            display:inline-block; min-width:2.6rem; text-align:center;
            padding:.12rem .5rem; border-radius:999px; font-size:.8rem; font-weight:600;
            background:var(--bleu-wash); color:var(--bleu);
          }
          .prio--haute{ background:var(--bleu); color:#fff }
          .lang{
            display:inline-block; margin-inline-end:.3rem;
            padding:.08rem .45rem; border:1px solid var(--trait); border-radius:6px;
            font-size:.72rem; font-weight:600; color:var(--ink-2); text-transform:uppercase;
          }
          footer{ padding:.9rem 1.1rem; font-size:.8rem; color:var(--ink-2); background:var(--bleu-wash) }
          @media (max-width:640px){ .col-lang{ display:none } }
        </style>
      </head>
      <body>
        <div class="card">
          <header>
            <h1>Plan du site — Clinique Espoir</h1>
            <p>
              sevrage-tunisie.com · El Menzah 9, Tunis ·
              <xsl:value-of select="count(sm:urlset/sm:url)"/> pages indexées
            </p>
          </header>
          <table>
            <thead>
              <tr>
                <th>Page</th>
                <th>Modifiée le</th>
                <th>Priorité</th>
                <th class="col-lang">Langues</th>
              </tr>
            </thead>
            <tbody>
              <xsl:for-each select="sm:urlset/sm:url">
                <xsl:sort select="sm:priority" order="descending" data-type="number"/>
                <tr>
                  <td>
                    <a href="{sm:loc}">
                      <xsl:choose>
                        <xsl:when test="substring-after(sm:loc, 'sevrage-tunisie.com/') = ''">Accueil /</xsl:when>
                        <xsl:otherwise><xsl:value-of select="substring-after(sm:loc, 'sevrage-tunisie.com/')"/></xsl:otherwise>
                      </xsl:choose>
                    </a>
                  </td>
                  <td class="date"><xsl:value-of select="sm:lastmod"/></td>
                  <td>
                    <xsl:choose>
                      <xsl:when test="number(sm:priority) &gt;= 0.9">
                        <span class="prio prio--haute"><xsl:value-of select="sm:priority"/></span>
                      </xsl:when>
                      <xsl:otherwise>
                        <span class="prio"><xsl:value-of select="sm:priority"/></span>
                      </xsl:otherwise>
                    </xsl:choose>
                  </td>
                  <td class="col-lang">
                    <xsl:for-each select="xhtml:link[@hreflang != 'x-default']">
                      <span class="lang"><xsl:value-of select="@hreflang"/></span>
                    </xsl:for-each>
                  </td>
                </tr>
              </xsl:for-each>
            </tbody>
          </table>
          <footer>
            Ce fichier est le sitemap XML lu par les moteurs de recherche ;
            cette présentation n'est qu'un habillage pour les visiteurs humains.
          </footer>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
