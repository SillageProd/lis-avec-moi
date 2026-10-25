import pathlib, sys
src = pathlib.Path("/home/claude/lis-avec-moi/source/apercu.html").read_text()
def R(a, b, n=1):
    global src
    c = src.count(a)
    assert c == n, (c, a)
    src = src.replace(a, b)

R("<title>Lis avec moi</title>", "<title>Compte avec moi</title>")
R('content="Lis avec moi"', 'content="Compte avec moi"')
R('const PREFIXE = L("lam_", "lmm_");', 'const PREFIXE = L("cam_", "cmm_");')
# contenu : exercices générés au lieu des mots de l'école
old_start = src.index("  // Copie du Google Sheet de l'école")
old_end = src.index("  const MAX_PROFILS = 6;")
src = src[:old_start] + '''  // Pas de Google Sheet par défaut : les calculs sont créés par l'app selon les exercices choisis
  const LIEN_SHEET_ECOLE = "";
  const LIEN_SHEET_NL = "";
  // ---------- exercices ----------
  // Chaque type crée sa liste de calculs. Types provisoires, en attendant ceux choisis par Robin.
  const suite = (a, b) => Array.from({ length: b - a + 1 }, (_, i) => a + i);
  const TYPES = [
    { id: "nombres20", nom: L("Lire les nombres de 0 à 20", "Getallen lezen van 0 tot 20"), ico: "🔢",
      creer: () => suite(0, 20).map(String) },
    { id: "plus10", nom: L("Additions jusqu'à 10", "Optellen tot 10"), ico: "➕",
      creer: () => suite(0, 10).flatMap(a => suite(0, 10 - a).map(b => `${a} + ${b} =`)) },
    { id: "moins10", nom: L("Soustractions jusqu'à 10", "Aftrekken tot 10"), ico: "➖",
      creer: () => suite(0, 10).flatMap(a => suite(0, a).map(b => `${a} - ${b} =`)) }
  ];
  let typesChoisis = lire("types", ["plus10"]).filter(id => TYPES.some(t => t.id === id));
  const creerCalculs = ids => TYPES.filter(t => ids.includes(t.id)).flatMap(t => t.creer());
  const MOTS_EXEMPLE = creerCalculs(typesChoisis.length ? typesChoisis : ["plus10"]);
  const MOTS_EXEMPLE_NL = MOTS_EXEMPLE;
  // Réponse d'un calcul simple (pour l'adulte), ou null si ce n'est pas un calcul
  function reponseDe(calcul) {
    const e = String(calcul).replace(/=\\s*\\??\\s*$/, "").replace(/[×x]/g, "*").replace(/[÷:]/g, "/").replace(/−/g, "-").replace(/,/g, ".").trim();
    if (!/^[\\d\\s+\\-*/().]+$/.test(e) || !/\\d\\s*[+\\-*/]\\s*[\\d(]/.test(e)) return null;
    try { const v = Function('"use strict"; return (' + e + ")")(); return Number.isFinite(v) ? Math.round(v * 1000) / 1000 : null; } catch (err) { return null; }
  }
''' + src[old_end:]
R('let source = lire("source", { type: "exemple", libelle: "Liste de l\'école (copie du 23/10)", maj: null });',
  'let source = lire("source", { type: "exercices", libelle: "Exercices choisis", maj: null });')
R('if (!Array.isArray(mots) || !mots.length) { mots = nettoyer(MOTS_EXEMPLE); if (!NL) source = { type: "exemple", libelle: "Liste de l\'école (copie du 23/10)", maj: null }; }',
  '''// Exercices choisis : la liste est recréée à chaque ouverture (les nouvelles versions de l'app peuvent changer les calculs)
  if (!Array.isArray(mots) || !mots.length || source.type === "exercices") { mots = nettoyer(MOTS_EXEMPLE); source = { type: "exercices", libelle: "Exercices choisis", maj: source.maj || null }; }''')
R('if (source.type !== "exemple") retenirNouveaux', 'if (source.type !== "exemple" || src.type === "exercices") retenirNouveaux')
R('premiereFois = source.type === "exemple";', 'premiereFois = source.type === "exemple" || source.type === "exercices";')
R('["mot", "mots", "lettre", "lettres", "mots/lettres", "lettres/mots", "liste", "woord", "woorden", "letters"]',
  '["calcul", "calculs", "exercice", "exercices", "mot", "mots", "liste", "som", "sommen"]')
R('ajoutes > 1 ? ajoutes + L(" nouveaux mots à lire !", " nieuwe woorden om te lezen!") : L("1 nouveau mot à lire !", "1 nieuw woord om te lezen!")',
  'ajoutes > 1 ? ajoutes + L(" nouveaux calculs !", " nieuwe sommen!") : L("1 nouveau calcul !", "1 nieuwe som!")')
R('mots.length + " mots et lettres chargés depuis le Google Sheet."', 'mots.length + " calculs chargés depuis le Google Sheet."')
R('mots.length + " mots et lettres importés depuis "', 'mots.length + " calculs importés depuis "')
R('avec un mot ou une lettre par ligne dans la colonne A."', 'avec un calcul par ligne dans la colonne A."')
# libellés « mots » → « calculs »
R('nombreTexte = n => n === "tout" ? L("tous les mots", "alle woorden") : n === "new" ? L("les nouveaux mots", "de nieuwe woorden") : n + L(" mots", " woorden");',
  'nombreTexte = n => n === "tout" ? L("tous les calculs", "alle sommen") : n === "new" ? L("les nouveaux calculs", "de nieuwe sommen") : n + L(" calculs", " sommen");')
R('L("Lis avec moi", "Lees met mij")}</header>', 'L("Compte avec moi", "Reken met mij")}</header>')
R('L("Qui veut lire ?", "Wie wil er lezen?")', 'L("Qui veut compter ?", "Wie wil er rekenen?")')
R('<span class="ico">📖</span><span class="nom">${L("Normal", "Normaal")}</span><span class="sous">${L("Tous les mots, sans se presser", "Alle woorden, zonder haast")}</span>',
  '<span class="ico">🔢</span><span class="nom">${L("Normal", "Normaal")}</span><span class="sous">${L("Tous les calculs, sans se presser", "Alle sommen, zonder haast")}</span>')
R('n === "tout" ? mots.length + L(" mots", " woorden") : n === "new" ? listeNew().length + (listeNew().length > 1 ? L(" mots", " woorden") : L(" mot", " woord")) : L("mots", "woorden")',
  'n === "tout" ? mots.length + L(" calculs", " sommen") : n === "new" ? listeNew().length + (listeNew().length > 1 ? L(" calculs", " sommen") : L(" calcul", " som")) : L("calculs", "sommen")')
R('L("Combien de mots ?", "Hoeveel woorden?")', 'L("Combien de calculs ?", "Hoeveel sommen?")')
R('L(`La liste contient ${mots.length} mots et lettres.`, `De lijst bevat ${mots.length} woorden en letters.`)',
  'L(`La liste contient ${mots.length} calculs.`, `De lijst bevat ${mots.length} sommen.`)')
R('L(`mot${r.justes > 1 ? "s" : ""} juste${r.justes > 1 ? "s" : ""} en`, r.justes === 1 ? "juist woord in" : "juiste woorden in")',
  'L(`bonne${r.justes > 1 ? "s" : ""} réponse${r.justes > 1 ? "s" : ""} en`, r.justes === 1 ? "juist antwoord in" : "juiste antwoorden in")')
R('L("Mots justes en ", "Juiste woorden in ")', 'L("Bonnes réponses en ", "Juiste antwoorden in ")')
R('<span class="ico">📖</span>${L(`Pas encore de partie avec', '<span class="ico">🔢</span>${L(`Pas encore de partie avec')
R('📖 ${avecNombre(L("Normal", "Normaal")', '🔢 ${avecNombre(L("Normal", "Normaal")')
R('legende: r.justes > 1 ? L("mots justes", "juiste woorden") : L("mot juste", "juist woord")',
  'legende: r.justes > 1 ? L("bonnes réponses", "juiste antwoorden") : L("bonne réponse", "juist antwoord")')
R('delta = L("+" + d + (d > 1 ? " mots" : " mot") + " par rapport à la dernière fois", d + (d > 1 ? " woorden" : " woord") + " meer dan de vorige keer");',
  'delta = L("+" + d + (d > 1 ? " bonnes réponses" : " bonne réponse") + " par rapport à la dernière fois", d + (d > 1 ? " juiste antwoorden" : " juist antwoord") + " meer dan de vorige keer");')
# espace parents : choix des exercices + listes de calculs
R('''          <h3>${L("Mots et lettres à lire", "Woorden en letters om te lezen")}</h3>
          <p class="aide"><b>${mots.length}</b> ${L("mots et lettres · " + esc(source.libelle) + maj, "woorden en letters" + (motsPerso.length ? ` (${motsPerso.length} van u)` : "") + maj)}</p>''',
  '''          <h3>${L("Exercices", "Oefeningen")}</h3>
          <p class="aide">${L("Touchez les exercices à proposer. Les calculs sont mélangés à chaque partie.", "Tik op de oefeningen die u wilt aanbieden. De sommen worden bij elk spel door elkaar gehaald.")}</p>
          <div class="choix-types">${TYPES.map(t => `<button data-a="typeExercice" data-v="${t.id}" aria-pressed="${source.type === "exercices" && typesChoisis.includes(t.id)}"><span>${t.ico}</span>${esc(t.nom)}<small>${t.creer().length}</small></button>`).join("")}</div>
          <p class="aide"><b>${mots.length}</b> ${L("calculs · " + esc(source.libelle) + maj, "sommen" + maj)}</p>''')
R('''          <ol class="aide">
            <li>Créez un Google Sheet et écrivez un mot ou une lettre par ligne dans la <b>colonne A</b>.</li>''',
  '''          <ol class="aide">
            <li>Créez un Google Sheet et écrivez un calcul par ligne dans la <b>colonne A</b> (par exemple « 3 + 4 = »).</li>''')
R('<h3>Depuis un Google Sheet (conseillé)</h3>', '<h3>Vos propres calculs depuis un Google Sheet</h3>')
R('<p class="aide">Un mot ou une lettre par ligne dans la colonne A. La liste actuelle est remplacée.</p>', '<p class="aide">Un calcul par ligne dans la colonne A. La liste actuelle est remplacée.</p>')
R('L("Écrire la liste à la main", "Zelf woorden toevoegen")', 'L("Écrire les calculs à la main", "Zelf sommen toevoegen")')
R('L("Un mot ou une lettre par ligne.", "Eén woord of letter per regel. Ze worden toegevoegd aan de lijst van de app.")',
  'L("Un calcul par ligne, par exemple « 3 + 4 = » ou « 12 ». Utilisez + - × ÷.", "Eén som per regel, bijvoorbeeld « 3 + 4 = ». Ze worden toegevoegd aan de lijst van de app.")')
R('"Liste enregistrée : " + mots.length + " mots et lettres."', '"Liste enregistrée : " + mots.length + " calculs."')
R('`Opgeslagen: ${motsPerso.length} eigen woorden, ${mots.length} woorden en letters in totaal.`', '`Opgeslagen: ${motsPerso.length} eigen sommen, ${mots.length} sommen in totaal.`')
R('<li>Créez un nouveau Google Sheet, par exemple « Lis avec moi – résultats ».</li>', '<li>Créez un nouveau Google Sheet, par exemple « Compte avec moi – résultats ».</li>')
R("/* Lis avec moi - synchronisation", "/* Compte avec moi - synchronisation")
R('edition: L("fr", "nl")', 'edition: L("maths-fr", "maths-nl")')
# action : choisir les exercices
R('''    async mettreAJour() {''', '''    typeExercice(el) {
      const id = el.dataset.v;
      if (source.type !== "exercices") typesChoisis = [];
      const choix = typesChoisis.includes(id) ? typesChoisis.filter(x => x !== id) : [...typesChoisis, id];
      if (!choix.length) { statutMots = { ok: false, texte: "Gardez au moins un exercice." }; return afficher(); }
      typesChoisis = TYPES.filter(t => choix.includes(t.id)).map(t => t.id); ecrire("types", typesChoisis);
      appliquerMots(creerCalculs(typesChoisis), { type: "exercices", libelle: "Exercices choisis", maj: new Date().toISOString() });
      if (!NL) { lienSheet = ""; ecrire("lienSheet", ""); }
      statutMots = { ok: true, texte: mots.length + " calculs prêts." };
      afficher();
    },
    async mettreAJour() {''')
# réponse visible pour l'adulte, sur demande
R('<div class="scene"><div class="cadre-mot entre" id="mot"></div><div class="verdict" id="verdict"></div></div>',
  '<div class="scene"><div class="cadre-mot entre" id="mot"></div><div class="verdict" id="verdict"></div><button class="voir-reponse" data-a="voirReponse" id="voirReponse" aria-label="${L("Voir la réponse", "Antwoord tonen")}">👁️</button></div>')
R('''    const c = document.getElementById("compteur"); if (c) c.textContent = (partie.index + 1) + " / " + partie.total;''',
  '''    const c = document.getElementById("compteur"); if (c) c.textContent = (partie.index + 1) + " / " + partie.total;
    const b = document.getElementById("voirReponse"); if (b) { b.hidden = reponseDe(partie.mot) === null; b.textContent = "👁️"; b.classList.remove("ouvert"); }''')
R('''    repondre(el) { repondre(el.dataset.v === "1"); },''', '''    repondre(el) { repondre(el.dataset.v === "1"); },
    // l'adulte peut vérifier la réponse : elle s'affiche discrètement quelques secondes
    voirReponse(el) {
      if (!partie) return;
      const v = reponseDe(partie.mot); if (v === null) return;
      const mot = partie.mot;
      el.textContent = "= " + String(v).replace(".", ","); el.classList.add("ouvert");
      setTimeout(() => { if (partie && partie.mot === mot) { el.textContent = "👁️"; el.classList.remove("ouvert"); } }, 2500);
    },''')
R('''/* fin de partie */''', '''.voir-reponse { position: absolute; right: max(0px, calc(50% - min(44vw, 340px) - 8px)); bottom: -6px; min-width: 52px; height: 52px; padding: 0 12px; border-radius: 999px; background: rgba(255,255,255,.75); box-shadow: var(--ombre); font-size: 22px; font-weight: 700; color: var(--encre-douce); font-variant-numeric: tabular-nums; }
.voir-reponse.ouvert { background: var(--papier); color: var(--cadre); font-size: 24px; }
.choix-types { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; }
.choix-types button { min-height: 64px; border-radius: 18px; background: var(--ciel); border: 4px solid transparent; font-size: 19px; font-weight: 600; display: flex; align-items: center; gap: 10px; padding: 8px 14px; text-align: left; }
.choix-types button span { font-size: 28px; }
.choix-types button small { margin-left: auto; color: var(--encre-douce); font-size: 15px; }
.choix-types button[aria-pressed="true"] { border-color: var(--cadre); background: #eceeff; }

/* fin de partie */''')
R('const VERSION = "1.8.0";', 'const VERSION = "0.1.0";')
pathlib.Path("/home/claude/lis-avec-moi/maths/source/apercu.html").write_text(src)
print("ok")
