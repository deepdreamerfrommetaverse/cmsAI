# AI CMS Enterprise Desktop

Electron powłoka otwiera lokalny (lub zdalny) frontend AI CMS Enterprise pod `/` – zakładamy, że backend+frontend są uruchomione w Dockerze (http://localhost:5173).

## Szybki start

```bash
cd electron
npm install
npm start          # uruchamia w trybie deweloperskim
```

## Build instalatorów

```bash
npm run build      # buduje DMG (mac), NSIS (win), AppImage (linux)
```

Instalatory lądują w `dist/`.

**Brak placeholderów** – konfiguracja `electron-builder` jest kompletna: asar, ikony, zapisy okna (`electron-store`), blokowanie zewnętrznych linków, wsparcie mac/win/linux.
