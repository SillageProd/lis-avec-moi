// Lis avec moi : garde les profils et les résultats des enfants pour les partager
// entre l'iPad et l'iPhone. À coller dans Extensions > Apps Script d'un Google Sheet.
const ONGLETS = {
  Profils: ["id", "nom", "animal", "couleur"],
  Resultats: ["id", "profil", "mode", "duree", "nombre", "justes", "faux", "total", "tempsMs", "date"],
  Supprimes: ["id"]
};

function feuille(nom) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let f = ss.getSheetByName(nom);
  if (!f) {
    f = ss.insertSheet(nom);
    f.getRange("A:Z").setNumberFormat("@"); // tout en texte, pour garder les valeurs telles quelles
    f.appendRow(ONGLETS[nom]);
  }
  return f;
}

function lireTout(nom) {
  const valeurs = feuille(nom).getDataRange().getValues();
  const titres = valeurs.shift();
  return valeurs.filter(l => l[0] !== "").map(l => {
    const o = {};
    titres.forEach((t, i) => o[t] = l[i]);
    return o;
  });
}

function etat() {
  return {
    ok: true,
    profils: lireTout("Profils"),
    resultats: lireTout("Resultats"),
    supprimes: lireTout("Supprimes").map(s => String(s.id))
  };
}

function repondre(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return repondre(etat());
}

function doPost(e) {
  const verrou = LockService.getScriptLock();
  verrou.waitLock(20000);
  try {
    const d = JSON.parse(e.postData.contents);
    const envois = [
      ["Profils", d.profils || []],
      ["Resultats", d.resultats || []],
      ["Supprimes", (d.supprimes || []).map(id => ({ id: id }))]
    ];
    envois.forEach(([nom, liste]) => {
      if (!liste.length) return;
      const f = feuille(nom);
      const deja = new Set(lireTout(nom).map(o => String(o.id)));
      const lignes = liste
        .filter(o => !deja.has(String(o.id)))
        .map(o => ONGLETS[nom].map(k => o[k] == null ? "" : String(o[k])));
      if (lignes.length) f.getRange(f.getLastRow() + 1, 1, lignes.length, lignes[0].length).setValues(lignes);
    });
    return repondre(etat());
  } finally {
    verrou.releaseLock();
  }
}
