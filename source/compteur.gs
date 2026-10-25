/* Lis avec moi / Lees met mij - compteur discret des appareils (FR et NL), visible seulement par Robin.
   A coller dans Extensions > Apps Script d'un NOUVEAU Google Sheet prive, en remplacant tout le contenu.
   1. Choisir la fonction « installer » puis Executer (et autoriser) : cree les onglets et les rapports par e-mail.
   2. Deployer > Nouveau deploiement > Application Web : executer en tant que « Moi », acces « Tout le monde ».
   Aucune donnee personnelle : seulement la date, l'edition, installee ou non, le type d'appareil et un numero au hasard. */

var COLONNES = ["date", "edition", "type", "appareil", "id"];
var APPAREILS = ["iPad", "iPhone", "Android", "Ordinateur"];

function feuille() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var f = ss.getSheetByName("Compteur");
  if (!f) {
    f = ss.insertSheet("Compteur");
    f.appendRow(COLONNES);
    f.setFrozenRows(1);
  }
  return f;
}

// Un signal par appareil, envoye par l'app a sa premiere ouverture (dans le navigateur, puis une fois installee).
function doGet(e) {
  var p = (e && e.parameter) || {};
  var edition = p.edition === "fr" || p.edition === "nl" ? p.edition : "";
  var type = p.type === "installation" || p.type === "navigateur" ? p.type : "";
  var appareil = APPAREILS.indexOf(p.appareil) >= 0 ? p.appareil : "Autre";
  var id = String(p.id || "").replace(/[^a-z0-9]/gi, "").slice(0, 40);
  if (edition && type && id) {
    var verrou = LockService.getScriptLock();
    verrou.waitLock(20000);
    try {
      var f = feuille();
      var n = f.getLastRow() - 1;
      var deja = n > 0 ? f.getRange(2, 3, n, 3).getValues() : [];
      var trouve = false;
      for (var i = 0; i < deja.length; i++) if (deja[i][0] === type && String(deja[i][2]) === id) trouve = true;
      if (!trouve) f.appendRow([new Date(), edition, type, appareil, id]);
    } finally {
      verrou.releaseLock();
    }
  }
  return ContentService.createTextOutput("ok");
}

function compterEntre(debut, fin) {
  var c = { fr: { installation: 0, navigateur: 0 }, nl: { installation: 0, navigateur: 0 } };
  var n = feuille().getLastRow() - 1;
  var lignes = n > 0 ? feuille().getRange(2, 1, n, 3).getValues() : [];
  for (var i = 0; i < lignes.length; i++) {
    var d = new Date(lignes[i][0]);
    if (d >= debut && d < fin && c[lignes[i][1]] && lignes[i][2] in c[lignes[i][1]]) c[lignes[i][1]][lignes[i][2]]++;
  }
  return c;
}

function ligne(nom, p, t) {
  return nom + " : " + p.installation + " installation(s) sur l'ecran d'accueil (total " + t.installation + "), " +
    p.navigateur + " nouvel(s) appareil(s) dans le navigateur (total " + t.navigateur + ")";
}

function rapport(sujet, intro, debut, fin) {
  var p = compterEntre(debut, fin), t = compterEntre(new Date(0), fin);
  var texte = intro + "\n\n" +
    ligne("Lis avec moi (FR)", p.fr, t.fr) + "\n" +
    ligne("Lees met mij (NL)", p.nl, t.nl) + "\n\n" +
    "Detail : " + SpreadsheetApp.getActiveSpreadsheet().getUrl();
  MailApp.sendEmail(Session.getEffectiveUser().getEmail(), sujet, texte);
}

function rapportSemaine() {
  var fin = new Date(), debut = new Date(fin.getTime() - 7 * 24 * 3600 * 1000);
  rapport("Lis avec moi - rapport de la semaine", "Ces 7 derniers jours :", debut, fin);
}

function rapportMois() {
  var maintenant = new Date();
  var fin = new Date(maintenant.getFullYear(), maintenant.getMonth(), 1);
  var debut = new Date(maintenant.getFullYear(), maintenant.getMonth() - 1, 1);
  var mois = Utilities.formatDate(debut, Session.getScriptTimeZone(), "MM/yyyy");
  rapport("Lis avec moi - rapport du mois " + mois, "Le mois " + mois + " :", debut, fin);
}

// A executer une fois : onglets + rapport chaque lundi vers 8 h et le 1er de chaque mois vers 8 h (mois ecoule).
function installer() {
  feuille();
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var r = ss.getSheetByName("Resume") || ss.insertSheet("Resume");
  r.clear();
  r.getRange(1, 1, 4, 3).setValues([
    ["", "Installations", "Navigateur"],
    ["Lis avec moi (FR)", "", ""],
    ["Lees met mij (NL)", "", ""],
    ["Total", "", ""]
  ]);
  r.getRange("B2:C3").setFormulas([
    ['=COUNTIFS(Compteur!B:B,"fr",Compteur!C:C,"installation")', '=COUNTIFS(Compteur!B:B,"fr",Compteur!C:C,"navigateur")'],
    ['=COUNTIFS(Compteur!B:B,"nl",Compteur!C:C,"installation")', '=COUNTIFS(Compteur!B:B,"nl",Compteur!C:C,"navigateur")']
  ]);
  r.getRange("B4:C4").setFormulas([["=B2+B3", "=C2+C3"]]);
  var anciens = ScriptApp.getProjectTriggers();
  for (var i = 0; i < anciens.length; i++) ScriptApp.deleteTrigger(anciens[i]);
  ScriptApp.newTrigger("rapportSemaine").timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(8).create();
  ScriptApp.newTrigger("rapportMois").timeBased().onMonthDay(1).atHour(8).create();
}
