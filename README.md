![60302610_10156531187624141_831535432628961280_n](https://github.com/user-attachments/assets/2ad91250-a212-489a-9017-4a9524e21764)



# MADRIX 5 – Intégration Home Assistant (Avancée)

Cette intégration fournit un squelette fonctionnel pour piloter MADRIX 5 depuis Home Assistant.
Elle supporte plusieurs *backends* (protocoles). Dans cette version la prise en charge **complète** est
implémentée pour le backend **HTTP Remote API** (Remote HTTP). Les autres protocoles sont listés et
des instructions sont données pour les activer.

## Protocoles listés par MADRIX 5
- Art-Net (I, II, 3, 4)
- ASIO
- Blackmagic Design (DeckLink, Intensity, and more)
- CAST Software BlackTrax (via MADRIX Script)
- CITP
- DMX512
- GamePort
- MA-Net 1 / MA-Net 2
- MADRIX I/O
- MADRIX ORION
- Media (Images, Pictures, Logos, Videos, Text, Live-Signal Capturing, Screen Capturing)
- MIDI
- NewTek NDI (Send & Receive)
- Remote HTTP (Web Server)  <-- **Fully supported in this integration**
- Spout (Send & Receive)
- Streaming ACN (sACN / E1.31)
- Time Code (Art-Net / MIDI / SMPTE / System Time)
- WDM

## Fonctionnalités (version présente)
- Contrôle via Remote HTTP (POST /api/command) : ON/OFF, set_brightness, load_scene, goto_cue
- Polling de l'état via GET /api/status
- Entités `light` et `sensor` exposées
- Configuration via l'UI (hôte, port, protocole, api_key)

## Comment utiliser le backend HTTP
L'intégration suppose que MADRIX expose (ou qu'un plugin externe expose) une API HTTP REST avec ces endpoints :

- `POST http://{host}:{port}/api/command` avec JSON:
  ```json
  { "command": "load_scene", "params": { "name": "SceneName" } }
  ```
- `GET http://{host}:{port}/api/status` -> retourne JSON:
  ```json
  { "status": "running", "current_scene": "SceneName", "current_cue": 3 }
  ```

Si ton installation MADRIX utilise un plugin différent, adapte les endpoints ou crée un petit proxy HTTP
qui traduit les requêtes vers le protocole natif de MADRIX (Art-Net, sACN, MIDI, etc.)

## Activer d'autres protocoles
- **Art-Net / sACN / DMX** : il faut utiliser une librairie DMX/ArtNet côté Home Assistant ou un bridge sur le réseau.
  Exemple : un petit service Python qui expose une API HTTP et envoie des paquets Art-Net.
- **MIDI / ASIO / Blackmagic** : ces interfaces nécessitent du code natif ou un service sur la machine connectée.
- **NDI / Spout / Media** : le contrôle des médias se fera via plugins spécifiques.

## Exemple d'automatisation
```yaml
- alias: 'Activer scène d\'entrée'
  trigger:
    - platform: time
      at: '20:00:00'
  action:
    - service: light.turn_on
      target:
        entity_id: light.madrix_output
      data:
        scene: 'Welcome'
        brightness: 200
```

## Développement & contributions
- Les fichiers se trouvent dans `custom_components/madrix5/`
- Pour ajouter un backend : implémentez `MadrixAPI` dans `api.py` (méthodes `send_command` et `get_status`).
- Tests recommandés : créer un simple mock HTTP server renvoyant des états pour `GET /api/status`.

## Icône
Le dépôt contient `icon.png` (logo MADRIX placeholder). Remplacez-le par votre logo (transparent PNG recommandé).

## Licence
MIT — adapte selon ton choix.
