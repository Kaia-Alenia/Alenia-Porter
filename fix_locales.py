import json

with open('/media/alejandro/D/tool/porter/src/alenia_porter/assets/locales/locales.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix English ones that are Spanish
en = data['en']
en['quality_bad'] = 'Bad'
en['quality_worst'] = 'Worst'
en['quality_best'] = 'Best'
en['cmd_none'] = 'None (Default)'
en['example_remove_audio'] = '(Remove audio)'
en['example_remove_video'] = '(Remove video)'
en['bitrate_256'] = '256 kbps (Very good quality)'
en['formulaGroupVideoImage'] = 'VIDEO — IMAGE'
en['formulaGroupVideoImageDesc'] = 'Visual transformations, cropping, and filters'
en['formulaGroupVideoAudio'] = 'VIDEO — AUDIO'
en['formulaGroupVideoAudioDesc'] = 'Audio track management and extraction'
en['formulaGroupVideoTime'] = 'VIDEO — TIME & FPS'
en['formulaGroupVideoTimeDesc'] = 'Speed control, framerate, and trimming'
en['formulaGroupVideoStream'] = 'VIDEO — FORMATS & CODECS'
en['formulaGroupVideoStreamDesc'] = 'Change formats, codecs, and web optimization'
en['formulaGroupAudioVol'] = 'AUDIO — VOLUME'
en['formulaGroupAudioVolDesc'] = 'Normalization and gain adjustments'
en['formulaGroupAudioChannel'] = 'AUDIO — CHANNELS & FREQUENCY'
en['formulaGroupAudioChannelDesc'] = 'Mono/stereo conversion and sampling'
en['formulaGroupAudioFx'] = 'AUDIO — EFFECTS'
en['formulaGroupAudioFxDesc'] = 'Filters, echoes, and fades'
en['formulaGroupAudioBitrate'] = 'AUDIO — BITRATE & TRIMMING'
en['formulaGroupAudioBitrateDesc'] = 'Compression quality and time editing'
en['formulaGroupImageTransform'] = 'IMAGE — TRANSFORM'
en['formulaGroupImageTransformDesc'] = 'Resize, rotate, and crop'
en['formulaGroupImageColor'] = 'IMAGE — COLOR'
en['formulaGroupImageColorDesc'] = 'Brightness, contrast, and filters'
en['formulaGroupImageFx'] = 'IMAGE — EFFECTS'
en['formulaGroupImageFxDesc'] = 'Blur, sharpen, and vignettes'
en['formulaFormulas'] = 'Formulas'
en['fHflip'] = 'Horizontal flip'
en['fVflip'] = 'Vertical flip'
en['fTrans1'] = 'Rotate 90° right'
en['fTrans2'] = 'Rotate 90° left'
en['fGray'] = 'Grayscale'
en['fNegate'] = 'Negative colors'
en['fBright5'] = 'Brightness +5%'
en['fCont30'] = 'Contrast +30%'
en['fSat50'] = 'Saturation +50%'
en['fUnsharp'] = 'Sharpen'
en['fBoxblur'] = 'Soft blur'
en['fScale1280'] = 'Width 1280px, auto height'
en['fPadLetterbox'] = 'Letterbox 1920x1080'
en['fAn'] = 'Remove audio track'
en['fVn'] = 'Extract audio only (no video)'
en['fCaCopy'] = 'Copy audio without re-encoding'
en['fAfVol15'] = 'Amplify audio +50%'
en['fLoudnorm'] = 'Normalize volume (EBU R128)'
en['fSsTrim'] = 'Trim: from 0:30, dur. 60s'
en['fR30'] = 'Fix FPS to 30'
en['fR60'] = 'Fix FPS to 60'
en['fSetpts05'] = 'Speed x2 (timelapse)'
en['fSetpts20'] = 'Slow motion x0.5'
en['fCvCopy'] = 'Copy video without re-encoding'
en['fMovflags'] = 'Optimize for web streaming'
en['fThreads4'] = 'Force 4 CPU threads'
en['fBv2m'] = 'Fixed bitrate 2 Mbps'
en['fCrf18'] = 'High quality (CRF 18)'
en['fVol20'] = 'Double volume (+100%)'
en['fVol05'] = 'Reduce to half'
en['fDynaudnorm'] = 'Dynamic normalization'
en['fAgate'] = 'Noise gate (silence)'
en['fAc1'] = 'Convert to Mono'
en['fAc2'] = 'Force Stereo'
en['fAr44'] = 'Sample rate 44.1 kHz (CD)'
en['fAr48'] = 'Sample rate 48 kHz (video)'
en['fAr22'] = 'Sample rate 22 kHz (web)'
en['fAtempo15'] = 'Speed x1.5 (no pitch change)'
en['fAtempo075'] = 'Speed x0.75 (no pitch change)'
en['fAecho'] = 'Echo / reverb'
en['fHighpass'] = 'High-pass filter 200 Hz'
en['fLowpass'] = 'Low-pass filter 3 kHz'
en['fFadein'] = '3 second fade-in'
en['fFadeout'] = '3 second fade-out'
en['fTrimAud'] = 'Trim: from 1:00, 30s'
en['fBa320'] = 'Bitrate 320 kbps (high quality)'
en['fBa128'] = 'Bitrate 128 kbps (standard)'
en['fBa64'] = 'Bitrate 64 kbps (saver)'
en['fScale800'] = 'Width 800px, proportional height'
en['fCrop'] = 'Crop left half'
en['fTile'] = '3x3 Mosaic'
en['fBright10'] = 'Brightness +10%'
en['fCont50'] = 'Contrast +50%'
en['fSat0'] = 'Remove saturation (B&W)'
en['fSatDouble'] = 'Double saturation'
en['fVintage'] = 'Vintage effect'
en['fGamma'] = 'Gamma +50%'
en['fUnsharpHigh'] = 'Strong sharpen'
en['fUnsharpLow'] = 'Soft sharpen'
en['fBoxblurGauss'] = 'Gaussian blur'
en['fNoise'] = 'Add noise / grain'
en['fVignette'] = 'Dark vignette on edges'
en['fEdge'] = 'Edge detection'

# Add the ones that the user said are missing (which might not be missing but just in case, I will add them to both)
missing = {
    'optgroup_webmoderno': {'en': '── Web / Modern ──', 'es': '── Web / Moderno ──'},
    'optgroup_altacompatibilidad': {'en': '── High Compatibility ──', 'es': '── Alta Compatibilidad ──'},
    'optgroup_sinprdida': {'en': '── Lossless ──', 'es': '── Sin pérdida ──'},
    'optgroup_conprdida': {'en': '── Lossy ──', 'es': '── Con pérdida ──'},
    'optgroup_estndar': {'en': '── Standard ──', 'es': '── Estándar ──'},
    'optgroup_avanzado': {'en': '── Advanced ──', 'es': '── Avanzado ──'},
    'optgroup_especial': {'en': '── Special ──', 'es': '── Especial ──'},
    'optgroup_otros': {'en': '── Others ──', 'es': '── Otros ──'},
    'appWillRestart': {'en': 'Alenia Porter successfully updated. Restarting...', 'es': 'Alenia Porter actualizado exitosamente. Reiniciando...'},
    'currentVersion': {'en': 'Current Version:', 'es': 'Versión Actual:'},
    'dataPrivacy': {'en': 'Data Privacy', 'es': 'Privacidad de Datos'},
    'downloadingUpdate': {'en': 'Downloading update...', 'es': 'Descargando actualización...'},
    'errorNoFiles': {'en': 'No compatible files (Video/Audio/Image) detected.', 'es': 'Ningún archivo compatible (Video/Audio/Imagen) fue detectado.'},
    'githubLink': {'en': 'GitHub Repository', 'es': 'Repositorio GitHub'},
    'newVersionAvailable': {'en': 'New version available!', 'es': '¡Nueva versión disponible!'},
    'outputFormatsFolder': {'en': 'Output folders', 'es': 'Carpetas de salida'},
    'savedInSource': {'en': 'Files saved to source', 'es': 'Archivos guardados en origen'},
    'selectTabFormat': {'en': 'Output format', 'es': 'Formato de salida'},
    'yourAlias': {'en': 'Your anonymous alias:', 'es': 'Tu alias anónimo:'},
    'opt_libvpx-vp9': {'en': 'VP9 (WebM)', 'es': 'VP9 (WebM)'},
    'opt_libaom-av1': {'en': 'AV1 (libaom)', 'es': 'AV1 (libaom)'},
    'opt_libsvtav1': {'en': 'AV1 (SVT-AV1, fast)', 'es': 'AV1 (SVT-AV1, rápido)'},
    'opt_mjpeg': {'en': 'MJPEG (Motion JPEG)', 'es': 'MJPEG (Motion JPEG)'},
}

for k, v in missing.items():
    data['en'][k] = v['en']
    data['es'][k] = v['es']

with open('/media/alejandro/D/tool/porter/src/alenia_porter/assets/locales/locales.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
