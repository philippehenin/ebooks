import os
import subprocess
import shutil
import zipfile

BASE_DIR = r"c:\Users\phili\Git\ebooks"
PACKS_DIR = os.path.join(BASE_DIR, 'device_packs')
CONVERTER = r"C:\Program Files\Calibre2\ebook-convert.exe"

# HTML Template with 100% pure CSS icons, badges, and zero raw Unicode emojis
html_template = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>NotebookLM Infographic Installation Guide</title>
<style>
  @page {
    margin: 10mm 12mm 10mm 12mm;
  }
  * {
    box-sizing: border-box;
  }
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.45;
    font-size: 13px;
    margin: 0;
    padding: 0;
  }
  
  .header-banner {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 8px;
    margin-bottom: 14px;
    text-align: center;
  }
  .header-banner h1 {
    margin: 0 0 6px 0;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.5px;
  }
  .header-banner p {
    margin: 0;
    font-size: 12.5px;
    font-weight: 600;
    opacity: 0.95;
    letter-spacing: 0.5px;
  }

  .flag-pill {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 11px;
    margin-right: 6px;
    text-transform: uppercase;
  }
  .flag-fr { background-color: #dbeafe; color: #1e40af; }
  .flag-gb { background-color: #fef3c7; color: #92400e; }

  .icon-circle {
    display: inline-block;
    width: 20px;
    height: 20px;
    line-height: 20px;
    text-align: center;
    border-radius: 50%;
    font-weight: 700;
    font-size: 11px;
    margin-right: 6px;
  }
  .icon-blue { background-color: #2563eb; color: #ffffff; }
  .icon-green { background-color: #16a34a; color: #ffffff; }
  .icon-amber { background-color: #d97706; color: #ffffff; }

  .section-title {
    background-color: #f1f5f9;
    border-left: 5px solid #2563eb;
    padding: 8px 14px;
    font-size: 15px;
    font-weight: 700;
    color: #0f172a;
    margin: 14px 0 10px 0;
    border-radius: 0 6px 6px 0;
    page-break-after: avoid;
  }

  .callout-box {
    background-color: #eff6ff;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #3b82f6;
    padding: 12px 16px;
    border-radius: 6px;
    margin: 10px 0;
    page-break-inside: avoid;
  }
  .callout-title {
    font-weight: 700;
    color: #1e40af;
    font-size: 14px;
    margin-bottom: 6px;
  }
  .callout-body {
    color: #1e293b;
    font-size: 12.5px;
  }

  .infographic-container {
    text-align: center;
    margin: 10px 0;
    page-break-inside: avoid;
  }
  .infographic-img {
    max-width: 90%;
    height: auto;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }

  .steps-grid {
    margin: 10px 0;
  }
  .step-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 10px 14px;
    margin-bottom: 8px;
    page-break-inside: avoid;
  }
  .step-header {
    font-weight: 700;
    font-size: 13.5px;
    color: #0f172a;
    margin-bottom: 4px;
  }
  
  .step-num {
    display: inline-block;
    width: 22px;
    height: 22px;
    line-height: 22px;
    background-color: #2563eb;
    color: #ffffff;
    text-align: center;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
    margin-right: 8px;
  }

  .step-desc {
    color: #334155;
    font-size: 12.5px;
    padding-left: 30px;
  }

  .tree-box {
    background: #0f172a;
    color: #f8fafc;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    padding: 10px 14px;
    border-radius: 6px;
    margin: 8px 0 4px 30px;
    line-height: 1.4;
    white-space: pre;
    page-break-inside: avoid;
  }

  .alt-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 4px solid #22c55e;
    padding: 10px 14px;
    border-radius: 6px;
    margin: 10px 0;
    page-break-inside: avoid;
  }
  .alt-title {
    font-weight: 700;
    color: #15803d;
    font-size: 13.5px;
    margin-bottom: 4px;
  }

  .part-header {
    background: #0f172a;
    color: #ffffff;
    padding: 10px 16px;
    border-radius: 6px;
    font-size: 15px;
    font-weight: 700;
    margin: 14px 0 10px 0;
    text-align: center;
    page-break-before: always;
  }
</style>
</head>
<body>

  <!-- GLOBAL BANNER -->
  <div class="header-banner">
    <h1>NOTEBOOKLM INFOGRAPHIC INSTALLATION GUIDE</h1>
    <p><span class="flag-pill flag-fr">FR</span> FRANÇAIS (EN PREMIER) &nbsp;|&nbsp; <span class="flag-pill flag-gb">GB</span> ENGLISH (BELOW)</p>
  </div>

  <!-- PART 1: FRENCH -->
  <div class="section-title"><span class="flag-pill flag-fr">FR</span> PARTIE 1 : GUIDE DE TRANSFERT ET INFOGRAPHIE (FRANÇAIS)</div>

  <div class="infographic-container">
    <img class="infographic-img" src="notebooklm_library_overview.png" alt="Vue d'ensemble de la bibliothèque">
  </div>

  <div class="callout-box">
    <div class="callout-title"><span class="icon-circle icon-blue">i</span> Le Contexte & Mystère Résolu</div>
    <div class="callout-body">
      <strong>Pourquoi vos fichiers <code>.EPUB</code> ne s'affichaient pas par câble USB sur le Kindle ?</strong><br>
      Les liseuses Amazon Kindle sont très exigeantes ! Lorsqu'elles sont branchées par <strong>câble USB</strong>, elles n'indexent <strong>QUE le format natif Amazon <code>.AZW3</code></strong> (ou <code>.MOBI</code>). Les fichiers <code>.EPUB</code> bruts sont ignorés par le câble USB.<br><br>
      <span class="icon-circle icon-amber">★</span> <strong>Bonne nouvelle</strong> : Nous avons converti <strong>l'intégralité des 293 chefs-d'œuvre</strong> au format natif <strong><code>.AZW3</code></strong> afin que votre Kindle les reconnaisse et les affiche immédiatement !
    </div>
  </div>

  <div class="section-title"><span class="icon-circle icon-blue">★</span> Infographie NotebookLM : Guide de Transfert Kindle</div>
  <div class="infographic-container">
    <img class="infographic-img" src="notebooklm_kindle_guide.png" alt="Guide de Transfert Kindle">
  </div>

  <div class="section-title"><span class="icon-circle icon-blue">▶</span> Guide Étape par Étape</div>

  <div class="steps-grid">
    <div class="step-card">
      <div class="step-header"><span class="step-num">1</span> Extraire l'archive ZIP</div>
      <div class="step-desc">Décompressez l'archive <strong><code>Kindle_10th_Gen_Pack.zip</code></strong> sur votre ordinateur (ou ouvrez le dossier <code>USB_Direct_Transfer_documents</code>).</div>
    </div>

    <div class="step-card">
      <div class="step-header"><span class="step-num">2</span> Brancher le Kindle en USB</div>
      <div class="step-desc">Branchez votre <strong>Kindle 10e Génération</strong> à votre ordinateur avec son câble USB. Ouvrez l'explorateur de fichiers et repérez le lecteur nommé <strong><code>Kindle</code></strong>.</div>
    </div>

    <div class="step-card">
      <div class="step-header"><span class="step-num">3</span> Copier les dossiers dans <code>documents</code></div>
      <div class="step-desc">Glissez-déposez les deux dossiers <strong><code>French_Classics</code></strong> et <strong><code>English_Classics</code></strong> directement dans le dossier <strong><code>documents</code></strong> de votre Kindle :</div>
      <div class="tree-box">Kindle (Lecteur)
 └── documents/
      ├── French_Classics/ [FR] (Monte-Cristo, Les Misérables, Lupin...)
      └── English_Classics/ [GB] (Sherlock Holmes, Frankenstein, Gatsby...)</div>
    </div>

    <div class="step-card">
      <div class="step-header"><span class="step-num">4</span> Éjecter et Lire !</div>
      <div class="step-desc">Éjectez en toute sécurité votre Kindle dans Windows/Mac, débranchez le câble, et <strong>magie !</strong> Tous les 293 livres apparaissent sur l'écran d'accueil avec couvertures, chapitres et mise en page parfaite.</div>
    </div>
  </div>

  <div class="alt-box">
    <div class="alt-title"><span class="icon-circle icon-green">W</span> Option Alternative : Transfert Sans Fil (Send to Kindle)</div>
    <div class="callout-body">
      Si vous souhaitez envoyer des fichiers <code>.EPUB</code> sans câble USB :<br>
      1. Rendez-vous sur <strong><a href="https://www.amazon.com/sendtokindle" style="color:#15803d;">amazon.com/sendtokindle</a></strong>.<br>
      2. Glissez-déposez vos fichiers <code>.epub</code> depuis le dossier <code>Send_To_Kindle_EPUBs</code>.<br>
      3. Cliquez sur <strong>Send</strong> : Amazon livrera les livres sans fil sur votre Kindle.
    </div>
  </div>

  <!-- PART 2: ENGLISH -->
  <div class="part-header"><span class="flag-pill flag-gb">GB</span> PART 2: INSTALLATION GUIDE & INFOGRAPHICS (ENGLISH)</div>

  <div class="callout-box">
    <div class="callout-title"><span class="icon-circle icon-blue">i</span> Technical Context & Mystery Solved</div>
    <div class="callout-body">
      <strong>Why didn't raw <code>.EPUB</code> files show up over USB cable on your Kindle?</strong><br>
      Amazon Kindle devices are picky about file formats over cable connections. When connected via <strong>USB cable</strong>, Kindles <strong>ONLY index native Amazon <code>.AZW3</code></strong> (Kindle Format 8) or <code>.MOBI</code> files. Raw <code>.EPUB</code> files get ignored over USB cable.<br><br>
      <span class="icon-circle icon-amber">★</span> <strong>Good news</strong>: We converted <strong>all 293 classic ebooks</strong> into native <strong><code>.AZW3</code></strong> format so your Kindle detects and renders them instantly!
    </div>
  </div>

  <div class="section-title"><span class="icon-circle icon-blue">★</span> NotebookLM Infographic Step-by-Step Guide</div>
  <div class="infographic-container">
    <img class="infographic-img" src="notebooklm_kindle_guide.png" alt="NotebookLM Kindle Guide">
  </div>

  <div class="section-title"><span class="icon-circle icon-blue">▶</span> Step-by-Step Direct Cable Recipe</div>

  <div class="steps-grid">
    <div class="step-card">
      <div class="step-header"><span class="step-num">1</span> Extract your Pack</div>
      <div class="step-desc">Unzip <strong><code>Kindle_10th_Gen_Pack.zip</code></strong> (or open the local folder <code>USB_Direct_Transfer_documents</code>).</div>
    </div>

    <div class="step-card">
      <div class="step-header"><span class="step-num">2</span> Connect your Kindle</div>
      <div class="step-desc">Connect your <strong>Kindle 10th Gen</strong> to your computer using a USB cable. Open your file explorer and locate the <strong><code>Kindle</code></strong> drive.</div>
    </div>

    <div class="step-card">
      <div class="step-header"><span class="step-num">3</span> Drag & Drop into <code>documents/</code></div>
      <div class="step-desc">Drag the <strong><code>French_Classics</code></strong> and <strong><code>English_Classics</code></strong> folders straight into your Kindle's <strong><code>documents</code></strong> folder:</div>
      <div class="tree-box">Kindle (Drive)
 └── documents/
      ├── French_Classics/ [FR] (Monte-Cristo, Les Misérables, Lupin...)
      └── English_Classics/ [GB] (Sherlock Holmes, Frankenstein, Gatsby...)</div>
    </div>

    <div class="step-card">
      <div class="step-header"><span class="step-num">4</span> Eject & Read!</div>
      <div class="step-desc">Safely eject your Kindle USB drive, unplug the cable, and <strong>enjoy 293 DRM-free classics</strong> ready on your home screen!</div>
    </div>
  </div>

  <div class="alt-box">
    <div class="alt-title"><span class="icon-circle icon-green">W</span> Alternative Option: Wireless Transfer (Send to Kindle)</div>
    <div class="callout-body">
      If you prefer sending <code>.EPUB</code> files wirelessly without a cable:<br>
      1. Visit <strong><a href="https://www.amazon.com/sendtokindle" style="color:#15803d;">amazon.com/sendtokindle</a></strong>.<br>
      2. Drag and drop <code>.epub</code> files from the <code>Send_To_Kindle_EPUBs</code> folder.<br>
      3. Click <strong>Send</strong> to deliver wirelessly to your Kindle account.
    </div>
  </div>

</body>
</html>
"""

def generate_pdf():
    kindle_pack_dir = os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack')
    html_file = os.path.join(kindle_pack_dir, 'INSTALLATION_GUIDE.html')
    pdf_file = os.path.join(kindle_pack_dir, 'INSTALLATION_GUIDE.pdf')

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print("Generated INSTALLATION_GUIDE.html")

    cmd = [
        CONVERTER, html_file, pdf_file,
        '--paper-size', 'letter',
        '--margin-top', '10',
        '--margin-bottom', '10',
        '--margin-left', '12',
        '--margin-right', '12',
        '--pdf-default-font-size', '13'
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(pdf_file):
        print(f"INSTALLATION_GUIDE.pdf generated successfully ({round(os.path.getsize(pdf_file)/1024, 1)} KB).")
    else:
        print("PDF Generation error:", res.stderr)

    # Copy to all pack folders
    pack_dirs = [
        os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack'),
        os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack'),
        os.path.join(PACKS_DIR, 'Master_Library_Pack')
    ]

    for pd in pack_dirs:
        os.makedirs(pd, exist_ok=True)
        if os.path.abspath(pd) != os.path.abspath(kindle_pack_dir):
            shutil.copy2(pdf_file, os.path.join(pd, 'INSTALLATION_GUIDE.pdf'))
            shutil.copy2(os.path.join(kindle_pack_dir, 'INSTALLATION_GUIDE.md'), os.path.join(pd, 'INSTALLATION_GUIDE.md'))

def zip_folder(folder_path, output_zip_path):
    print(f"Updating zip archive: {os.path.basename(output_zip_path)}...")
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as ziph:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, folder_path)
                ziph.write(filepath, arcname)
    size_mb = os.path.getsize(output_zip_path) / (1024 * 1024)
    print(f"Archive updated: {os.path.basename(output_zip_path)} ({size_mb:.1f} MB).")

if __name__ == '__main__':
    generate_pdf()
    zip_folder(os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack'), os.path.join(PACKS_DIR, 'Kindle_10th_Gen_Pack.zip'))
    zip_folder(os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack'), os.path.join(PACKS_DIR, 'X3_X4_Eink_Reader_Pack.zip'))
    zip_folder(os.path.join(PACKS_DIR, 'Master_Library_Pack'), os.path.join(PACKS_DIR, 'Top_300_Ebook_Master_Pack.zip'))
    print("ALL DONE!")
