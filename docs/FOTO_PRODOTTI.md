# Foto dei prodotti: procedura completa (progetto pilota, 31/10/2026)

Provata e funzionante online su 3 prodotti pilota. Vale per prodottidigitali2 e per ogni clone del template con shop (`_data/catalogo.json`).

## 1. Quale caso e' il tuo prodotto?

| Caso | Esempi | Come si fa | Campi del catalogo |
|---|---|---|---|
| A. Foto SENZA testo | planner, habit tracker, stampe, schemi | Gemini con `img.py`, pagine vuote | solo `immagine` |
| B. Foto CON testo (la scritta fa parte del prodotto) | inviti, menu, template con titoli, CV | Pillow in `automation/foto_<id>.py`, un file per lingua | `immagine` (IT) + `tr.en.immagine` (EN) |

Regola: se nella foto compare una parola, una data o un numero, e' il caso B. Gemini non va MAI usato per il caso B (sbaglia date e lettere e scrive in inglese).

## 2. Caso A: foto senza testo con Gemini

Comando (dalla cartella della repo):

```
python C:\Users\mirco\Desktop\gemini_auto\img.py "<oggetto, pagine VUOTE, colori, sfondo PURE WHITE>" --profilo prodotto --nome <id> --out assets\images\prodotti --extra "ABSOLUTELY NO TEXT of any kind: no letters, no numbers, no digits, no words, no headings, no labels, no logos, nothing written anywhere, not even tiny. Only empty circles and blank lines. Pure white seamless background, no desk, no props. Language-neutral image."
```

Cose imparate:
- Nel soggetto scrivere "pagine vuote", "righe vuote", "cerchi vuoti". Se scrivi "calendario con i mesi" Gemini mette mesi e numeri.
- Il controllo automatico di `img.py` scarta la foto se lo sfondo non e' bianco (messaggio "scartata (sfondo non bianco ...)"): chiedere "isolated on a PURE WHITE background, no desk, no props". Una scrivania o un tavolo fanno scartare la foto.
- Guardare SEMPRE la foto prima di collegarla (leggerla con `read_file` di Desktop Commander). Esempi di errori trovati: numeri 1-20 con il 13 saltato, "NOTES", "MONTH". Se c'e' testo leggibile: rigenerare con `--extra` piu' severo (stesso `--nome`, sovrascrive).
- Qualche trattino illeggibile e' accettabile; una parola o un numero no.
- Costo: circa 3 crediti a foto, 600 crediti ogni 5 ore. Controllare con `python C:\Users\mirco\Desktop\gemini_auto\img.py --crediti`.
- Risultato: un file `assets/images/prodotti/<id>.webp` (1000x1000).

Collegare al catalogo: `"immagine": "assets/images/prodotti/<id>.webp"` (vedi sezione 4).

## 3. Caso B: foto con testo, una per lingua, con Pillow

Modello da copiare: `automation/foto_invito_matrimonio.py`. Scrive `assets/images/prodotti/<id>.webp` (IT) e `<id>-en.webp` (EN).

Come e' fatto:
- Un dizionario `TESTI` con i testi per ogni lingua (`it`, `en`). Per aggiungere una lingua basta un'altra voce e una riga nel ciclo finale.
- Le carte (invito, menu, risposta, segnaposto) sono funzioni che disegnano su un'immagine RGBA; `metti()` le ruota e aggiunge l'ombra; `ramo()` disegna i ramoscelli.
- Si disegna a 2000 px e si riduce a 1000 con LANCZOS (bordi lisci). Sfondo bianco puro come le altre foto.
- Font di Windows: `georgia.ttf`, `georgiai.ttf`, `georgiab.ttf`, `segoesc.ttf` (corsivo "a mano" per nomi e titoli). Sono in `C:\Windows\Fonts`.
- Contenuti fittizi realistici: date che esistono davvero (12 giugno 2027 e' un sabato), nomi neutri, niente marchi.

Controlli dopo ogni generazione (guardare entrambe le immagini):
- nessun testo tagliato da un'altra carta o da un ramoscello (cosi' e' stato corretto l'IT: la scheda risposta copriva il bordo dell'invito; e l'EN: una foglia sfiorava "TOGETHER");
- le frasi inglesi sono piu' lunghe di quelle italiane: controllare che stiano dentro la cornice;
- accenti corretti (Menù, Parteciperò, Non potrò).

## 4. Collegare le foto (template + catalogo)

Dal 31/10/2026 il template legge la foto per lingua. Tre punti, da tenere allineati (se ne cambi uno, cambia gli altri due):
1. `_layouts/negozio-prodotto.html`: pagina del prodotto (`nz_img = nz_p.tr[page.lang].immagine | default: nz_p.immagine`).
2. `_includes/negozio-riga.html`: riga nell'elenco negozio/categoria.
3. `_includes/masthead.html`: miniatura nel carrello (variabile `bi`).

Regola di ripiego: se la lingua non ha `tr.<lingua>.immagine`, usa `immagine`. Perche' funziona anche per le altre lingue: basta aggiungere `tr.de.immagine` e simili nel catalogo.

Esempio nel catalogo (`_data/catalogo.json`):

```
"id": "invito-matrimonio",
"immagine": "assets/images/prodotti/invito-matrimonio.webp",
...
"tr": { "en": { "immagine": "assets/images/prodotti/invito-matrimonio-en.webp", "nome": "...", ... } }
```

Come modificare il catalogo senza rovinarlo: script node con sostituzione di stringa esatta + `JSON.parse` di controllo prima di scrivere (esempi: `claudetemp\collega_planner.js`, `collega_habit.js`, `immagine_per_lingua.js`). Mai riscrivere tutto il JSON a mano. Rispettare gli a capo del file (CRLF/LF).

### Foto cliccabile con zoom (31/10/2026)
Nella scheda prodotto la foto fa un leggero zoom al passaggio del mouse (solo con mouse, non sul touch) e con il clic si apre a schermo intero (Esc o clic fuori per chiudere). Riusa il lightbox gia' presente in `assets/js/galleria.js` tramite il link `a.nz-pp-zoom` con `data-lb="prodotto"` in `negozio-prodotto.html`; gli stili sono in `negozio.css` (`.nz-pp-zoom`) e `galleria.css` (`.exlb-1`). Vale per tutti i prodotti con foto, senza toccare il catalogo.

## 5. Pubblicare e verificare

```
..\pubblica.ps1 -Repo prodottidigitali2 -Msg "..." -Files 'a','b','c'
```
- Sempre `-Files` espliciti (nella repo ci sono altri file non committati: foto non usate, ecc.). Mai `-Tutto`.
- PowerShell stampa `NativeCommandError` / avvisi LF->CRLF: sono innocui se l'ultima riga dice "Pubblicato commit ...".
- "Niente da committare" puo' voler dire che un'altra sessione ha gia' committato: controllare con `git log --oneline -3` e `git status -sb`.
- Il comando non aspetta la build. Verifica a mano:
  - Actions: https://github.com/cialdecompatibili-netizen/prodottidigitali2/actions (workflow "pages build and deployment", verde = online)
  - IT: `/negozio/<id>/` ; EN: `/en/shop/` e aprire il prodotto
  - negozio, categoria, carrello (la miniatura usa `masthead.html`); Ctrl+F5 per la cache.

## 6. Risultati del pilota

| Prodotto | Caso | Commit | Esito |
|---|---|---|---|
| planner-annuale | A (foto v2 senza testo) | `64fc0e9` | online |
| habit-tracker | A (2 tentativi scartati prima della foto giusta) | `456a606` | online |
| invito-matrimonio | B (IT + EN Pillow) + modifica template | `7853116` | online, verificato IT ed EN |

Nel planner-annuale restano non collegate `planner-annuale.webp` e `planner-annuale-en.webp` (generate da Gemini, con testo e mese): se si vuole usarle come foto per lingua, vanno bene solo dopo aver verificato date e giorni (gennaio 2027 inizia di venerdi', e' corretto in entrambe).

## 7. Da fare

1. Script `automation/foto_prodotti.py`: legge `_data/catalogo.json`, genera con il comando del caso A i prodotti con `immagine` vuota (circa 115 su 120), scrive il percorso nel catalogo, segnala le foto da rivedere. Dividere in due finestre di crediti (600 ogni 5 ore, circa 200 foto).
2. Per i prodotti del caso B (CV, inviti, template con titoli, menu): un `automation/foto_<id>.py` ciascuno, partendo da `foto_invito_matrimonio.py`.
3. Verificare che l'admin (E-commerce > Prodotti) non perda `tr.<lingua>.immagine` quando salva un prodotto (non testato).
4. Eventuale OCR per segnalare testo residuo nelle foto del caso A.
5. Altre lingue: aggiungere la voce in `TESTI` e il campo `tr.<lingua>.immagine`.
