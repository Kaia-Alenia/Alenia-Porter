import React, { useState, useEffect, useRef } from "react";
import {
  FileVideo,
  FileAudio,
  FileImage,
  UploadCloud,
  Layers,
  Settings,
  Sliders,
  Terminal,
  Play,
  PlayCircle,
  Clock,
  Sparkles,
  Download,
  CheckCircle2,
  ListRestart,
  HelpCircle,
  ArrowRight,
  Info,
  ExternalLink,
  ChevronRight,
  ChevronDown,
  ChevronUp,
  RefreshCw,
  Plus,
  Trash2,
  Maximize2,
  Copy,
  Check,
  AlertTriangle,
  Heart,
  Palette,
  BookOpen,
  ArrowLeft,
  File,
  Folder
} from "lucide-react";
import Mascot from "./components/Mascot";
import SplitSlider from "./components/SplitSlider";
import { MediaType, DemoFile, CompressionSettings, TerminalLog, OptimizationResult } from "./types";

const DEMO_FILES: DemoFile[] = [
  {
    id: "demo-video",
    name: "paisaje_cinematico_naturaleza.mp4",
    type: "video",
    originalSize: 25680100, // 24.5 MB
    duration: "0:15",
    resolution: "1920x1080",
    src: "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
  },
  {
    id: "demo-audio",
    name: "lofi_synth_relaxation.mp3",
    type: "audio",
    originalSize: 7130200, // 6.8 MB
    duration: "3:12",
    src: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
  },
  {
    id: "demo-image",
    name: "tokio_calle_noche_4k.jpg",
    type: "image",
    originalSize: 8591000, // 8.2 MB
    resolution: "3840x2160",
    src: "https://images.unsplash.com/photo-1540959733332-eab4deceeaf7?auto=format&fit=crop&w=1200&q=80"
  }
];

const TRANSLATIONS: Record<string, Record<string, string>> = {
  US: {
    title: "ALENIA PORTER",
    uploadTitle: "UPLOAD MEDIA FILE",
    uploadDesc: "Tap to load files or drag here",
    uploadFiles: "Upload Files",
    uploadFolderRecursive: "Upload Folder (Recursive)",
    browseFiles: "Browse files",
    processingQueue: "PROCESSING QUEUE",
    pause: "Pause",
    process: "Process",
    clear: "Clear",
    fileChar: "FILE CHARACTERISTICS",
    fileName: "Name",
    fileSize: "Size",
    fileFormat: "Format",
    fileDimensions: "Dimensions",
    fileDuration: "Duration",
    compEstimations: "COMPRESSION ESTIMATIONS",
    original: "Original",
    estimated: "Estimated",
    savings: "Savings",
    downloadOptimized: "Download Optimized",
    compParameters: "COMPRESSION PARAMETERS",
    presetLabel: "PRESETS",
    outputFormat: "Output Format",
    videoCodec: "Video Codec",
    audioBitrate: "Audio Bitrate",
    resolutionScale: "Resolution (Scale)",
    fps: "Frame Rate (FPS)",
    speedPreset: "Speed Preset",
    customArgs: "Custom FFmpeg Arguments",
    optimizeBtn: "Optimize File",
    optimizingBtn: "Optimizing...",
    successMsg: "PROCESSED SUCCESSFULLY",
    runningMsg: "RUNNING OPTIMIZATION...",
    historyTitle: "CONVERSION HISTORY",
    clearHistory: "Clear",
    noHistory: "No optimized files in this session yet.",
    settingsTitle: "Alenia Porter Settings",
    visualCustomization: "Visual Customization",
    themeLabel: "Theme Color",
    systemSettings: "System Settings",
    safeMode: "Safe Mode",
    safeModeDesc: "Forces CPU backup encoding",
    hardwareAcceleration: "Hardware Acceleration",
    hwDetected: "Detected",
    none: "None",
    downloadCrashDump: "DOWNLOAD CRASH DUMP",
    crashDumpDesc: "Generates a simulated memory dump in case of WASM errors",
    sendTelemetry: "Send Anonymous Telemetry",
    communityDashboard: "GLOBAL COMMUNITY DASHBOARD",
    files: "Files",
    bytesSaved: "Bytes Saved",
    apiRequests: "API Requests",
    users: "Users",
    supportTitle: "Performance & Support",
    privacyTitle: "Privacy & Statistics",
    versionInfo: "Version Info",
    changelog: "Changelog & Updates",
    close: "Close",
    updateAvailable: "New version available!",
    clickToUpdate: "Click to update",
    originalScale: "Original Scale",
    originalFps: "Original FPS",
    optimizationSuccess: "Optimization finished! Compressed {savings}% of the original file.",
    initLog: "[Alenia FFmpeg] Starting media compilation...",
    sourceFile: "[Alenia FFmpeg] Source file: ",
    commandLog: "[Alenia FFmpeg] Command: ",
    cacheMatch: "[Smart-Cache] MD5/SHA fingerprint match in local cache!",
    cacheSkip: "[Smart-Cache] Skipping redundant compilation for: ",
    supportedFormats: "Supported Formats",
    supportedFormatsDesc: "All accepted formats ordered by media category:",
    supportSection: "Support Alenia Studios",
    supportDesc: "Official support options for Alenia Studios. Your support lets us keep creating free tools for the community!",
    donatePaypal: "Donate via PayPal",
    hwDetectedLabel: "Detected",
    crashDumpBtn: "DOWNLOAD CRASH DUMP",
    nicknameAlias: "Alias",
    nicknameSave: "Save",
    nicknameCancel: "Cancel",
    nicknameEdit: "Edit",
    themeWhite: "White",
    themeDark: "Dark",
    themeCream: "Cream",

    formulaGroupVideoImage: "VIDEO — IMAGE",
    formulaGroupVideoImageDesc: "Visual transformations, cropping, and filters",
    formulaGroupVideoAudio: "VIDEO — AUDIO",
    formulaGroupVideoAudioDesc: "Audio track management and extraction",
    formulaGroupVideoTime: "VIDEO — TIME & FPS",
    formulaGroupVideoTimeDesc: "Speed control, framerate, and trimming",
    formulaGroupVideoStream: "VIDEO — FORMATS & CODECS",
    formulaGroupVideoStreamDesc: "Change formats, codecs, and web optimization",

    formulaGroupAudioVol: "AUDIO — VOLUME",
    formulaGroupAudioVolDesc: "Normalization and gain adjustments",
    formulaGroupAudioChannel: "AUDIO — CHANNELS & FREQUENCY",
    formulaGroupAudioChannelDesc: "Mono/stereo conversion and sampling",
    formulaGroupAudioFx: "AUDIO — EFFECTS",
    formulaGroupAudioFxDesc: "Filters, echoes, and fades",
    formulaGroupAudioBitrate: "AUDIO — BITRATE & TRIMMING",
    formulaGroupAudioBitrateDesc: "Compression quality and time editing",
    
    formulaGroupImageTransform: "IMAGE — TRANSFORM",
    formulaGroupImageTransformDesc: "Resize, rotate, and crop",
    formulaGroupImageColor: "IMAGE — COLOR",
    formulaGroupImageColorDesc: "Brightness, contrast, and filters",
    formulaGroupImageFx: "IMAGE — EFFECTS",
    formulaGroupImageFxDesc: "Blur, sharpen, and vignettes",
    formulaFormulas: "Formulas",
    
    fHflip: "Horizontal flip",
    fVflip: "Vertical flip",
    fTrans1: "Rotate 90° right",
    fTrans2: "Rotate 90° left",
    fGray: "Grayscale",
    fNegate: "Negative colors",
    fBright5: "Brightness +5%",
    fCont30: "Contrast +30%",
    fSat50: "Saturation +50%",
    fUnsharp: "Sharpen",
    fBoxblur: "Soft blur",
    fScale1280: "Width 1280px, auto height",
    fPadLetterbox: "Letterbox 1920x1080",
    fAn: "Remove audio track",
    fVn: "Extract audio only (no video)",
    fCaCopy: "Copy audio without re-encoding",
    fAfVol15: "Amplify audio +50%",
    fLoudnorm: "Normalize volume (EBU R128)",
    fSsTrim: "Trim: from 0:30, dur. 60s",
    fR30: "Fix FPS to 30",
    fR60: "Fix FPS to 60",
    fSetpts05: "Speed x2 (timelapse)",
    fSetpts20: "Slow motion x0.5",
    fCvCopy: "Copy video without re-encoding",
    fMovflags: "Optimize for web streaming",
    fThreads4: "Force 4 CPU threads",
    fBv2m: "Fixed bitrate 2 Mbps",
    fCrf18: "High quality (CRF 18)",
    fVol20: "Double volume (+100%)",
    fVol05: "Reduce to half",
    fDynaudnorm: "Dynamic normalization",
    fAgate: "Noise gate (silence)",
    fAc1: "Convert to Mono",
    fAc2: "Force Stereo",
    fAr44: "Sample rate 44.1 kHz (CD)",
    fAr48: "Sample rate 48 kHz (video)",
    fAr22: "Sample rate 22 kHz (web)",
    fAtempo15: "Speed x1.5 (no pitch change)",
    fAtempo075: "Speed x0.75 (no pitch change)",
    fAecho: "Echo / reverb",
    fHighpass: "High-pass filter 200 Hz",
    fLowpass: "Low-pass filter 3 kHz",
    fFadein: "3 second fade-in",
    fFadeout: "3 second fade-out",
    fTrimAud: "Trim: from 1:00, 30s",
    fBa320: "Bitrate 320 kbps (high quality)",
    fBa128: "Bitrate 128 kbps (standard)",
    fBa64: "Bitrate 64 kbps (saver)",
    fScale800: "Width 800px, proportional height",
    fCrop: "Crop left half",
    fTile: "3x3 Mosaic",
    fBright10: "Brightness +10%",
    fCont50: "Contrast +50%",
    fSat0: "Remove saturation (B&W)",
    fSatDouble: "Double saturation",
    fVintage: "Vintage effect",
    fGamma: "Gamma +50%",
    fUnsharpHigh: "Strong sharpen",
    fUnsharpLow: "Soft sharpen",
    fBoxblurGauss: "Gaussian blur",
    fNoise: "Add noise / grain",
    fVignette: "Dark vignette on edges",
    fEdge: "Edge detection",
    },
  ES: {
    title: "ALENIA PORTER",
    uploadTitle: "CARGAR ARCHIVO DE MEDIO",
    uploadDesc: "Toca para cargar archivos o arrastra aquí",
    uploadFiles: "Subir Archivos",
    uploadFolderRecursive: "Subir Carpeta (Recursivo)",
    browseFiles: "Explorar archivos",
    processingQueue: "COLA DE PROCESAMIENTO",
    pause: "Pausar",
    process: "Procesar",
    clear: "Vaciar",
    fileChar: "CARACTERÍSTICAS DEL ARCHIVO",
    fileName: "Nombre",
    fileSize: "Tamaño",
    fileFormat: "Formato",
    fileDimensions: "Dimensiones",
    fileDuration: "Duración",
    compEstimations: "ESTIMACIONES DE COMPRESIÓN",
    original: "Original",
    estimated: "Estimado",
    savings: "Ahorro",
    downloadOptimized: "Descargar Optimizado",
    compParameters: "PARÁMETROS DE COMPRESIÓN",
    presetLabel: "PREESTABLECIDOS",
    outputFormat: "Formato de Salida",
    videoCodec: "Códec de Video",
    audioBitrate: "Tasa de Bits (Audio)",
    resolutionScale: "Resolución (Escala)",
    fps: "Frecuencia de Cuadros (FPS)",
    speedPreset: "Preajuste de Velocidad",
    customArgs: "Argumentos Personalizados de FFmpeg",
    optimizeBtn: "Optimizar Archivo",
    optimizingBtn: "Optimizando...",
    successMsg: "PROCESADO EXITOSAMENTE",
    runningMsg: "EJECUTANDO OPTIMIZACIÓN...",
    historyTitle: "HISTORIAL DE CONVERSIONES",
    clearHistory: "Vaciar",
    noHistory: "Aún no hay archivos optimizados en esta sesión.",
    settingsTitle: "Ajustes de Alenia Porter",
    visualCustomization: "Personalización Visual",
    themeLabel: "Color de Tema",
    systemSettings: "Ajustes del Sistema",
    safeMode: "Modo Seguro (Safe Mode)",
    safeModeDesc: "Fuerza codificación CPU de respaldo",
    hardwareAcceleration: "Aceleración de Hardware",
    hwDetected: "Detectado",
    none: "Ninguno",
    downloadCrashDump: "DESCARGAR CRASH DUMP",
    crashDumpDesc: "Genera un volcado de memoria simulado ante errores WASM",
    sendTelemetry: "Enviar Telemetría Anónima",
    communityDashboard: "DASHBOARD COMUNITARIO GLOBAL",
    files: "Archivos",
    bytesSaved: "Bytes Ahorrados",
    apiRequests: "Peticiones API",
    users: "Usuarios",
    supportTitle: "Rendimiento y Soporte",
    privacyTitle: "Privacidad y Estadísticas",
    versionInfo: "Información de Versión",
    changelog: "Registro de Cambios y Actualizaciones",
    close: "Cerrar",
    updateAvailable: "¡Nueva versión disponible!",
    clickToUpdate: "Haz clic para actualizar",
    originalScale: "Escala Original",
    originalFps: "FPS Original",
    optimizationSuccess: "¡Optimización finalizada! Se comprimió un {savings}% del archivo original.",
    initLog: "[Alenia FFmpeg] Iniciando compilación de medios...",
    sourceFile: "[Alenia FFmpeg] Archivo origen: ",
    commandLog: "[Alenia FFmpeg] Comando: ",
    cacheMatch: "[Smart-Cache] ¡Coincidencia de huella digital MD5/SHA en el caché local!",
    cacheSkip: "[Smart-Cache] Omitiendo compilación redundante para: ",
    supportedFormats: "Formatos Soportados",
    supportedFormatsDesc: "Todos los formatos que acepta ordenados por categoría de medio:",
    supportSection: "Apoyar a Alenia Studios",
    supportDesc: "Configuración oficial de apoyo para Alenia Studios. ¡Tu apoyo nos permite seguir creando herramientas de libre uso para la comunidad!",
    donatePaypal: "Donar vía PayPal",
    hwDetectedLabel: "Detectado",
    crashDumpBtn: "DESCARGAR CRASH DUMP",
    nicknameAlias: "Alias",
    nicknameSave: "Guardar",
    nicknameCancel: "Cancelar",
    nicknameEdit: "Editar",
    themeWhite: "Blanco",
    themeDark: "Oscuro",
    themeCream: "Crema",

    formulaGroupVideoImage: "VIDEO — IMAGEN",
    formulaGroupVideoImageDesc: "Transformaciones visuales, recortes y filtros",
    formulaGroupVideoAudio: "VIDEO — AUDIO",
    formulaGroupVideoAudioDesc: "Gestión de pistas de audio y extracción",
    formulaGroupVideoTime: "VIDEO — TIEMPO Y FPS",
    formulaGroupVideoTimeDesc: "Control de velocidad, framerate y recortes",
    formulaGroupVideoStream: "VIDEO — FORMATOS Y CÓDECS",
    formulaGroupVideoStreamDesc: "Cambiar formatos, códecs y optimización web",

    formulaGroupAudioVol: "AUDIO — VOLUMEN",
    formulaGroupAudioVolDesc: "Ajustes de normalización y ganancia",
    formulaGroupAudioChannel: "AUDIO — CANALES Y FRECUENCIA",
    formulaGroupAudioChannelDesc: "Conversión mono/estéreo y muestreo",
    formulaGroupAudioFx: "AUDIO — EFECTOS",
    formulaGroupAudioFxDesc: "Filtros, ecos, y desvanecimientos",
    formulaGroupAudioBitrate: "AUDIO — BITRATE Y RECORTES",
    formulaGroupAudioBitrateDesc: "Calidad de compresión y edición de tiempo",
    
    formulaGroupImageTransform: "IMAGEN — TRANSFORMACIÓN",
    formulaGroupImageTransformDesc: "Redimensionar, rotar y recortar",
    formulaGroupImageColor: "IMAGEN — COLOR",
    formulaGroupImageColorDesc: "Ajuste de brillo, contraste y filtros",
    formulaGroupImageFx: "IMAGEN — EFECTOS",
    formulaGroupImageFxDesc: "Desenfocar, afilar y viñetas",
    formulaFormulas: "Fórmulas",
    
    fHflip: "Espejo horizontal",
    fVflip: "Voltear verticalmente",
    fTrans1: "Rotar 90° derecha",
    fTrans2: "Rotar 90° izquierda",
    fGray: "Escala de grises",
    fNegate: "Colores negativos",
    fBright5: "Brillo +5%",
    fCont30: "Contraste +30%",
    fSat50: "Saturación +50%",
    fUnsharp: "Nitidez (sharpen)",
    fBoxblur: "Desenfoque suave",
    fScale1280: "Ancho 1280px, alto auto",
    fPadLetterbox: "Letterbox 1920x1080",
    fAn: "Eliminar pista de audio",
    fVn: "Extraer solo audio (sin video)",
    fCaCopy: "Copiar audio sin recodificar",
    fAfVol15: "Amplificar audio +50%",
    fLoudnorm: "Normalizar volumen (EBU R128)",
    fSsTrim: "Recortar: desde 0:30, dur. 60s",
    fR30: "Fijar FPS a 30",
    fR60: "Fijar FPS a 60",
    fSetpts05: "Velocidad x2 (timelapse)",
    fSetpts20: "Camara lenta x0.5",
    fCvCopy: "Copiar video sin recodificar",
    fMovflags: "Optimizar para streaming web",
    fThreads4: "Forzar 4 hilos de CPU",
    fBv2m: "Bitrate fijo 2 Mbps",
    fCrf18: "Calidad alta (CRF 18)",
    fVol20: "Doblar volumen (+100%)",
    fVol05: "Reducir a la mitad",
    fDynaudnorm: "Normalizacion dinamica",
    fAgate: "Noise gate (silencio)",
    fAc1: "Convertir a Mono",
    fAc2: "Forzar Stereo",
    fAr44: "Sample rate 44.1 kHz (CD)",
    fAr48: "Sample rate 48 kHz (video)",
    fAr22: "Sample rate 22 kHz (web)",
    fAtempo15: "Velocidad x1.5 (sin pitch)",
    fAtempo075: "Velocidad x0.75 (sin pitch)",
    fAecho: "Eco / reverb",
    fHighpass: "Filtro high-pass 200 Hz",
    fLowpass: "Filtro low-pass 3 kHz",
    fFadein: "Fade-in de 3 segundos",
    fFadeout: "Fade-out de 3 segundos",
    fTrimAud: "Recortar: desde 1:00, 30s",
    fBa320: "Bitrate 320 kbps (alta calidad)",
    fBa128: "Bitrate 128 kbps (estandar)",
    fBa64: "Bitrate 64 kbps (ahorro)",
    fScale800: "Ancho 800px, alto proporcional",
    fCrop: "Recortar mitad izquierda",
    fTile: "Mosaico 3x3",
    fBright10: "Brillo +10%",
    fCont50: "Contraste +50%",
    fSat0: "Quitar saturacion (BN)",
    fSatDouble: "Saturacion doble",
    fVintage: "Efecto vintage",
    fGamma: "Gamma +50%",
    fUnsharpHigh: "Sharpen fuerte",
    fUnsharpLow: "Sharpen suave",
    fBoxblurGauss: "Desenfoque gaussiano",
    fNoise: "Añadir ruido / grano",
    fVignette: "Viñeta oscura en bordes",
    fEdge: "Deteccion de bordes",
    },
  FR: {
    title: "ALENIA PORTER",
    uploadTitle: "CHARGER UN FICHIER MULTIMÉDIA",
    uploadDesc: "Appuyez pour charger ou glissez ici",
    uploadFiles: "Télécharger des fichiers",
    uploadFolderRecursive: "Télécharger un dossier (Récursif)",
    browseFiles: "Parcourir les fichiers",
    processingQueue: "FILE D'ATTENTE DE TRAITEMENT",
    pause: "Pause",
    process: "Traiter",
    clear: "Vider",
    fileChar: "CARACTÉRISTIQUES DU FICHIER",
    fileName: "Nom",
    fileSize: "Taille",
    fileFormat: "Format",
    fileDimensions: "Dimensions",
    fileDuration: "Durée",
    compEstimations: "ESTIMATIONS DE COMPRESSION",
    original: "Original",
    estimated: "Estimé",
    savings: "Économie",
    downloadOptimized: "Télécharger l'optimisé",
    compParameters: "PARAMÈTRES DE COMPRESSION",
    presetLabel: "PRÉRÉGLAGES",
    outputFormat: "Format de Sortie",
    videoCodec: "Codec Vidéo",
    audioBitrate: "Débit Audio",
    resolutionScale: "Résolution (Échelle)",
    fps: "Taux de Trames (FPS)",
    speedPreset: "Préréglage de Vitesse",
    customArgs: "Arguments FFmpeg Personnalisés",
    optimizeBtn: "Optimiser le Fichier",
    optimizingBtn: "Optimisation...",
    successMsg: "TRAITÉ AVEC SUCCÈS",
    runningMsg: "OPTIMISATION EN COURS...",
    historyTitle: "HISTORIQUE DES CONVERSIONS",
    clearHistory: "Vider",
    noHistory: "Aucun fichier optimisé dans cette session.",
    settingsTitle: "Paramètres d'Alenia Porter",
    visualCustomization: "Personnalisation Visuelle",
    themeLabel: "Couleur du Thème",
    systemSettings: "Paramètres Système",
    safeMode: "Mode Sans Échec (Safe Mode)",
    safeModeDesc: "Force l'encodage CPU de secours",
    hardwareAcceleration: "Accélération Matérielle",
    hwDetected: "Détecté",
    none: "Aucun",
    downloadCrashDump: "TÉLÉCHARGER LE CRASH DUMP",
    crashDumpDesc: "Génère un vidage de mémoire simulé en cas d'erreurs WASM",
    sendTelemetry: "Envoyer la Télémétrie Anonyme",
    communityDashboard: "TABLEAU DE BORD COMMUNAUTAIRE GLOBAL",
    files: "Fichiers",
    bytesSaved: "Octets Économisés",
    apiRequests: "Requêtes API",
    users: "Utilisateurs",
    supportTitle: "Performance & Support",
    privacyTitle: "Confidentialité & Statistiques",
    versionInfo: "Informations de Version",
    changelog: "Journal des Modifications",
    close: "Fermer",
    updateAvailable: "Nouvelle version disponible !",
    clickToUpdate: "Cliquez pour mettre à jour",
    originalScale: "Échelle Originale",
    originalFps: "FPS Originaux",
    optimizationSuccess: "Optimisation terminée ! {savings}% du fichier original compressé.",
    initLog: "[Alenia FFmpeg] Début de la compilation des médias...",
    sourceFile: "[Alenia FFmpeg] Fichier source : ",
    commandLog: "[Alenia FFmpeg] Commande : ",
    cacheMatch: "[Smart-Cache] Correspondance de l'empreinte MD5/SHA dans le cache local !",
    cacheSkip: "[Smart-Cache] Ignorer la compilation redondante pour : ",
    supportedFormats: "Formats Supportés",
    supportedFormatsDesc: "Tous les formats acceptés classés par catégorie de média :",
    supportSection: "Soutenir Alenia Studios",
    supportDesc: "Options de soutien officielles pour Alenia Studios. Votre soutien nous permet de continuer à créer des outils gratuits !",
    donatePaypal: "Faire un don via PayPal",
    hwDetectedLabel: "Détecté",
    crashDumpBtn: "TÉLÉCHARGER CRASH DUMP",
    nicknameAlias: "Alias",
    nicknameSave: "Enregistrer",
    nicknameCancel: "Annuler",
    nicknameEdit: "Modifier",
    themeWhite: "Blanc",
    themeDark: "Sombre",
    themeCream: "Crème",

    formulaGroupVideoImage: "VIDÉO — IMAGE",
    formulaGroupVideoImageDesc: "Transformations visuelles, recadrage et filtres",
    formulaGroupVideoAudio: "VIDÉO — AUDIO",
    formulaGroupVideoAudioDesc: "Gestion des pistes audio et extraction",
    formulaGroupVideoTime: "VIDÉO — TEMPS ET FPS",
    formulaGroupVideoTimeDesc: "Contrôle de la vitesse, framerate et découpage",
    formulaGroupVideoStream: "VIDÉO — FORMATS ET CODECS",
    formulaGroupVideoStreamDesc: "Changer de formats, codecs et optimisation web",

    formulaGroupAudioVol: "AUDIO — VOLUME",
    formulaGroupAudioVolDesc: "Ajustements de normalisation et gain",
    formulaGroupAudioChannel: "AUDIO — CANAUX ET FRÉQUENCE",
    formulaGroupAudioChannelDesc: "Conversion mono/stéréo et échantillonnage",
    formulaGroupAudioFx: "AUDIO — EFFETS",
    formulaGroupAudioFxDesc: "Filtres, échos et fondus",
    formulaGroupAudioBitrate: "AUDIO — DÉBIT ET DÉCOUPAGE",
    formulaGroupAudioBitrateDesc: "Qualité de compression et édition temporelle",
    
    formulaGroupImageTransform: "IMAGE — TRANSFORMER",
    formulaGroupImageTransformDesc: "Redimensionner, pivoter et recadrer",
    formulaGroupImageColor: "IMAGE — COULEUR",
    formulaGroupImageColorDesc: "Luminosité, contraste et filtres",
    formulaGroupImageFx: "IMAGE — EFFETS",
    formulaGroupImageFxDesc: "Flou, netteté et vignettes",
    formulaFormulas: "Formules",
    
    fHflip: "Miroir horizontal",
    fVflip: "Retourner verticalement",
    fTrans1: "Pivoter 90° à droite",
    fTrans2: "Pivoter 90° à gauche",
    fGray: "Niveaux de gris",
    fNegate: "Couleurs négatives",
    fBright5: "Luminosité +5%",
    fCont30: "Contraste +30%",
    fSat50: "Saturation +50%",
    fUnsharp: "Netteté (sharpen)",
    fBoxblur: "Flou doux",
    fScale1280: "Largeur 1280px, hauteur auto",
    fPadLetterbox: "Letterbox 1920x1080",
    fAn: "Supprimer la piste audio",
    fVn: "Extraire l'audio uniquement",
    fCaCopy: "Copier l'audio sans réencoder",
    fAfVol15: "Amplifier l'audio +50%",
    fLoudnorm: "Normaliser le volume (EBU R128)",
    fSsTrim: "Découper : de 0:30, dur. 60s",
    fR30: "Fixer FPS à 30",
    fR60: "Fixer FPS à 60",
    fSetpts05: "Vitesse x2 (timelapse)",
    fSetpts20: "Ralenti x0.5",
    fCvCopy: "Copier la vidéo sans réencoder",
    fMovflags: "Optimiser pour le web streaming",
    fThreads4: "Forcer 4 threads CPU",
    fBv2m: "Débit fixe 2 Mbps",
    fCrf18: "Haute qualité (CRF 18)",
    fVol20: "Double volume (+100%)",
    fVol05: "Réduire de moitié",
    fDynaudnorm: "Normalisation dynamique",
    fAgate: "Noise gate (silence)",
    fAc1: "Convertir en Mono",
    fAc2: "Forcer Stéréo",
    fAr44: "Taux d'échantillonnage 44.1 kHz",
    fAr48: "Taux d'échantillonnage 48 kHz",
    fAr22: "Taux d'échantillonnage 22 kHz",
    fAtempo15: "Vitesse x1.5 (sans changer le pitch)",
    fAtempo075: "Vitesse x0.75 (sans changer le pitch)",
    fAecho: "Écho / réverbération",
    fHighpass: "Filtre passe-haut 200 Hz",
    fLowpass: "Filtre passe-bas 3 kHz",
    fFadein: "Fondu entrant 3 secondes",
    fFadeout: "Fondu sortant 3 secondes",
    fTrimAud: "Découper : de 1:00, 30s",
    fBa320: "Débit 320 kbps (haute qualité)",
    fBa128: "Débit 128 kbps (standard)",
    fBa64: "Débit 64 kbps (économie)",
    fScale800: "Largeur 800px, hauteur prop.",
    fCrop: "Recadrer moitié gauche",
    fTile: "Mosaïque 3x3",
    fBright10: "Luminosité +10%",
    fCont50: "Contraste +50%",
    fSat0: "Supprimer saturation (N&B)",
    fSatDouble: "Saturation double",
    fVintage: "Effet vintage",
    fGamma: "Gamma +50%",
    fUnsharpHigh: "Netteté forte",
    fUnsharpLow: "Netteté douce",
    fBoxblurGauss: "Flou gaussien",
    fNoise: "Ajouter du bruit / grain",
    fVignette: "Vignette sombre sur les bords",
    fEdge: "Détection des contours",
    },
  JP: {
    title: "アレニア・ポーター",
    uploadTitle: "メディアファイルのアップロード",
    uploadDesc: "タップして読み込むか、ここにドラッグ",
    uploadFiles: "ファイルをアップロード",
    uploadFolderRecursive: "フォルダをアップロード (再帰的)",
    browseFiles: "ファイルを閲覧",
    processingQueue: "処理キュー",
    pause: "一時停止",
    process: "処理開始",
    clear: "クリア",
    fileChar: "ファイル属性",
    fileName: "ファイル名",
    fileSize: "サイズ",
    fileFormat: "フォーマット",
    fileDimensions: "解像度",
    fileDuration: "再生時間",
    compEstimations: "圧縮推定",
    original: "オリジナル",
    estimated: "推定サイズ",
    savings: "節約量",
    downloadOptimized: "最適化版をダウンロード",
    compParameters: "圧縮パラメーター",
    presetLabel: "プリセット",
    outputFormat: "出力形式",
    videoCodec: "ビデオコーデック",
    audioBitrate: "音声ビットレート",
    resolutionScale: "解像度（スケール）",
    fps: "フレームレート（FPS）",
    speedPreset: "速度プリセット",
    customArgs: "カスタムFFmpeg引数",
    optimizeBtn: "ファイルを最適化",
    optimizingBtn: "最適化中...",
    successMsg: "正常に処理されました",
    runningMsg: "最適化を実行中...",
    historyTitle: "変換履歴",
    clearHistory: "クリア",
    noHistory: "このセッションの最適化済みファイルはまだありません。",
    settingsTitle: "アレニア・ポーターの設定",
    visualCustomization: "外観のカスタマイズ",
    themeLabel: "テーマカラー",
    systemSettings: "システム設定",
    safeMode: "セーフモード",
    safeModeDesc: "CPUバックアップエンコードを強制する",
    hardwareAcceleration: "ハードウェアアクセラレーション",
    hwDetected: "検出",
    none: "なし",
    downloadCrashDump: "クラッシュダンプをダウンロード",
    crashDumpDesc: "WASMエラーに備えて模擬メモリダンプを生成します",
    sendTelemetry: "匿名テレメトリを送信する",
    communityDashboard: "グローバルコミュニティダッシュボード",
    files: "ファイル数",
    bytesSaved: "節約バイト数",
    apiRequests: "APIリクエスト",
    users: "ユーザー数",
    supportTitle: "パフォーマンスとサポート",
    privacyTitle: "プライバシーと統計",
    versionInfo: "バージョン情報",
    changelog: "変更履歴とアップデート",
    close: "閉じる",
    updateAvailable: "新しいバージョンがあります！",
    clickToUpdate: "クリックしてアップデート",
    originalScale: "元のスケール",
    originalFps: "元のFPS",
    optimizationSuccess: "最適化が完了しました。元のファイルの {savings}% が圧縮されました。",
    initLog: "[Alenia FFmpeg] メディアのコンパイルを開始しています...",
    sourceFile: "[Alenia FFmpeg] ソースファイル: ",
    commandLog: "[Alenia FFmpeg] コマンド: ",
    cacheMatch: "[Smart-Cache] ローカルキャッシュにMD5/SHAフィンガープリントが一致しました！",
    cacheSkip: "[Smart-Cache] 冗長なコンパイルをスキップしています: ",
    supportedFormats: "対応フォーマット",
    supportedFormatsDesc: "対応しているすべてのフォーマットをメディアカテゴリ別に:",
    supportSection: "Alenia Studiosを支援する",
    supportDesc: "Alenia Studiosの公式サポートオプション。あなたの支援で無料ツールを作り続けられます！",
    donatePaypal: "PayPalで寄付",
    hwDetectedLabel: "検出済み",
    crashDumpBtn: "クラッシュダンプをダウンロード",
    nicknameAlias: "エイリアス",
    nicknameSave: "保存",
    nicknameCancel: "キャンセル",
    nicknameEdit: "編集",
    themeWhite: "ホワイト",
    themeDark: "ダーク",
    themeCream: "クリーム",

    formulaGroupVideoImage: "ビデオ — 画像",
    formulaGroupVideoAudio: "ビデオ — 音声",
    formulaGroupVideoTime: "ビデオ — 時間",
    formulaGroupVideoStream: "ビデオ — ストリーム",
    formulaGroupAudioVol: "音声 — 音量",
    formulaGroupAudioChannel: "音声 — チャンネル/サンプル",
    formulaGroupAudioFx: "音声 — エフェクト",
    formulaGroupAudioBitrate: "音声 — ビットレート/トリム",
    formulaGroupImageTransform: "画像 — 変形",
    formulaGroupImageColor: "画像 — 色彩",
    formulaGroupImageFx: "画像 — エフェクト",
    formulaFormulas: "数式 (Formulas)",
    
    fHflip: "左右反転",
    fVflip: "上下反転",
    fTrans1: "右に90度回転",
    fTrans2: "左に90度回転",
    fGray: "グレースケール",
    fNegate: "色を反転",
    fBright5: "明るさ +5%",
    fCont30: "コントラスト +30%",
    fSat50: "彩度 +50%",
    fUnsharp: "シャープネス",
    fBoxblur: "ソフトなぼかし",
    fScale1280: "幅1280px、高さ自動",
    fPadLetterbox: "レターボックス 1920x1080",
    fAn: "音声トラックを削除",
    fVn: "音声のみ抽出",
    fCaCopy: "再エンコードせずに音声をコピー",
    fAfVol15: "音量を+50%増幅",
    fLoudnorm: "音量を正規化 (EBU R128)",
    fSsTrim: "トリミング: 0:30から、長さ60秒",
    fR30: "FPSを30に固定",
    fR60: "FPSを60に固定",
    fSetpts05: "速度x2 (タイムラプス)",
    fSetpts20: "スローモーションx0.5",
    fCvCopy: "再エンコードせずにビデオをコピー",
    fMovflags: "Webストリーミング用に最適化",
    fThreads4: "4 CPUスレッドを強制",
    fBv2m: "固定ビットレート 2 Mbps",
    fCrf18: "高品質 (CRF 18)",
    fVol20: "音量を2倍 (+100%)",
    fVol05: "音量を半分に減らす",
    fDynaudnorm: "動的正規化",
    fAgate: "ノイズゲート (無音)",
    fAc1: "モノラルに変換",
    fAc2: "ステレオを強制",
    fAr44: "サンプルレート 44.1 kHz (CD)",
    fAr48: "サンプルレート 48 kHz (ビデオ)",
    fAr22: "サンプルレート 22 kHz (Web)",
    fAtempo15: "速度 x1.5 (ピッチ変更なし)",
    fAtempo075: "速度 x0.75 (ピッチ変更なし)",
    fAecho: "エコー / リバーブ",
    fHighpass: "ハイパスフィルター 200 Hz",
    fLowpass: "ローパスフィルター 3 kHz",
    fFadein: "3秒のフェードイン",
    fFadeout: "3秒のフェードアウト",
    fTrimAud: "トリミング: 1:00から、長さ30秒",
    fBa320: "ビットレート 320 kbps (高品質)",
    fBa128: "ビットレート 128 kbps (標準)",
    fBa64: "ビットレート 64 kbps (節約)",
    fScale800: "幅800px、高さ比例",
    fCrop: "左半分を切り抜き",
    fTile: "3x3 モザイク",
    fBright10: "明るさ +10%",
    fCont50: "コントラスト +50%",
    fSat0: "彩度を削除 (白黒)",
    fSatDouble: "彩度を2倍",
    fVintage: "ヴィンテージ効果",
    fGamma: "ガンマ +50%",
    fUnsharpHigh: "強いシャープネス",
    fUnsharpLow: "弱いシャープネス",
    fBoxblurGauss: "ガウスぼかし",
    fNoise: "ノイズ/粒子を追加",
    fVignette: "エッジに暗いビネット",
    fEdge: "エッジ検出",
    },
  CN: {
    title: "阿莱尼亚传送门",
    uploadTitle: "上传媒体文件",
    uploadDesc: "点击加载文件或拖拽至此",
    uploadFiles: "上传文件",
    uploadFolderRecursive: "上传文件夹 (递归)",
    browseFiles: "浏览文件",
    processingQueue: "处理队列",
    pause: "暂停",
    process: "开始处理",
    clear: "清空",
    fileChar: "文件属性",
    fileName: "文件名",
    fileSize: "原始大小",
    fileFormat: "格式",
    fileDimensions: "分辨率",
    fileDuration: "时长",
    compEstimations: "压缩估算",
    original: "原始大小",
    estimated: "估算大小",
    savings: "节省空间",
    downloadOptimized: "下载优化版",
    compParameters: "压缩参数设置",
    presetLabel: "预设方案",
    outputFormat: "输出格式",
    videoCodec: "视频编码器",
    audioBitrate: "音频比特率",
    resolutionScale: "分辨率缩放",
    fps: "帧率 (FPS)",
    speedPreset: "编码速度预设",
    customArgs: "自定义 FFmpeg 参数",
    optimizeBtn: "开始优化文件",
    optimizingBtn: "正在优化...",
    successMsg: "处理完成",
    runningMsg: "正在执行优化...",
    historyTitle: "转换历史记录",
    clearHistory: "清空",
    noHistory: "当前会话暂无优化文件记录。",
    settingsTitle: "阿莱尼亚传送门设置",
    visualCustomization: "视觉个性化",
    themeLabel: "主题色彩",
    systemSettings: "系统设置",
    safeMode: "安全模式 (Safe Mode)",
    safeModeDesc: "强制使用CPU备份编码",
    hardwareAcceleration: "硬件加速",
    hwDetected: "已检测到",
    none: "无",
    downloadCrashDump: "下载崩溃转储文件",
    crashDumpDesc: "在WASM发生错误时生成模拟内存转储",
    sendTelemetry: "发送匿名使用统计",
    communityDashboard: "全球社区统计看板",
    files: "已处理文件",
    bytesSaved: "累计节省空间",
    apiRequests: "API 请求数",
    users: "独立用户数",
    supportTitle: "性能与技术支持",
    privacyTitle: "隐私与数据统计",
    versionInfo: "版本信息",
    changelog: "更新日志与历史版本",
    close: "关闭",
    updateAvailable: "发现新版本！",
    clickToUpdate: "点击下载更新",
    originalScale: "原始比例",
    originalFps: "原始帧率",
    optimizationSuccess: "优化完成！已压缩原始文件的 {savings}%。",
    initLog: "[Alenia FFmpeg] 正在启动媒体编译...",
    sourceFile: "[Alenia FFmpeg] 源文件: ",
    commandLog: "[Alenia FFmpeg] 命令: ",
    cacheMatch: "[Smart-Cache] 本地缓存中匹配到 MD5/SHA 指纹！",
    cacheSkip: "[Smart-Cache] 正在跳过冗余编译： ",
    supportedFormats: "支持的格式",
    supportedFormatsDesc: "按媒体类别列出的所有支持格式：",
    supportSection: "支持 Alenia Studios",
    supportDesc: "Alenia Studios官方支持选项。您的支持让我们能够继续为社区创建免费工具！",
    donatePaypal: "通过PayPal捐赠",
    hwDetectedLabel: "已检测",
    crashDumpBtn: "下载崩溃转储",
    nicknameAlias: "别名",
    nicknameSave: "保存",
    nicknameCancel: "取消",
    nicknameEdit: "编辑",
    themeWhite: "白色",
    themeDark: "深色",
    themeCream: "奶油",

    formulaGroupVideoImage: "视频 — 图像",
    formulaGroupVideoAudio: "视频 — 音频",
    formulaGroupVideoTime: "视频 — 时间",
    formulaGroupVideoStream: "视频 — 流",
    formulaGroupAudioVol: "音频 — 音量",
    formulaGroupAudioChannel: "音频 — 通道/采样",
    formulaGroupAudioFx: "音频 — 效果",
    formulaGroupAudioBitrate: "音频 — 比特率/剪裁",
    formulaGroupImageTransform: "图像 — 变换",
    formulaGroupImageColor: "图像 — 颜色",
    formulaGroupImageFx: "图像 — 效果",
    formulaFormulas: "公式 (Formulas)",
    
    fHflip: "水平翻转",
    fVflip: "垂直翻转",
    fTrans1: "向右旋转90度",
    fTrans2: "向左旋转90度",
    fGray: "灰度",
    fNegate: "反色",
    fBright5: "亮度 +5%",
    fCont30: "对比度 +30%",
    fSat50: "饱和度 +50%",
    fUnsharp: "锐化",
    fBoxblur: "柔和模糊",
    fScale1280: "宽 1280px，高自动",
    fPadLetterbox: "信箱模式 1920x1080",
    fAn: "移除音频轨",
    fVn: "仅提取音频",
    fCaCopy: "不重新编码复制音频",
    fAfVol15: "放大音频 +50%",
    fLoudnorm: "音量标准化 (EBU R128)",
    fSsTrim: "修剪：从 0:30，时长 60s",
    fR30: "固定FPS为30",
    fR60: "固定FPS为60",
    fSetpts05: "速度x2 (延时摄影)",
    fSetpts20: "慢动作x0.5",
    fCvCopy: "不重新编码复制视频",
    fMovflags: "为Web流媒体优化",
    fThreads4: "强制4个CPU线程",
    fBv2m: "固定比特率 2 Mbps",
    fCrf18: "高质量 (CRF 18)",
    fVol20: "双倍音量 (+100%)",
    fVol05: "减半音量",
    fDynaudnorm: "动态标准化",
    fAgate: "噪声门限 (静音)",
    fAc1: "转换为单声道",
    fAc2: "强制立体声",
    fAr44: "采样率 44.1 kHz (CD)",
    fAr48: "采样率 48 kHz (视频)",
    fAr22: "采样率 22 kHz (Web)",
    fAtempo15: "速度 x1.5 (不变调)",
    fAtempo075: "速度 x0.75 (不变调)",
    fAecho: "回声 / 混响",
    fHighpass: "高通滤波器 200 Hz",
    fLowpass: "低通滤波器 3 kHz",
    fFadein: "3秒淡入",
    fFadeout: "3秒淡出",
    fTrimAud: "修剪：从 1:00，时长 30s",
    fBa320: "比特率 320 kbps (高质量)",
    fBa128: "比特率 128 kbps (标准)",
    fBa64: "比特率 64 kbps (节省)",
    fScale800: "宽 800px，高按比例",
    fCrop: "裁剪左半部分",
    fTile: "3x3 马赛克",
    fBright10: "亮度 +10%",
    fCont50: "对比度 +50%",
    fSat0: "去除饱和度 (黑白)",
    fSatDouble: "双倍饱和度",
    fVintage: "复古效果",
    fGamma: "伽马 +50%",
    fUnsharpHigh: "强锐化",
    fUnsharpLow: "柔和锐化",
    fBoxblurGauss: "高斯模糊",
    fNoise: "添加噪点/颗粒",
    fVignette: "边缘暗角",
    fEdge: "边缘检测",
    },
  RU: {
    title: "ALENIA PORTER",
    uploadTitle: "ЗАГРУЗИТЬ МЕДИАФАЙЛ",
    uploadDesc: "Нажмите для загрузки или перетащите сюда",
    uploadFiles: "Загрузить файлы",
    uploadFolderRecursive: "Загрузить папку (рекурсивно)",
    browseFiles: "Обзор файлов",
    processingQueue: "ОЧЕРЕДЬ ОБРАБОТКИ",
    pause: "Пауза",
    process: "Запустить",
    clear: "Очистить",
    fileChar: "ХАРАКТЕРИСТИКИ ФАЙЛА",
    fileName: "Имя файла",
    fileSize: "Размер",
    fileFormat: "Формат",
    fileDimensions: "Разрешение",
    fileDuration: "Длительность",
    compEstimations: "ОЦЕНКА СЖАТИЯ",
    original: "Оригинал",
    estimated: "Ожидаемый",
    savings: "Экономия",
    downloadOptimized: "Скачать оптимизированный",
    compParameters: "ПАРАМЕТРЫ СЖАТИЯ",
    presetLabel: "ПРЕСЕТЫ",
    outputFormat: "Выходной формат",
    videoCodec: "Видеокодек",
    audioBitrate: "Аудиобитрейт",
    resolutionScale: "Разрешение (Масштаб)",
    fps: "Частота кадров (FPS)",
    speedPreset: "Пресет скорости",
    customArgs: "Свои аргументы FFmpeg",
    optimizeBtn: "Оптимизировать файл",
    optimizingBtn: "Оптимизация...",
    successMsg: "УСПЕШНО ОБРАБОТАНО",
    runningMsg: "ВЫПОЛНЯЕТСЯ ОПТИМИЗАЦИЯ...",
    historyTitle: "ИСТОРИЯ КОНВЕРТАЦИЙ",
    clearHistory: "Очистить",
    noHistory: "В этой сессии пока нет оптимизированных файлов.",
    settingsTitle: "Настройки Alenia Porter",
    visualCustomization: "Визуальная настройка",
    themeLabel: "Цвет темы",
    systemSettings: "Системные настройки",
    safeMode: "Безопасный режим (Safe Mode)",
    safeModeDesc: "Принудительное резервное кодирование процессором",
    hardwareAcceleration: "Аппаратное ускорение",
    hwDetected: "Обнаружено",
    none: "Нет",
    downloadCrashDump: "СКАЧАТЬ ДАМП АВАРИИ",
    crashDumpDesc: "Создает симулированный дамп памяти в случае ошибок WASM",
    sendTelemetry: "Отправлять анонимную телеметрию",
    communityDashboard: "ГЛОБАЛЬНАЯ СТАТИСТИКА СООБЩЕСТВА",
    files: "Файлы",
    bytesSaved: "Байт сэкономлено",
    apiRequests: "Запросы API",
    users: "Пользователи",
    supportTitle: "Производительность и поддержка",
    privacyTitle: "Конфиденциальность и статистика",
    versionInfo: "Информация о версии",
    changelog: "История изменений и обновления",
    close: "Закрыть",
    updateAvailable: "Доступна новая версия!",
    clickToUpdate: "Нажмите, чтобы обновить",
    originalScale: "Исходный масштаб",
    originalFps: "Исходный FPS",
    optimizationSuccess: "Оптимизация завершена! Сжато {savings}% от исходного файла.",
    initLog: "[Alenia FFmpeg] Запуск компиляции медиа...",
    sourceFile: "[Alenia FFmpeg] Исходный файл: ",
    commandLog: "[Alenia FFmpeg] Команда: ",
    cacheMatch: "[Smart-Cache] Совпадение цифрового отпечатка MD5/SHA в локальном кэше!",
    cacheSkip: "[Smart-Cache] Пропуск избыточной компиляции для: ",
    supportedFormats: "Поддерживаемые форматы",
    supportedFormatsDesc: "Все поддерживаемые форматы по категориям медиа:",
    supportSection: "Поддержать Alenia Studios",
    supportDesc: "Официальные варианты поддержки Alenia Studios. Ваша поддержка помогает нам создавать бесплатные инструменты!",
    donatePaypal: "Пожертвовать через PayPal",
    hwDetectedLabel: "Обнаружено",
    crashDumpBtn: "СКАЧАТЬ CRASH DUMP",
    nicknameAlias: "Псевдоним",
    nicknameSave: "Сохранить",
    nicknameCancel: "Отмена",
    nicknameEdit: "Изменить",
    themeWhite: "Белый",
    themeDark: "Тёмный",
    themeCream: "Кремовый",
  },
  BR: {
    title: "ALENIA PORTER",
    uploadTitle: "CARREGAR ARQUIVO DE MÍDIA",
    uploadDesc: "Toque para carregar ou arraste aqui",
    uploadFiles: "Enviar Arquivos",
    uploadFolderRecursive: "Enviar Pasta (Recursivo)",
    browseFiles: "Procurar arquivos",
    processingQueue: "FILA DE PROCESSAMENTO",
    pause: "Pausar",
    process: "Processar",
    clear: "Limpar",
    fileChar: "CARACTERÍSTICAS DO ARQUIVO",
    fileName: "Nome",
    fileSize: "Tamanho",
    fileFormat: "Formato",
    fileDimensions: "Dimensões",
    fileDuration: "Duração",
    compEstimations: "ESTIMATIVAS DE COMPRESSÃO",
    original: "Original",
    estimated: "Estimado",
    savings: "Economia",
    downloadOptimized: "Baixar Otimizado",
    compParameters: "PARÂMETROS DE COMPRESSÃO",
    presetLabel: "PRESETS",
    outputFormat: "Formato de Saída",
    videoCodec: "Codec de Vídeo",
    audioBitrate: "Taxa de Bits (Áudio)",
    resolutionScale: "Resolução (Escala)",
    fps: "Taxa de Quadros (FPS)",
    speedPreset: "Predefinição de Velocidade",
    customArgs: "Argumentos Personalizados do FFmpeg",
    optimizeBtn: "Otimizar Arquivo",
    optimizingBtn: "Otimizando...",
    successMsg: "PROCESSADO COM SUCESSO",
    runningMsg: "EXECUTANDO OTIMIZAÇÃO...",
    historyTitle: "HISTÓRICO DE CONVERSÕES",
    clearHistory: "Limpar",
    noHistory: "Nenhum arquivo otimizado nesta sessão ainda.",
    settingsTitle: "Configurações do Alenia Porter",
    visualCustomization: "Personalização Visual",
    themeLabel: "Cor do Tema",
    systemSettings: "Configurações do Sistema",
    safeMode: "Modo Seguro (Safe Mode)",
    safeModeDesc: "Força codificação de backup pela CPU",
    hardwareAcceleration: "Aceleração de Hardware",
    hwDetected: "Detectado",
    none: "Nenhum",
    downloadCrashDump: "BAIXAR CRASH DUMP",
    crashDumpDesc: "Gera um dump de memória simulado em caso de erros WASM",
    sendTelemetry: "Enviar Telemetria Anônima",
    communityDashboard: "PAINEL GLOBAL DA COMUNIDADE",
    files: "Arquivos",
    bytesSaved: "Bytes Economizados",
    apiRequests: "Requisições API",
    users: "Usuários",
    supportTitle: "Desempenho & Suporte",
    privacyTitle: "Privacidade & Estatísticas",
    versionInfo: "Informações da Versão",
    changelog: "Registro de Alterações e Atualizações",
    close: "Fechar",
    updateAvailable: "Nova versão disponível!",
    clickToUpdate: "Clique para atualizar",
    originalScale: "Escala Original",
    originalFps: "FPS Original",
    optimizationSuccess: "Otimização concluída! {savings}% do arquivo original comprimido.",
    initLog: "[Alenia FFmpeg] Iniciando compilação de mídia...",
    sourceFile: "[Alenia FFmpeg] Arquivo de origem: ",
    commandLog: "[Alenia FFmpeg] Comando: ",
    cacheMatch: "[Smart-Cache] Correspondência de assinatura MD5/SHA encontrada no cache local!",
    cacheSkip: "[Smart-Cache] Ignorando compilação redundante para: ",
    supportedFormats: "Formatos Suportados",
    supportedFormatsDesc: "Todos os formatos aceitos organizados por categoria de mídia:",
    supportSection: "Apoiar o Alenia Studios",
    supportDesc: "Opções oficiais de apoio ao Alenia Studios. Seu apoio nos permite continuar criando ferramentas gratuitas!",
    donatePaypal: "Doar via PayPal",
    hwDetectedLabel: "Detectado",
    crashDumpBtn: "BAIXAR CRASH DUMP",
    nicknameAlias: "Apelido",
    nicknameSave: "Salvar",
    nicknameCancel: "Cancelar",
    nicknameEdit: "Editar",
    themeWhite: "Branco",
    themeDark: "Escuro",
    themeCream: "Creme",
  },
  DE: {
    title: "ALENIA PORTER",
    uploadTitle: "MEDIENDATEI HOCHLADEN",
    uploadDesc: "Tippen zum Laden oder hierher ziehen",
    uploadFiles: "Dateien hochladen",
    uploadFolderRecursive: "Ordner hochladen (Rekursiv)",
    browseFiles: "Dateien durchsuchen",
    processingQueue: "VERARBEITUNGSWARTESCHLANGE",
    pause: "Pause",
    process: "Starten",
    clear: "Leeren",
    fileChar: "DATEIEIGENSCHAFTEN",
    fileName: "Name",
    fileSize: "Größe",
    fileFormat: "Format",
    fileDimensions: "Dimensionen",
    fileDuration: "Dauer",
    compEstimations: "KOMPRESSIONSSCHÄTZUNG",
    original: "Original",
    estimated: "Geschätzt",
    savings: "Ersparnis",
    downloadOptimized: "Optimiertes Herunterladen",
    compParameters: "KOMPRESSIONSPARAMETER",
    presetLabel: "PRESETS",
    outputFormat: "Ausgabeformat",
    videoCodec: "Videocodec",
    audioBitrate: "Audio-Bitrate",
    resolutionScale: "Auflösung (Skalierung)",
    fps: "Bildrate (FPS)",
    speedPreset: "Geschwindigkeitspreset",
    customArgs: "Benutzerdefinierte FFmpeg-Argumente",
    optimizeBtn: "Datei optimieren",
    optimizingBtn: "Optimierung läuft...",
    successMsg: "ERFOLGREICH VERARBEITET",
    runningMsg: "OPTIMIERUNG WIRD AUSGEFÜHRT...",
    historyTitle: "KONVERTIERUNGSVERLAUF",
    clearHistory: "Leeren",
    noHistory: "Noch keine optimierten Dateien in dieser Sitzung.",
    settingsTitle: "Alenia Porter Einstellungen",
    visualCustomization: "Visuelle Anpassung",
    themeLabel: "Themenfarbe",
    systemSettings: "Systemeinstellungen",
    safeMode: "Sicherer Modus (Safe Mode)",
    safeModeDesc: "Erzwingt CPU-Backup-Codierung",
    hardwareAcceleration: "Hardware-Beschleunigung",
    hwDetected: "Erkannt",
    none: "Keine",
    downloadCrashDump: "CRASH DUMP HERUNTERLADEN",
    crashDumpDesc: "Erzeugt einen simulierten Speicherabzug im Falle von WASM-Fehlern",
    sendTelemetry: "Anonyme Telemetrie senden",
    communityDashboard: "GLOBALE COMMUNITY-STATS",
    files: "Dateien",
    bytesSaved: "Bytes gespart",
    apiRequests: "API-Anfragen",
    users: "Benutzer",
    supportTitle: "Leistung & Support",
    privacyTitle: "Datenschutz & Statistiken",
    versionInfo: "Versionsinfo",
    changelog: "Änderungsprotokoll & Updates",
    close: "Schließen",
    updateAvailable: "Neue Version verfügbar!",
    clickToUpdate: "Klicken zum Aktualisieren",
    originalScale: "Originalskalierung",
    originalFps: "Original FPS",
    optimizationSuccess: "Optimierung abgeschlossen! {savings}% der Originaldatei komprimiert.",
    initLog: "[Alenia FFmpeg] Medienkompilierung wird gestartet...",
    sourceFile: "[Alenia FFmpeg] Quelldatei: ",
    commandLog: "[Alenia FFmpeg] Befehl: ",
    cacheMatch: "[Smart-Cache] MD5/SHA-Fingerabdruck-Übereinstimmung im lokalen Cache gefunden!",
    cacheSkip: "[Smart-Cache] Redundante Kompilierung wird übersprungen für: ",
    supportedFormats: "Unterstützte Formate",
    supportedFormatsDesc: "Alle akzeptierten Formate geordnet nach Medienkategorie:",
    supportSection: "Alenia Studios unterstützen",
    supportDesc: "Offizielle Support-Optionen für Alenia Studios. Ihre Unterstützung hilft uns, weiterhin kostenlose Tools zu erstellen!",
    donatePaypal: "Über PayPal spenden",
    hwDetectedLabel: "Erkannt",
    crashDumpBtn: "CRASH DUMP HERUNTERLADEN",
    nicknameAlias: "Alias",
    nicknameSave: "Speichern",
    nicknameCancel: "Abbrechen",
    nicknameEdit: "Bearbeiten",
    themeWhite: "Weiß",
    themeDark: "Dunkel",
    themeCream: "Creme",
  }
};

export default function App() {
  const THEME_COLORS = {
    white: {
      bodyBg: "bg-slate-50",
      cardBg: "bg-white",
      cardBorder: "border-gray-200/85",
      textPrimary: "text-gray-900",
      textSecondary: "text-gray-700",
      textMuted: "text-gray-400",
      inputBg: "bg-gray-50",
      inputBorder: "border-gray-200",
      inputText: "text-gray-800",
      primary: "bg-blue-600 hover:bg-blue-500",
      textSimple: "text-blue-600",
      border: "border-blue-200",
      bgLight: "bg-blue-50/50",
      bgLightSolid: "bg-blue-50",
      ring: "focus:ring-blue-500 focus:border-blue-500",
      accentBadge: "bg-blue-50 border-blue-100 text-blue-700",
      progress: "bg-blue-600",
      dragActiveBorder: "border-blue-500 bg-blue-50/50",
      segmentBg: "bg-gray-100",
      segmentActive: "bg-white text-gray-900 shadow-xs border border-gray-200",
      segmentInactive: "text-gray-400 hover:text-gray-650",
      badgeFmt: "bg-blue-50 border border-blue-100/50 text-blue-700",
      badgeInactive: "bg-slate-100 border-slate-200 text-slate-600 hover:bg-slate-200",
      accentIcon: "text-gray-900"
    },
    blue: {
      bodyBg: "bg-blue-100",
      cardBg: "bg-blue-50/70",
      cardBorder: "border-blue-200",
      textPrimary: "text-blue-950",
      textSecondary: "text-blue-800",
      textMuted: "text-blue-500",
      inputBg: "bg-blue-50",
      inputBorder: "border-blue-200",
      inputText: "text-blue-900",
      primary: "bg-blue-600 hover:bg-blue-500",
      textSimple: "text-blue-700",
      border: "border-blue-300",
      bgLight: "bg-blue-100/50",
      bgLightSolid: "bg-blue-100",
      ring: "focus:ring-blue-500 focus:border-blue-500",
      accentBadge: "bg-blue-100 border-blue-200 text-blue-800",
      progress: "bg-blue-600",
      dragActiveBorder: "border-blue-500 bg-blue-100/50",
      segmentBg: "bg-blue-100",
      segmentActive: "bg-white text-blue-900 shadow-xs border border-blue-200",
      segmentInactive: "text-blue-600 hover:text-blue-800",
      badgeFmt: "bg-blue-100 border border-blue-200 text-blue-800",
      badgeInactive: "bg-blue-50 border-blue-200 text-blue-700 hover:bg-blue-100",
      accentIcon: "text-blue-700"
    },
    violet: {
      bodyBg: "bg-violet-100",
      cardBg: "bg-violet-50/70",
      cardBorder: "border-violet-200",
      textPrimary: "text-violet-950",
      textSecondary: "text-violet-800",
      textMuted: "text-violet-500",
      inputBg: "bg-violet-50",
      inputBorder: "border-violet-200",
      inputText: "text-violet-900",
      primary: "bg-violet-600 hover:bg-violet-500",
      textSimple: "text-violet-700",
      border: "border-violet-300",
      bgLight: "bg-violet-100/50",
      bgLightSolid: "bg-violet-100",
      ring: "focus:ring-violet-500 focus:border-violet-500",
      accentBadge: "bg-violet-100 border-violet-200 text-violet-800",
      progress: "bg-violet-600",
      dragActiveBorder: "border-violet-500 bg-violet-100/50",
      segmentBg: "bg-violet-100",
      segmentActive: "bg-white text-violet-900 shadow-xs border border-violet-200",
      segmentInactive: "text-violet-600 hover:text-violet-800",
      badgeFmt: "bg-violet-100 border border-violet-200 text-violet-800",
      badgeInactive: "bg-violet-50 border-violet-200 text-violet-700 hover:bg-violet-100",
      accentIcon: "text-violet-700"
    },
    slate: {
      bodyBg: "bg-slate-200",
      cardBg: "bg-slate-50/70",
      cardBorder: "border-slate-300",
      textPrimary: "text-slate-900",
      textSecondary: "text-slate-700",
      textMuted: "text-slate-500",
      inputBg: "bg-slate-50",
      inputBorder: "border-slate-300",
      inputText: "text-slate-900",
      primary: "bg-slate-700 hover:bg-slate-600",
      textSimple: "text-slate-700",
      border: "border-slate-400",
      bgLight: "bg-slate-200/50",
      bgLightSolid: "bg-slate-200",
      ring: "focus:ring-slate-500 focus:border-slate-500",
      accentBadge: "bg-slate-200 border-slate-300 text-slate-800",
      progress: "bg-slate-700",
      dragActiveBorder: "border-slate-500 bg-slate-200/50",
      segmentBg: "bg-slate-200",
      segmentActive: "bg-white text-slate-900 shadow-xs border border-slate-300",
      segmentInactive: "text-slate-600 hover:text-slate-800",
      badgeFmt: "bg-slate-200 border border-slate-300 text-slate-800",
      badgeInactive: "bg-slate-100 border-slate-300 text-slate-700 hover:bg-slate-200",
      accentIcon: "text-slate-700"
    },
    emerald: {
      bodyBg: "bg-emerald-100",
      cardBg: "bg-emerald-50/70",
      cardBorder: "border-emerald-200",
      textPrimary: "text-emerald-950",
      textSecondary: "text-emerald-800",
      textMuted: "text-emerald-500",
      inputBg: "bg-emerald-50",
      inputBorder: "border-emerald-200",
      inputText: "text-emerald-900",
      primary: "bg-emerald-600 hover:bg-emerald-500",
      textSimple: "text-emerald-700",
      border: "border-emerald-300",
      bgLight: "bg-emerald-100/50",
      bgLightSolid: "bg-emerald-100",
      ring: "focus:ring-emerald-500 focus:border-emerald-500",
      accentBadge: "bg-emerald-100 border-emerald-200 text-emerald-800",
      progress: "bg-emerald-600",
      dragActiveBorder: "border-emerald-500 bg-emerald-100/50",
      segmentBg: "bg-emerald-100",
      segmentActive: "bg-white text-emerald-900 shadow-xs border border-emerald-200",
      segmentInactive: "text-emerald-600 hover:text-emerald-800",
      badgeFmt: "bg-emerald-100 border border-emerald-200 text-emerald-800",
      badgeInactive: "bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100",
      accentIcon: "text-emerald-700"
    },
    rose: {
      bodyBg: "bg-rose-100",
      cardBg: "bg-rose-50/70",
      cardBorder: "border-rose-200",
      textPrimary: "text-rose-950",
      textSecondary: "text-rose-800",
      textMuted: "text-rose-500",
      inputBg: "bg-rose-50",
      inputBorder: "border-rose-200",
      inputText: "text-rose-900",
      primary: "bg-rose-600 hover:bg-rose-500",
      textSimple: "text-rose-700",
      border: "border-rose-300",
      bgLight: "bg-rose-100/50",
      bgLightSolid: "bg-rose-100",
      ring: "focus:ring-rose-500 focus:border-rose-500",
      accentBadge: "bg-rose-100 border-rose-200 text-rose-800",
      progress: "bg-rose-600",
      dragActiveBorder: "border-rose-500 bg-rose-100/50",
      segmentBg: "bg-rose-100",
      segmentActive: "bg-white text-rose-900 shadow-xs border border-rose-200",
      segmentInactive: "text-rose-600 hover:text-rose-800",
      badgeFmt: "bg-rose-100 border border-rose-200 text-rose-800",
      badgeInactive: "bg-rose-50 border-rose-200 text-rose-700 hover:bg-rose-100",
      accentIcon: "text-rose-700"
    },
    dark: {
      bodyBg: "bg-gray-950",
      cardBg: "bg-gray-900",
      cardBorder: "border-gray-700",
      textPrimary: "text-gray-50",
      textSecondary: "text-gray-300",
      textMuted: "text-gray-500",
      inputBg: "bg-gray-800",
      inputBorder: "border-gray-600",
      inputText: "text-gray-100",
      primary: "bg-indigo-500 hover:bg-indigo-400",
      textSimple: "text-indigo-400",
      border: "border-indigo-500",
      bgLight: "bg-indigo-950/50",
      bgLightSolid: "bg-gray-800",
      ring: "focus:ring-indigo-500 focus:border-indigo-500",
      accentBadge: "bg-indigo-950 border-indigo-800 text-indigo-300",
      progress: "bg-indigo-500",
      dragActiveBorder: "border-indigo-500 bg-indigo-950/50",
      segmentBg: "bg-gray-800",
      segmentActive: "bg-gray-700 text-gray-50 shadow-xs border border-gray-600",
      segmentInactive: "text-gray-400 hover:text-gray-200",
      badgeFmt: "bg-indigo-950 border border-indigo-800 text-indigo-300",
      badgeInactive: "bg-gray-800 border-gray-600 text-gray-400 hover:bg-gray-700",
      accentIcon: "text-indigo-400"
    },
    cream: {
      bodyBg: "bg-amber-50",
      cardBg: "bg-yellow-50",
      cardBorder: "border-amber-200",
      textPrimary: "text-stone-900",
      textSecondary: "text-stone-700",
      textMuted: "text-stone-400",
      inputBg: "bg-amber-50/80",
      inputBorder: "border-amber-200",
      inputText: "text-stone-800",
      primary: "bg-amber-600 hover:bg-amber-500",
      textSimple: "text-amber-700",
      border: "border-amber-300",
      bgLight: "bg-amber-100/50",
      bgLightSolid: "bg-amber-100",
      ring: "focus:ring-amber-500 focus:border-amber-500",
      accentBadge: "bg-amber-100 border-amber-200 text-amber-800",
      progress: "bg-amber-600",
      dragActiveBorder: "border-amber-500 bg-amber-100/50",
      segmentBg: "bg-amber-100",
      segmentActive: "bg-amber-50 text-stone-900 shadow-xs border border-amber-300",
      segmentInactive: "text-stone-500 hover:text-stone-700",
      badgeFmt: "bg-amber-100 border border-amber-200 text-amber-800",
      badgeInactive: "bg-amber-50 border-amber-200 text-amber-700 hover:bg-amber-100",
      accentIcon: "text-amber-700"
    }
  };

  // Media State
  const [activeMediaType, setActiveMediaType] = useState<MediaType>("video");
  const [selectedFile, setSelectedFile] = useState<DemoFile | null>(DEMO_FILES[0]);
  const [dragActive, setDragActive] = useState(false);

  // Batch Queue & Checkpoint states
  const [filesQueue, setFilesQueue] = useState<DemoFile[]>([]);
  const [currentQueueIndex, setCurrentQueueIndex] = useState<number>(-1);
  const [checkpointIndex, setCheckpointIndex] = useState<number>(-1);
  const [isProcessingQueue, setIsProcessingQueue] = useState<boolean>(false);
  const [isPaused, setIsPaused] = useState<boolean>(false);

  // Telemetry, Privacy-First, and Nickname Generator (v6.0)
  const [telemetryConsentShow, setTelemetryConsentShow] = useState<boolean>(false);
  const [telemetryEnabled, setTelemetryEnabled] = useState<boolean>(false);
  const [userUuid, setUserUuid] = useState<string>("");
  const [userNickname, setUserNickname] = useState<string>("");
  const [isEditingNickname, setIsEditingNickname] = useState<boolean>(false);
  const [tempNickname, setTempNickname] = useState<string>("");
  const [nicknameCustomized, setNicknameCustomized] = useState<boolean>(false);

  // Safe Mode and GPU Hardware Acceleration options (v6.1 & v6.5)
  const [safeMode, setSafeMode] = useState<boolean>(false);
  const [gpuEncoderDetected, setGpuEncoderDetected] = useState<string>("Ninguno");
  const [hardwareAccelerationEnabled, setHardwareAccelerationEnabled] = useState<boolean>(true);

  // Community Global Stats from Database API
  const [globalStats, setGlobalStats] = useState<any>({
    totalEvents: 0,
    totalFiles: 0,
    totalBytesSaved: 0,
    uniqueUsers: 0
  });

  // Smart caching index records (v6.4)
  const [cachedOptimizations, setCachedOptimizations] = useState<Record<string, OptimizationResult>>({});

  // Nickname generation vocabulary (Petnames system)
  const NICKNAMES_ADJECTIVES = [
    "happy", "dashing", "swift", "clever", "brave", "silent", "creative", "active", "smart", "jolly",
    "bold", "wild", "bright", "proud", "kind", "lively", "fierce", "eager", "fancy", "cozy",
    "funky", "epic", "cool", "chill", "golden", "magic", "mystic", "noble", "quick", "rusty",
    "shady", "stellar", "tricky", "unique", "vast", "zesty", "agile", "calm", "dark", "elite",
    "grand", "heroic", "iconic", "jade", "keen", "lucky", "mighty", "neon", "retro", "ultra",
    "crimson", "azure", "solar", "lunar", "cosmic", "cyber", "rapid", "quiet", "merry", "gentle",
    "brazen", "sneaky", "sleepy", "wandering", "hidden", "flying", "jumping", "swimming", "lost",
    "famous", "hidden", "silly", "witty", "wise", "playful", "sunny", "stormy", "winter", "spring",
    "autumn", "summer", "arctic", "desert", "ocean", "jungle", "mountain", "valley", "river", "lake",
    "forest", "moonlight", "starlight", "sunlight", "twilight", "midnight", "dawn", "dusk", "morning",
    "evening", "day", "night", "light", "shadow", "ghost", "spirit", "soul", "heart", "mind"
  ];
  const NICKNAMES_NOUNS = [
    "tiger", "robot", "fox", "eagle", "panther", "coder", "falcon", "puffin", "koala", "badger",
    "wolf", "deer", "rabbit", "bear", "lion", "hawk", "owl", "dolphin", "whale", "squirrel",
    "shark", "dragon", "ninja", "wizard", "pirate", "ghost", "knight", "cyborg", "mutant", "alien",
    "phantom", "rebel", "sniper", "titan", "vampire", "zombie", "goblin", "orc", "troll", "elf",
    "dwarf", "giant", "mermaid", "yeti", "kraken", "sphinx", "phoenix", "unicorn", "pegasus", "griffin",
    "leopard", "cheetah", "jaguar", "cougar", "lynx", "bobcat", "puma", "ocelot", "caracal", "serval",
    "hound", "terrier", "mastiff", "bulldog", "collie", "poodle", "pug", "beagle", "boxer", "husky",
    "sparrow", "raven", "crow", "dove", "swan", "goose", "duck", "penguin", "ostrich", "emu",
    "turtle", "tortoise", "lizard", "snake", "crocodile", "alligator", "iguana", "gecko", "chameleon", "skink",
    "frog", "toad", "salamander", "newt", "axolotl", "fish", "shark", "ray", "eel", "crab"
  ];
  const generateRandomNickname = () => {
    const adj = NICKNAMES_ADJECTIVES[Math.floor(Math.random() * NICKNAMES_ADJECTIVES.length)];
    const noun = NICKNAMES_NOUNS[Math.floor(Math.random() * NICKNAMES_NOUNS.length)];
    return `${adj}-${noun}`;
  };

  // Helper: Get global metrics from database
  const fetchGlobalStats = async () => {
    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 5000);
      const response = await fetch("https://alenia-porter.onrender.com/telemetry/stats", { signal: ctrl.signal });
      clearTimeout(timer);
      if (response.ok) {
        const data = await response.json();
        if (data && data.stats) {
          const filesCount = (data.stats.audio || 0) + (data.stats.video || 0) + (data.stats.image || 0);
          setGlobalStats({
            totalEvents: filesCount,
            totalFiles: filesCount,
            totalBytesSaved: data.total_bytes_saved || 0,
            uniqueUsers: data.active_users || 0
          });
        }
      }
    } catch {
    }
  };

  // Load and initialize local parameters and preferences on mount
  useEffect(() => {
    const storedConsent = localStorage.getItem("alenia_telemetry_consent");
    const storedEnabled = localStorage.getItem("alenia_telemetry_enabled") === "true";
    const storedUuid = localStorage.getItem("alenia_user_uuid") || "";
    const storedNickname = localStorage.getItem("alenia_user_nickname") || "";
    const storedCustomized = localStorage.getItem("alenia_nickname_customized") === "true";
    const storedSafeMode = localStorage.getItem("alenia_safe_mode") === "true";
    const storedHwAcc = localStorage.getItem("alenia_hw_acc") !== "false";

    let finalUuid = storedUuid;
    let finalNickname = storedNickname;

    if (!storedUuid) {
      finalUuid = "ap-uuid-" + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      localStorage.setItem("alenia_user_uuid", finalUuid);
    }
    if (!storedNickname) {
      finalNickname = generateRandomNickname();
      localStorage.setItem("alenia_user_nickname", finalNickname);
    }

    setUserUuid(finalUuid);
    setUserNickname(finalNickname);
    setNicknameCustomized(storedCustomized);
    setSafeMode(storedSafeMode);
    setHardwareAccelerationEnabled(storedHwAcc);

    if (storedConsent === null) {
      setTelemetryConsentShow(true);
      setTelemetryEnabled(false); // Default disabled/silent until opt-in
    } else {
      setTelemetryEnabled(storedEnabled);
    }

    // Auto-detect a GPU encoder dynamically for simulation matching
    const encoders = ["NVIDIA NVENC (h264_nvenc)", "Intel QuickSync (h264_qsv)", "AMD AMF (h264_amf)"];
    const randomEncoder = encoders[Math.floor((finalUuid.charCodeAt(0) || 0) % encoders.length)];
    setGpuEncoderDetected(randomEncoder);

    fetchGlobalStats();
    const statsInterval = setInterval(fetchGlobalStats, 30000);
    return () => clearInterval(statsInterval);
  }, []);


  // Submit telemetry data helper
  const submitTelemetryEvent = async (fileType: string, fileCount: number, duration: number, savings: number) => {
    if (!telemetryEnabled) return; // Silent by default

    try {
      let osFamily = "Web Browser";
      if (navigator.userAgent.indexOf("Win") !== -1) osFamily = "Windows";
      else if (navigator.userAgent.indexOf("Mac") !== -1) osFamily = "macOS";
      else if (navigator.userAgent.indexOf("Linux") !== -1) osFamily = "Linux";

      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 5000);
      await fetch("https://alenia-porter.onrender.com/telemetry/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: ctrl.signal,
        body: JSON.stringify({
          uuid: userUuid,
          nickname: userNickname,
          os_family: osFamily,
          interface_type: "IDE",
          file_type: fileType,
          file_count: fileCount,
          duration_seconds: duration,
          savings_bytes: savings
        })
      });
      clearTimeout(timer);
      fetchGlobalStats();
    } catch {
    }
  };

  const [videoFormat, setVideoFormat] = useState("mp4");
  const [audioFormat, setAudioFormat] = useState("mp3");
  const [imageFormat, setImageFormat] = useState("jpg");

  const format = activeMediaType === "video" ? videoFormat : activeMediaType === "audio" ? audioFormat : imageFormat;
  const setFormat = (val: string) => {
    if (activeMediaType === "video") setVideoFormat(val);
    else if (activeMediaType === "audio") setAudioFormat(val);
    else setImageFormat(val);
  };

  const [codec, setCodec] = useState("libx264");
  const [quality, setQuality] = useState(28);
  const [audioBitrate, setAudioBitrate] = useState(128); // kbps
  const [scale, setScale] = useState("original");
  const [fps, setFps] = useState("original");
  const [preset, setPreset] = useState("medium");
  const [customArgsVideo, setCustomArgsVideo] = useState("");
  const [customArgsAudio, setCustomArgsAudio] = useState("");
  const [customArgsImage, setCustomArgsImage] = useState("");

  const customArgs = activeMediaType === "video" ? customArgsVideo : activeMediaType === "audio" ? customArgsAudio : customArgsImage;
  const setCustomArgs = (val: string) => {
    if (activeMediaType === "video") setCustomArgsVideo(val);
    else if (activeMediaType === "audio") setCustomArgsAudio(val);
    else setCustomArgsImage(val);
  };

  // FFmpeg Command Terminal State
  const [ffmpegCommand, setFfmpegCommand] = useState("");
  const [isManualEditing, setIsManualEditing] = useState(false);
  const [copiedCmd, setCopiedCmd] = useState(false);

  // Optimization Process Simulation State
  const [mascotState, setMascotState] = useState<"idle" | "thinking" | "success" | "error" | "winking">("idle");
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [terminalLogs, setTerminalLogs] = useState<TerminalLog[]>([]);
  const [optimizationHistory, setOptimizationHistory] = useState<OptimizationResult[]>([]);

  // Command Explainer state
  const [techExplanation, setTechExplanation] = useState<string | null>(null);
  const [isExplaining, setIsExplaining] = useState(false);
  const [showExamplesDropdown, setShowExamplesDropdown] = useState(false);

  // New Alenia Porter Custom States
  const [appVersion, setAppVersion] = useState("5.9");
  const [latestVersion, setLatestVersion] = useState("");
  const [updateAvailable, setUpdateAvailable] = useState(false);
  const [updateUrl, setUpdateUrl] = useState("https://github.com/Kaia-Alenia/Alenia-Porter");
  const [updateDownloadUrl, setUpdateDownloadUrl] = useState(""); // URL directa del binario
  const [showVersionModal, setShowVersionModal] = useState(false);
  const [isUpdatingVersion, setIsUpdatingVersion] = useState(false);
  const [updateProgress, setUpdateProgress] = useState(0);
  const [showSettings, setShowSettings] = useState(false);
  const [themeColor, setThemeColor] = useState<"white" | "blue" | "violet" | "slate" | "emerald" | "rose" | "dark" | "cream">("white");
  const [currentLang, setCurrentLang] = useState<string>(() => localStorage.getItem("alenia_lang") || "ES");
  const [showLangDropdown, setShowLangDropdown] = useState(false);

  useEffect(() => {
    localStorage.setItem("alenia_lang", currentLang);
  }, [currentLang]);

  const t = (key: string) => {
    return TRANSLATIONS[currentLang]?.[key] || TRANSLATIONS["US"]?.[key] || key;
  };

  // Registrar callbacks globales del updater (solo al montar)
  useEffect(() => {
    (window as any).updateReadyToRestart = () => {
      setUpdateProgress(100);
      setIsUpdatingVersion(false);
      setUpdateAvailable(false);
      setShowVersionModal(false);
      addLog("[Sistema] Alenia Porter actualizado exitosamente. Reiniciando...", "success");
      setMascotState("success");
    };
    (window as any).updateFailed = (errMsg?: string) => {
      setIsUpdatingVersion(false);
      setUpdateProgress(0);
      addLog(`[Error] Falló la actualización: ${errMsg || "Error desconocido"}`, "error");
    };
  }, []);

  // Verificar actualizaciones: primero via pywebview, fallback a fetch directo
  useEffect(() => {
    const isPyWebView = !!(window as any).pywebview;
    const checkUpdate = async () => {
      try {
        if (isPyWebView) {
          const result = await (window as any).pywebview.api.check_update();
          if (result && result.has_update) {
            setLatestVersion(result.new_ver || "");
            setUpdateAvailable(true);
            setUpdateDownloadUrl(result.dl_url || "");
            setUpdateUrl(result.dl_url || "https://github.com/Kaia-Alenia/Alenia-Porter");
          }
          return;
        }
      } catch (_) {}

      // Fallback: fetch directo para modo dev/web
      try {
        const response = await fetch("https://api.github.com/repos/Kaia-Alenia/Alenia-Porter/releases/latest");
        if (response.ok) {
          const data = await response.json();
          const tag = data.tag_name;
          const cleanTag = tag ? tag.replace(/^v/, "") : "";
          if (cleanTag && cleanTag !== appVersion) {
            setLatestVersion(cleanTag);
            setUpdateAvailable(true);
            setUpdateUrl(data.html_url || "https://github.com/Kaia-Alenia/Alenia-Porter");
          }
        }
      } catch (_) {}
    };
    checkUpdate();
  }, [appVersion]);

  const logsEndRef = useRef<HTMLDivElement>(null);

  // Generate FFmpeg command based on state values
  const generateCommandString = () => {
    let inputName = selectedFile ? selectedFile.name : "input.mp4";
    let outputName = `optimizado_${inputName.split(".")[0]}.${format}`;

    let cmd = `ffmpeg -i ${inputName}`;

    if (scale !== "original") {
      const [w, h] = scale.split("x");
      cmd += ` -vf scale=${w}:${h}`;
    }

    if (activeMediaType === "video") {
      const videoCodec = (hardwareAccelerationEnabled && !safeMode) ? "h264_nvenc" : codec;
      cmd += ` -c:v ${videoCodec}`;
      cmd += ` -crf ${quality}`;
      if (preset !== "medium") cmd += ` -preset ${preset}`;
      if (fps !== "original") cmd += ` -r ${fps}`;
      cmd += ` -c:a aac -b:a ${audioBitrate}k`;
    } else if (activeMediaType === "audio") {
      const audioCodec = format === "mp3" ? "libmp3lame" : format === "opus" ? "libopus" : "libvorbis";
      cmd += ` -c:a ${audioCodec} -b:a ${audioBitrate}k`;
    } else if (activeMediaType === "image") {
      if (format === "webp") {
        cmd += ` -c:v libwebp -quality ${quality}`;
      } else {
        cmd += ` -q:v ${Math.floor((100 - quality) / 10 + 1)}`;
      }
    }

    if (customArgs.trim()) cmd += ` ${customArgs.trim()}`;
    cmd += ` ${outputName}`;
    return cmd;
  };

  useEffect(() => {
    if (!isManualEditing) setFfmpegCommand(generateCommandString());
  }, [videoFormat, audioFormat, imageFormat, codec, quality, audioBitrate, scale, fps, preset, customArgs, selectedFile, activeMediaType, hardwareAccelerationEnabled, safeMode]);

  useEffect(() => {
    if (logsEndRef.current) logsEndRef.current.scrollIntoView({ behavior: "smooth" });
  }, [terminalLogs]);

  const parseManualCommand = (cmd: string) => {
    try {
      const outputParts = cmd.trim().split(" ");
      const lastArg = outputParts[outputParts.length - 1];
      if (lastArg && lastArg.includes(".")) {
        const ext = lastArg.split(".").pop()?.toLowerCase();
        if (ext && ["mp4", "webm", "gif", "ogg", "opus", "mp3", "wav", "jpg", "png", "webp"].includes(ext)) setFormat(ext);
      }
      const crfMatch = cmd.match(/-crf\s+(\d+)/);
      if (crfMatch) setQuality(parseInt(crfMatch[1]));
      const bitrateMatch = cmd.match(/(?:-b:a|-ab)\s+(\d+)/);
      if (bitrateMatch) setAudioBitrate(parseInt(bitrateMatch[1]));
      const codecMatch = cmd.match(/(?:-c:v|-vcodec)\s+([a-zA-Z0-9_]+)/);
      if (codecMatch) setCodec(codecMatch[1]);
      const scaleMatch = cmd.match(/scale=(\d+:\d+)/);
      if (scaleMatch) setScale(scaleMatch[1].replace(":", "x"));
      const rMatch = cmd.match(/-r\s+(\d+)/);
      if (rMatch) setFps(rMatch[1]);
      const presetMatch = cmd.match(/-preset\s+([a-zA-Z]+)/);
      if (presetMatch) setPreset(presetMatch[1]);
    } catch (e) {
      console.warn("Could not parse command", e);
    }
  };

  const handleManualCommandChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    setFfmpegCommand(val);
    setIsManualEditing(true);
    parseManualCommand(val);
  };

  const copyCommandToClipboard = () => {
    navigator.clipboard.writeText(ffmpegCommand);
    setCopiedCmd(true);
    setMascotState("winking");
    setTimeout(() => setCopiedCmd(false), 2000);
  };

  const calculateFileHash = (name: string, size: number) => {
    let hash = 0;
    const str = `${name}-${size}`;
    for (let i = 0; i < str.length; i++) {
      hash = (hash << 5) - hash + str.charCodeAt(i);
      hash |= 0;
    }
    return `sha256-${Math.abs(hash).toString(16)}`;
  };

  const appendFilesToQueue = (filesList: { name: string, size: number, type: MediaType, path?: string, isDirectory?: boolean }[]) => {
    const freshItems: DemoFile[] = filesList.map(item => ({
      id: `file-${Date.now()}-${Math.random().toString(36).substring(3, 8)}`,
      name: item.name,
      type: item.type,
      originalSize: item.size,
      src: "simulated-src",
      path: item.path || item.name,
      isDirectory: item.isDirectory || false,
      status: "pending",
      hash: calculateFileHash(item.name, item.size)
    }));

    setFilesQueue(prev => {
      const merged = [...prev, ...freshItems];
      if (prev.length === 0 && merged.length > 0) {
        setCurrentQueueIndex(0);
        setSelectedFile(merged[0]);
        setActiveMediaType(merged[0].type);
      }
      return merged;
    });

    addLog(`¡Se agregaron ${freshItems.length} archivos a la cola de optimización!`, "success");
    setMascotState("winking");
    setTimeout(() => setMascotState("idle"), 1500);
  };

  const appendFilesToQueueRef = React.useRef(appendFilesToQueue);
  React.useEffect(() => {
    appendFilesToQueueRef.current = appendFilesToQueue;
  });

  React.useEffect(() => {
    (window as any).handleNativeDropResolved = (resolvedFiles: any[]) => {
      try {
        console.log("[CHISMOSO FE] handleNativeDropResolved llamado con:", resolvedFiles);
        addLog("[CHISMOSO FE] handleNativeDropResolved recibido con " + (resolvedFiles ? resolvedFiles.length : 0) + " archivos", "info");
        const validFiles = (resolvedFiles || []).filter(r => !!r).map(r => ({
          name: r.name,
          size: r.size || 0,
          type: (r.mediaType || "video") as MediaType,
          path: r.path,
          isDirectory: r.isDirectory || false
        }));
        if (validFiles.length > 0) {
          appendFilesToQueueRef.current(validFiles);
        }
      } catch (err: any) {
        console.error("[CHISMOSO FE] Error en handleNativeDropResolved:", err);
        addLog("[CHISMOSO FE] Error procesando drop nativo: " + err.message, "error");
      }
    };

    const preventDefault = (e: DragEvent) => {
      e.preventDefault();
    };
    window.addEventListener("dragover", preventDefault, false);
    window.addEventListener("drop", preventDefault, false);

    return () => {
      delete (window as any).handleNativeDropResolved;
      window.removeEventListener("dragover", preventDefault, false);
      window.removeEventListener("drop", preventDefault, false);
    };
  }, []);

  // ─── Drag & Drop ───────────────────────────────────────────────────────────
  const dragCounterRef = React.useRef(0);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    console.log("[CHISMOSO FE] handleDrag:", e.type);
    if (e.type === "dragenter") {
      dragCounterRef.current += 1;
      setDragActive(true);
    } else if (e.type === "dragleave") {
      dragCounterRef.current -= 1;
      if (dragCounterRef.current <= 0) {
        dragCounterRef.current = 0;
        setDragActive(false);
      }
    } else if (e.type === "dragover") {
      if (!dragActive) setDragActive(true);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    dragCounterRef.current = 0;
    setDragActive(false);
    console.log("[CHISMOSO FE] handleDrop DOM React disparado");
    addLog("[CHISMOSO FE] Soltado en DOM (React)", "info");

    const pendingFiles: { name: string; size: number; type: MediaType; path?: string; isDirectory?: boolean }[] = [];
    const isPyWebView = !!(window as any).pywebview;

    if (isPyWebView) {
      const rawPaths: string[] = [];

      if (e.dataTransfer?.files?.length > 0) {
        for (let i = 0; i < e.dataTransfer.files.length; i++) {
          const f = e.dataTransfer.files[i] as any;
          const fullPath = f.pywebviewFullPath || f.path;
          if (fullPath && fullPath.length > 0) {
            rawPaths.push(fullPath);
          }
        }
      }

      if (rawPaths.length === 0 && e.dataTransfer?.items?.length > 0) {
        for (let i = 0; i < e.dataTransfer.items.length; i++) {
          const item = e.dataTransfer.items[i];
          if (item.kind === "file") {
            const f = item.getAsFile() as any;
            const fullPath = f?.pywebviewFullPath || f?.path;
            if (fullPath && fullPath.length > 0) rawPaths.push(fullPath);
          }
        }
      }

      if (rawPaths.length === 0) {
        const uriList =
          e.dataTransfer?.getData("text/uri-list") ||
          e.dataTransfer?.getData("text/plain") ||
          "";
        uriList
          .split(/\r?\n/)
          .map((u) => u.trim())
          .filter((u) => u.length > 0 && !u.startsWith("#"))
          .forEach((u) => rawPaths.push(u));
      }

      console.log("[CHISMOSO FE] rawPaths extraidos en JS:", rawPaths);
      addLog("[CHISMOSO FE] rawPaths extraidos en JS: " + rawPaths.length, "info");

      if (rawPaths.length === 0) {
        console.log("[CHISMOSO FE] rawPaths vacios, esperando handler DOM de pywebview");
        addLog("[CHISMOSO FE] Esperando handler DOM de pywebview...", "info");
        return;
      }

      try {
        const resolved: any[] = await (window as any).pywebview.api.resolve_dropped_paths(rawPaths);
        if (resolved && resolved.length > 0) {
          for (const r of resolved) {
            if (!r) continue;
            if (r.isDirectory) {
              if ((r.mediaCount || 0) > 0) {
                addLog(`📁 ${r.name}: ${r.audio} audio, ${r.video} video, ${r.image} img`, "info");
                pendingFiles.push({ name: r.name, size: r.size || 0, type: activeMediaType, path: r.path, isDirectory: true });
              } else {
                addLog(`⚠ Sin archivos compatibles en: ${r.name}`, "error");
              }
            } else {
              pendingFiles.push({ name: r.name, size: r.size || 0, type: r.mediaType as MediaType, path: r.path, isDirectory: false });
            }
          }
          if (pendingFiles.length > 0) {
            appendFilesToQueue(pendingFiles);
          }
        } else {
          addLog("No se detectaron archivos de medios compatibles.", "error");
          setMascotState("error");
        }
      } catch (err) {
        addLog(`Error: ${err}`, "error");
      }
    } else {
      // ── Navegador web estándar: usar webkitGetAsEntry para soporte de carpetas ──
      const videoExts = ["mp4", "webm", "avi", "mkv", "mov", "3gp", "flv", "mpeg", "m4v", "wmv", "ts", "m2ts", "divx", "ogv"];
      const audioExts = ["ogg", "opus", "mp3", "wav", "flac", "aac", "amr", "wma", "m4a", "alac", "aiff", "aif", "ra", "rm"];
      const imageExts = ["webp", "jpg", "jpeg", "png", "gif", "bmp", "ico", "tiff", "tga", "pdf", "avif", "apng"];

      const detectType = (name: string, mime?: string): MediaType | null => {
        const ext = name.split(".").pop()?.toLowerCase() || "";
        if (mime?.startsWith("image/") || imageExts.includes(ext)) return "image";
        if (mime?.startsWith("video/") || videoExts.includes(ext)) return "video";
        if (mime?.startsWith("audio/") || audioExts.includes(ext)) return "audio";
        return null;
      };

      const traverseEntry = async (entry: any): Promise<void> => {
        if (entry.isFile) {
          const file: File = await new Promise((res, rej) => entry.file(res, rej));
          const mType = detectType(file.name, file.type);
          if (mType) pendingFiles.push({ name: file.name, size: file.size, type: mType });
        } else if (entry.isDirectory) {
          const reader = entry.createReader();
          const readAll = (): Promise<any[]> =>
            new Promise((res) => {
              const all: any[] = [];
              const loop = () =>
                reader.readEntries((batch: any[]) => {
                  if (!batch.length) { res(all); return; }
                  all.push(...batch);
                  loop();
                }, () => res(all));
              loop();
            });
          const children = await readAll();
          await Promise.all(children.map(traverseEntry));
        }
      };

      if (e.dataTransfer?.items?.length > 0) {
        const promises: Promise<void>[] = [];
        for (let i = 0; i < e.dataTransfer.items.length; i++) {
          if (e.dataTransfer.items[i].kind === "file") {
            const entry = e.dataTransfer.items[i].webkitGetAsEntry?.();
            if (entry) promises.push(traverseEntry(entry));
          }
        }
        await Promise.all(promises);
      }

      if (pendingFiles.length === 0 && e.dataTransfer?.files?.length > 0) {
        for (let i = 0; i < e.dataTransfer.files.length; i++) {
          const file = e.dataTransfer.files[i];
          const mType = detectType(file.name, file.type);
          if (mType) pendingFiles.push({ name: file.name, size: file.size, type: mType });
        }
      }
    }

    if (pendingFiles.length > 0) {
      appendFilesToQueue(pendingFiles);
    } else {
      addLog(t("errorNoFiles") || "Ningún archivo compatible (Video/Audio/Imagen) fue detectado.", "error");
      setMascotState("error");
    }
  };


  const handleManualFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const pendingFiles: { name: string, size: number, type: MediaType }[] = [];
      const files = e.target.files;
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const extension = file.name.split('.').pop()?.toLowerCase() || '';

        const videoExts = ["mp4", "webm", "avi", "mkv", "mov", "3gp", "flv", "mpeg"];
        const audioExts = ["ogg", "opus", "mp3", "wav", "flac", "aac", "amr", "wma"];
        const imageExts = ["webp", "jpg", "jpeg", "png", "gif", "bmp", "ico", "tiff", "avif", "apng"];

        let mType: MediaType | null = null;
        if (file.type.startsWith("image/") || imageExts.includes(extension)) {
          mType = "image";
        } else if (file.type.startsWith("video/") || videoExts.includes(extension)) {
          mType = "video";
        } else if (file.type.startsWith("audio/") || audioExts.includes(extension)) {
          mType = "audio";
        }

        if (mType) {
          pendingFiles.push({ name: file.name, size: file.size, type: mType });
        }
      }

      if (pendingFiles.length > 0) {
        appendFilesToQueue(pendingFiles);
      } else {
        addLog("Ningún archivo compatible con los formatos de Alenia Porter.", "error");
      }
    }
  };

  // Helper formatting size bytes
  const formatBytes = (bytes: number, decimals = 2) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ["Bytes", "KB", "MB", "GB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + " " + sizes[i];
  };

  // Add terminal trace logs
  const addLog = (text: string, type: "info" | "stdout" | "stderr" | "success" | "error" = "stdout") => {
    const timestamp = new Date().toLocaleTimeString();
    setTerminalLogs((prev) => {
      // Rotating Logs: Keep up to 80 logs to save memory!
      const nextLogs = [...prev, { id: `${Date.now()}-${Math.random()}`, timestamp, text, type }];
      if (nextLogs.length > 80) return nextLogs.slice(nextLogs.length - 80);
      return nextLogs;
    });
  };

  // Calculate simulated sizes based on parameters selected
  const getSimulatedSizes = () => {
    if (!selectedFile) return { original: "0 MB", compressed: "0 MB", bytesOriginal: 0, bytesCompressed: 0, savings: 0 };

    const orig = selectedFile.originalSize;
    let factor = 1.0;

    // Quality factor logic
    if (activeMediaType === "video") {
      const crfNormal = Math.max(0, (quality - 18) / 33); // 0 to 1
      factor = 1.0 - (crfNormal * 0.85); // up to 85% reduction based on crf

      if (codec === "libvpx-vp9" || codec === "libx265") factor *= 0.75;

      if (scale === "1280x720") factor *= 0.5;
      if (scale === "854x480") factor *= 0.25;

      if (fps === "24") factor *= 0.85;
      if (fps === "30") factor *= 0.9;
    } else if (activeMediaType === "audio") {
      factor = audioBitrate / 320;
      if (format === "opus") factor *= 0.8; // Opus efficiency
    } else if (activeMediaType === "image") {
      factor = (quality / 100) * 0.9;
      if (format === "webp") factor *= 0.65; // WebP efficiency
    }

    // Keep it realistic
    factor = Math.max(0.04, Math.min(0.98, factor));
    const compBytes = Math.round(orig * factor);
    const savings = Math.round(((orig - compBytes) / orig) * 100);

    return {
      original: formatBytes(orig),
      compressed: formatBytes(compBytes),
      bytesOriginal: orig,
      bytesCompressed: compBytes,
      savings
    };
  };

  // Get simulated sizes for any custom file
  const getSimulatedSizesForFile = (file: DemoFile) => {
    const orig = file.originalSize;
    let factor = 1.0;

    if (file.type === "video") {
      const crfNormal = Math.max(0, (quality - 18) / 33);
      factor = 1.0 - (crfNormal * 0.85);
      if (codec === "libvpx-vp9" || codec === "libx265") factor *= 0.75;
      if (scale === "1280x720") factor *= 0.5;
      if (scale === "854x480") factor *= 0.25;
    } else if (file.type === "audio") {
      factor = audioBitrate / 320;
      if (format === "opus") factor *= 0.8;
    } else if (file.type === "image") {
      factor = (quality / 100) * 0.9;
      if (format === "webp") factor *= 0.65;
    }

    factor = Math.max(0.04, Math.min(0.98, factor));
    const compBytes = Math.round(orig * factor);
    const savings = Math.round(((orig - compBytes) / orig) * 100);

    return {
      original: formatBytes(orig),
      compressed: formatBytes(compBytes),
      bytesOriginal: orig,
      bytesCompressed: compBytes,
      savings
    };
  };

  const simulationMetrics = getSimulatedSizes();

  // Explain manual FFmpeg commands using the local python engine
  const handleExplainCommand = async () => {
    if (!ffmpegCommand) return;
    setIsExplaining(true);
    setTechExplanation(null);
    setMascotState("thinking");

    try {
      const pywebview = (window as any).pywebview;
      if (pywebview && pywebview.api && pywebview.api.explain_command) {
        const explanation = await pywebview.api.explain_command(ffmpegCommand);
        setTechExplanation(explanation);
        setMascotState("winking");
        addLog("Explicación de comando generada por el analizador local", "success");
      } else {
        throw new Error("El analizador local de Python no está conectado.");
      }
    } catch (err: any) {
      console.error(err);
      addLog(`Error al explicar comando: ${err.message}`, "error");
      setMascotState("error");
    } finally {
      setIsExplaining(false);
    }
  };

  // Crash report generator in case of forced errors (v6.1)
  const generateCrashDump = () => {
    const dump = `=====================================================
ALENIA PORTER CRASH DUMP REPORT - v${appVersion}
=====================================================
Timestamp: ${new Date().toISOString()}
UUID: ${userUuid}
Nickname: ${userNickname}
Safe Mode: ${safeMode ? "ENABLED" : "DISABLED"}
Hardware Acceleration: ${hardwareAccelerationEnabled ? "ENABLED" : "DISABLED"}
GPU Encoder Detected: ${gpuEncoderDetected}

ACTIVE MEDIA TYPE: ${activeMediaType}
SELECTED FORMAT: ${format}
CODEC USED: ${codec}
FFMPEG COMMAND EXECUTED:
"${ffmpegCommand}"

ERROR CONTEXT:
[FFmpeg-WASM] Thread allocation failed. Driver signature mismatch or GPU memory overflow.
[FFmpeg-WASM] Reverting from acceleration API to soft fallback failed.
[FFmpeg-WASM] Signal 11 (SIGSEGV) encountered in ffmpeg_exec_core().

SUGGESTION:
Enable 'Modo Seguro (Safe Mode)' in Alenia Porter settings to force standard CPU encoding and bypass hardware acceleration drivers.
=====================================================`;
    
    const blob = new Blob([dump], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `alenia_crash_dump_${Date.now()}.txt`;
    link.click();
    URL.revokeObjectURL(url);
    addLog("Archivo alenia_crash_dump.txt descargado para soporte de la comunidad.", "info");
  };

  // Batch queue processing interval reference
  const processingIntervalRef = useRef<any>(null);

  // Start sequential batch processing with smart cache and checkpointing
  const startBatchQueueProcessing = () => {
    if (filesQueue.length === 0) {
      // If queue is empty, load a dummy file representation
      if (selectedFile) {
        setFilesQueue([selectedFile]);
        setTimeout(() => startBatchQueueIndex(0), 100);
      }
      return;
    }
    
    setIsProcessingQueue(true);
    setIsPaused(false);
    setMascotState("thinking");
    addLog(`[Alenia Batch] Iniciando procesamiento por lotes de ${filesQueue.length} archivo(s).`, "info");

    const resumeIdx = filesQueue.findIndex(f => f.status !== "completed");
    const activeIdx = resumeIdx === -1 ? 0 : resumeIdx;

    startBatchQueueIndex(activeIdx);
  };

  // Pause batch processing and save checkpoint (Section C of roadmap)
  const pauseBatchQueueProcessing = () => {
    setIsPaused(true);
    setIsProcessingQueue(false);
    setIsProcessing(false);
    setMascotState("idle");
    if (processingIntervalRef.current) {
      clearInterval(processingIntervalRef.current);
    }

    addLog(`[Alenia Batch] Procesamiento pausado. Punto de control guardado en archivo #${currentQueueIndex + 1}.`, "info");
    
    setFilesQueue(prev => {
      const updated = [...prev];
      if (updated[currentQueueIndex] && updated[currentQueueIndex].status === "processing") {
        updated[currentQueueIndex].status = "pending";
      }
      return updated;
    });
  };

  // Clean queue list completely
  const clearBatchQueue = () => {
    setFilesQueue([]);
    setCurrentQueueIndex(-1);
    setCheckpointIndex(-1);
    setIsProcessingQueue(false);
    setIsPaused(false);
    setSelectedFile(null);
    if (processingIntervalRef.current) {
      clearInterval(processingIntervalRef.current);
    }
    addLog("Cola de procesamiento vaciada.", "info");
  };

  const startBatchQueueIndex = (index: number) => {
    if (index >= filesQueue.length) {
      setIsProcessingQueue(false);
      setIsProcessing(false);
      setProgress(100);
      setMascotState("success");
      addLog(`[Alenia Batch] ¡Todos los archivos procesados exitosamente!`, "success");
      return;
    }

    const file = filesQueue[index];
    setSelectedFile(file);
    setActiveMediaType(file.type);
    setCurrentQueueIndex(index);
    setCheckpointIndex(index);

    setFilesQueue(prev => {
      const updated = [...prev];
      updated[index].status = "processing";
      return updated;
    });

    setProgress(0);
    setIsProcessing(true);
    addLog(`[Alenia FFmpeg] Optimizando archivo (${index + 1}/${filesQueue.length}): ${file.path || file.name}`, "info");

    const targetFormat = file.type === "video" ? videoFormat : file.type === "audio" ? audioFormat : imageFormat;
    const cacheKey = file.hash ? `${file.hash}-${targetFormat}` : "";

    // Smart-Caching fingerprint matching check! (Phase 6 / v6.4)
    if (cacheKey && cachedOptimizations[cacheKey] && !(window as any).pywebview) {
      const hit = cachedOptimizations[cacheKey];
      addLog(`[Smart-Cache] ¡Coincidencia de huella digital MD5/SHA en el caché local!`, "success");
      addLog(`[Smart-Cache] Omitiendo compilación redundante para: ${file.name}`, "success");
      
      setProgress(100);
      setFilesQueue(prev => {
        const updated = [...prev];
        updated[index].status = "completed";
        return updated;
      });

      // Insert hit in local logs immediately
      const cachedHistoryItem: OptimizationResult = {
        fileName: file.name,
        mediaType: file.type,
        originalSize: file.originalSize,
        compressedSize: hit.compressedSize,
        savingsPercent: hit.savingsPercent,
        format: hit.format,
        commandUsed: ffmpegCommand,
        timestamp: new Date().toLocaleTimeString() + " (Cache Hit)"
      };
      setOptimizationHistory(prev => [cachedHistoryItem, ...prev]);

      setTimeout(() => {
        startBatchQueueIndex(index + 1);
      }, 700);
      return;
    }

    const isGpuActive = hardwareAccelerationEnabled && !safeMode;
    const processStepSpeed = isGpuActive ? 15 : 6; // GPU provides accelerated conversion!
    
    addLog(isGpuActive ? `[FFmpeg-WASM] GPU Activo: ${gpuEncoderDetected}` : `[FFmpeg-WASM] Usando codificación soft (Drivers inactivos / Safe Mode)`, "info");

    let currentPercent = 0;
    const totalFrames = file.type === "video" ? 360 : 100;
    const itemMetrics = getSimulatedSizesForFile(file);

      if ((window as any).pywebview) {
        const filePath = file.path && file.path !== file.name ? file.path : (file.path || null);
        const isDir = file.isDirectory || false;

        if (!isDir && !filePath) {
          addLog(`Error: ruta de archivo no disponible para "${file.name}" — usa el selector de archivos nativo.`, "error");
          setMascotState("error");
          return;
        }

        const params = {
          inputDirectory: isDir ? filePath : null,
          input: !isDir && filePath ? filePath : null,
          files: !isDir && filePath ? [filePath] : [],
          mediaType: file.type,
          videoFormat: videoFormat || "mp4",
          audioFormat: audioFormat || "mp3",
          imageFormat: imageFormat || "jpg",
          format: file.type === "video" ? videoFormat : file.type === "audio" ? audioFormat : imageFormat,
          quality: quality,
          preset: preset,
          audioBitrate: audioBitrate,
          recursive: true,
          customArgs: customArgs || ""
        };

        if (isDir) {
          addLog(`[Alenia Porter] Modo carpeta: convirtiendo video→${videoFormat}, audio→${audioFormat}, imagen→${imageFormat}`, "info");
        }

        (window as any).updateProgress = (p: number) => {
          setProgress(p);
        };
        (window as any).conversionComplete = (success: boolean, finalOrigSize?: number, finalCompressedSize?: number, outDir?: string) => {
          if(success) {
            setProgress(100);
            setFilesQueue(prev => {
              const updated = [...prev];
              if(updated[index]) updated[index].status = "completed";
              return updated;
            });
            addLog(`✓ Conversión completada.`, "success");
            if (outDir) {
              addLog(`📁 Archivos guardados en: ${outDir}`, "success");
            }

            const origSizeToUse = finalOrigSize || file.originalSize || 0;
            const compSizeToUse = finalCompressedSize || 0;
            const savings = origSizeToUse > 0 && compSizeToUse > 0
                ? Math.max(0, Math.round(((origSizeToUse - compSizeToUse) / origSizeToUse) * 100))
                : 0;

            const cachedHistoryItem: OptimizationResult = {
              fileName: file.name || "Carpeta",
              mediaType: file.type,
              originalSize: origSizeToUse,
              compressedSize: compSizeToUse,
              savingsPercent: savings,
              format: isDir ? `vid:${videoFormat} aud:${audioFormat} img:${imageFormat}` : (file.type === "video" ? videoFormat : file.type === "audio" ? audioFormat : imageFormat),
              commandUsed: "Nativo",
              timestamp: new Date().toLocaleTimeString()
            };
            setOptimizationHistory(prev => [cachedHistoryItem, ...prev]);

            submitTelemetryEvent(
              isDir ? "folder" : file.type,
              1,
              Math.round((Date.now() - (file as any)._startTime || 0) / 1000) || 1,
              Math.max(0, origSizeToUse - compSizeToUse)
            );

            setTimeout(() => {
              startBatchQueueIndex(index + 1);
            }, 1000);
          } else {
            addLog(`Error en conversión`, "error");
            setMascotState("error");
          }
        };

        (window as any).pywebview.api.start_conversion(params);
        return;
      }

      // Fallback for web simulation
      const interval = setInterval(() => {
        currentPercent += Math.floor(Math.random() * processStepSpeed) + 3;
        if (currentPercent >= 100) {
          currentPercent = 100;
          clearInterval(interval);

          // Complete item in queue
          setFilesQueue(prev => {
            const updated = [...prev];
            updated[index].status = "completed";
            return updated;
          });

        // Save in cache
        const completedResult: OptimizationResult = {
          fileName: file.name,
          mediaType: file.type,
          originalSize: file.originalSize,
          compressedSize: itemMetrics.bytesCompressed,
          savingsPercent: itemMetrics.savings,
          format: file.type === "video" ? videoFormat : file.type === "audio" ? audioFormat : imageFormat,
          commandUsed: ffmpegCommand,
          timestamp: new Date().toLocaleTimeString()
        };
        const cKey = file.hash ? `${file.hash}-${completedResult.format}` : "";
        if (cKey) {
          setCachedOptimizations(prev => ({
            ...prev,
            [cKey]: completedResult
          }));
        }

        // Log to database server via API proxy
        submitTelemetryEvent(file.type, 1, 1.2, itemMetrics.bytesOriginal - itemMetrics.bytesCompressed);

        // Add to history
        setOptimizationHistory(prev => [completedResult, ...prev]);

        addLog(`[FFmpeg-WASM] Frame= ${totalFrames} (FPS: ${isGpuActive ? "142" : "54"}) Quality: OK.`, "stdout");
        addLog(`[FFmpeg-WASM] Write output file successful.`, "success");
        addLog(`¡Optimización finalizada! Se comprimió un ${itemMetrics.savings}% del archivo original.`, "success");

        // Advance sequentially
        setTimeout(() => {
          startBatchQueueIndex(index + 1);
        }, 800);

      } else {
        setProgress(currentPercent);

        // Feed metrics to CLI/Terminal outputs
        if (file.type === "video") {
          const frameNum = Math.floor((currentPercent / 100) * totalFrames);
          const currentSizeKB = Math.round(((currentPercent / 100) * itemMetrics.bytesCompressed) / 1024);
          addLog(
            `frame=  ${frameNum} fps=${isGpuActive ? "145" : "48"} q=${quality}.0 size=   ${currentSizeKB}kB time=00:00:12.10 bitrate=${audioBitrate}.0kbits/s speed=${isGpuActive ? "4.5x" : "1.8x"}`,
            "stdout"
          );
        } else if (file.type === "audio") {
          const currentSizeKB = ((currentPercent / 100) * itemMetrics.bytesCompressed) / 1024;
          addLog(
            `size= ${Math.round(currentSizeKB)}kB time=00:01:22.40 bitrate=${audioBitrate}kbits/s speed=${isGpuActive ? "84.2x" : "32.4x"}`,
            "stdout"
          );
        } else {
          addLog(`compressing image array... block row ${Math.floor(currentPercent)}% done`, "stdout");
        }
      }
    }, 150);

    processingIntervalRef.current = interval;
  };

  // Run a single optimization process simulation
  const handleRunOptimization = () => {
    if (!selectedFile) return;

    setProgress(0);
    setTerminalLogs([]);
    setMascotState("thinking");

    addLog(t("initLog"), "info");
    addLog(`${t("sourceFile")}${selectedFile.name}`, "info");
    addLog(`${t("commandLog")}${ffmpegCommand}`, "info");

    if (filesQueue.length > 1) {
      startBatchQueueProcessing();
      return;
    }

    setIsProcessing(true);
    addLog(`[FFmpeg-WASM] Loading shared-libs... Done.`, "stdout");
    addLog(`[FFmpeg-WASM] Mapping filesystem files... Done.`, "stdout");

    if ((window as any).pywebview) {
      const filePath = selectedFile.path && selectedFile.path !== selectedFile.name ? selectedFile.path : (selectedFile.path || null);
      const isDir = (selectedFile as any).isDirectory || false;

      if (!isDir && !filePath) {
        addLog(`Error: ruta de archivo no disponible para "${selectedFile.name}" — usa el selector de archivos nativo.`, "error");
        setIsProcessing(false);
        setMascotState("error");
        return;
      }

      const params = {
        inputDirectory: isDir ? filePath : null,
        input: !isDir && filePath ? filePath : null,
        files: !isDir && filePath ? [filePath] : [],
        mediaType: selectedFile.type,
        videoFormat: videoFormat || "mp4",
        audioFormat: audioFormat || "mp3",
        imageFormat: imageFormat || "jpg",
        format: selectedFile.type === "video" ? videoFormat : selectedFile.type === "audio" ? audioFormat : imageFormat,
        quality: quality,
        preset: preset,
        audioBitrate: audioBitrate,
        recursive: true,
        customArgs: customArgs || ""
      };

      if (isDir) {
        addLog(`[Alenia Porter] Modo carpeta: convirtiendo video→${videoFormat}, audio→${audioFormat}, imagen→${imageFormat}`, "info");
      }

      (window as any).updateProgress = (p: number) => {
        setProgress(p);
      };
      (window as any).conversionComplete = (success: boolean, finalOrigSize?: number, finalCompressedSize?: number, outDir?: string) => {
        setIsProcessing(false);
        if (success) {
          setProgress(100);
          setMascotState("success");
          addLog(`✓ Conversión completada.`, "success");
          if (outDir) {
            addLog(`📁 Archivos guardados en: ${outDir}`, "success");
          }

          const origSizeToUse = finalOrigSize || selectedFile.originalSize || 0;
          const compSizeToUse = finalCompressedSize || 0;
          const savings = origSizeToUse > 0 && compSizeToUse > 0
            ? Math.max(0, Math.round(((origSizeToUse - compSizeToUse) / origSizeToUse) * 100))
            : 0;

          const completedResult: OptimizationResult = {
            fileName: selectedFile.name || "Carpeta",
            mediaType: selectedFile.type,
            originalSize: origSizeToUse,
            compressedSize: compSizeToUse,
            savingsPercent: savings,
            format: isDir ? `vid:${videoFormat} aud:${audioFormat} img:${imageFormat}` : (selectedFile.type === "video" ? videoFormat : selectedFile.type === "audio" ? audioFormat : imageFormat),
            commandUsed: "Nativo",
            timestamp: new Date().toLocaleTimeString()
          };
          setOptimizationHistory(prev => [completedResult, ...prev]);
          submitTelemetryEvent(isDir ? "folder" : selectedFile.type, 1, 1, Math.max(0, origSizeToUse - compSizeToUse));
        } else {
          setMascotState("error");
          addLog(`Error en conversión.`, "error");
        }
      };

      (window as any).pywebview.api.start_conversion(params);
      return;
    }

    const targetFormat = selectedFile.type === "video" ? videoFormat : selectedFile.type === "audio" ? audioFormat : imageFormat;
    const cacheKey = selectedFile.hash ? `${selectedFile.hash}-${targetFormat}` : "";
    
    if (cacheKey && cachedOptimizations[cacheKey]) {
      const hit = cachedOptimizations[cacheKey];
      addLog(t("cacheMatch"), "success");
      addLog(`${t("cacheSkip")}${selectedFile.name}`, "success");
      
      setProgress(100);
      setIsProcessing(false);
      setMascotState("success");

      const cachedHistoryItem: OptimizationResult = {
        fileName: selectedFile.name,
        mediaType: activeMediaType,
        originalSize: selectedFile.originalSize,
        compressedSize: hit.compressedSize,
        savingsPercent: hit.savingsPercent,
        format: hit.format,
        commandUsed: ffmpegCommand,
        timestamp: new Date().toLocaleTimeString() + " (Cache Hit)"
      };
      setOptimizationHistory(prev => [cachedHistoryItem, ...prev]);
      return;
    }

    const isGpuActive = hardwareAccelerationEnabled && !safeMode;
    const processStepSpeed = isGpuActive ? 15 : 6;

    addLog(isGpuActive ? `[FFmpeg-WASM] GPU Activo: ${gpuEncoderDetected}` : `[FFmpeg-WASM] Usando codificación soft (Drivers inactivos / Safe Mode)`, "info");

    let currentPercent = 0;
    const totalFrames = activeMediaType === "video" ? 360 : 100;

    const interval = setInterval(() => {
      currentPercent += Math.floor(Math.random() * processStepSpeed) + 3;
      if (currentPercent >= 100) {
        currentPercent = 100;
        clearInterval(interval);

        setIsProcessing(false);
        setProgress(100);
        setMascotState("success");

        const completedResult: OptimizationResult = {
          fileName: selectedFile.name,
          mediaType: activeMediaType,
          originalSize: simulationMetrics.bytesOriginal,
          compressedSize: simulationMetrics.bytesCompressed,
          savingsPercent: simulationMetrics.savings,
          format,
          commandUsed: ffmpegCommand,
          timestamp: new Date().toLocaleTimeString()
        };
        const cKey = selectedFile.hash ? `${selectedFile.hash}-${format}` : "";
        if (cKey) {
          setCachedOptimizations(prev => ({
            ...prev,
            [cKey]: completedResult
          }));
        }

        submitTelemetryEvent(activeMediaType, 1, 1.2, simulationMetrics.bytesOriginal - simulationMetrics.bytesCompressed);
        setOptimizationHistory(prev => [completedResult, ...prev]);

        addLog(`[FFmpeg-WASM] Frame= ${totalFrames} (FPS: ${isGpuActive ? "142" : "54"}) Quality: OK.`, "stdout");
        addLog(`[FFmpeg-WASM] Write output file successful.`, "success");
        addLog(t("optimizationSuccess").replace("{savings}", String(simulationMetrics.savings)), "success");

      } else {
        setProgress(currentPercent);

        if (activeMediaType === "video") {
          const frameNum = Math.floor((currentPercent / 100) * totalFrames);
          const currentSizeKB = Math.round(((currentPercent / 100) * simulationMetrics.bytesCompressed) / 1024);
          addLog(
            `frame=  ${frameNum} fps=${isGpuActive ? "145" : "48"} q=${quality}.0 size=   ${currentSizeKB}kB time=00:00:12.10 bitrate=${audioBitrate}.0kbits/s speed=${isGpuActive ? "4.5x" : "1.8x"}`,
            "stdout"
          );
        } else if (activeMediaType === "audio") {
          const currentSizeKB = ((currentPercent / 100) * simulationMetrics.bytesCompressed) / 1024;
          addLog(
            `size= ${Math.round(currentSizeKB)}kB time=00:01:22.40 bitrate=${audioBitrate}kbits/s speed=${isGpuActive ? "84.2x" : "32.4x"}`,
            "stdout"
          );
        } else {
          addLog(`compressing image array... block row ${Math.floor(currentPercent)}% done`, "stdout");
        }
      }
    }, 150);

    processingIntervalRef.current = interval;
  };

  // Callback to load proposed command settings
  const handleApplyCommand = (cmd: string, recFormat: string, recQuality?: number, recBitrate?: number) => {
    setFfmpegCommand(cmd);
    setFormat(recFormat);
    if (recQuality) setQuality(recQuality);
    if (recBitrate) setAudioBitrate(recBitrate);
    setIsManualEditing(true);

    addLog(`Comando cargado exitosamente. Sincronizando interfaz.`, "success");
    setMascotState("winking");
    setTimeout(() => setMascotState("idle"), 1500);
  };

  // Helper formatting file type icons
  const renderMediaTypeIcon = (type: MediaType, size = 18) => {
    switch (type) {
      case "video":
        return <FileVideo size={size} className="text-blue-550" />;
      case "audio":
        return <FileAudio size={size} className="text-blue-550" />;
      case "image":
        return <FileImage size={size} className="text-blue-550" />;
    }
  };

  return (
    <div className="h-screen w-screen font-sans select-none flex flex-col">
      {/* ANDROID VIEWPORT CONTAINER */}
      <div className={`relative w-full h-screen ${THEME_COLORS[themeColor].bodyBg} overflow-hidden flex flex-col transition-all duration-300`}>
        
        {/* Dynamic App Content Body (Scrollable) */}
        <div className={`flex-1 overflow-y-auto px-4 py-4 space-y-4 ${THEME_COLORS[themeColor].bodyBg} relative pb-16 transition-all duration-300`}>
          
          {/* App Header with Brand Logo & Mascot */}
          <div className={`flex items-center justify-between ${THEME_COLORS[themeColor].cardBg} backdrop-blur-md border ${THEME_COLORS[themeColor].cardBorder} p-3 py-2.5 rounded-2xl shadow-xs transition-colors duration-300`}>
            <div className="flex items-center gap-1.5">
              <div className="flex flex-col">
                <span className={`font-display font-extrabold text-sm tracking-tight ${THEME_COLORS[themeColor].textPrimary} uppercase`}>
                  {t("title")}
                </span>
              </div>
            </div>
            <div className="flex items-center gap-1.5">
              {/* Version indicator and update alarm */}
              <button
                type="button"
                onClick={() => setShowVersionModal(true)}
                className={`inline-flex items-center gap-1.5 text-[10px] px-2 py-0.5 rounded-full border transition-all cursor-pointer font-bold ${
                  updateAvailable
                    ? "bg-amber-50 border-amber-200 text-amber-700 animate-pulse hover:bg-amber-100"
                    : THEME_COLORS[themeColor].badgeInactive
                }`}
                title={updateAvailable ? `${t("updateAvailable")} ${latestVersion}` : t("versionInfo")}
              >
                {updateAvailable ? (
                  <AlertTriangle size={11} className="text-amber-500 animate-bounce" />
                ) : (
                  <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
                )}
                <span>v{appVersion}</span>
              </button>

              {/* Language Selector Dropdown Button next to settings button */}
              <div className="relative">
                <button
                  type="button"
                  onClick={() => setShowLangDropdown(!showLangDropdown)}
                  className={`p-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1 text-[11px] font-bold hover:bg-slate-100/50 ${THEME_COLORS[themeColor].textMuted} hover:${THEME_COLORS[themeColor].textPrimary}`}
                  title="Cambiar idioma / Change language"
                >
                  <span className="text-xs">
                    {currentLang === "US" ? "🇺🇸" :
                     currentLang === "ES" ? "🇪🇸" :
                     currentLang === "FR" ? "🇫🇷" :
                     currentLang === "JP" ? "🇯🇵" :
                     currentLang === "CN" ? "🇨🇳" :
                     currentLang === "RU" ? "🇷🇺" :
                     currentLang === "BR" ? "🇧🇷" :
                     currentLang === "DE" ? "🇩🇪" : "🌐"}
                  </span>
                  <span className="text-[10px] font-mono">{currentLang}</span>
                  <ChevronDown size={10} className="opacity-60" />
                </button>

                {showLangDropdown && (
                  <>
                    {/* Background click-catcher to close dropdown */}
                    <div 
                      className="fixed inset-0 z-40" 
                      onClick={() => setShowLangDropdown(false)} 
                    />
                    <div className={`absolute right-0 mt-1 w-36 rounded-xl border shadow-lg py-1 z-50 max-h-60 overflow-y-auto ${THEME_COLORS[themeColor].cardBg} ${THEME_COLORS[themeColor].cardBorder}`}>
                      {(["US", "ES", "FR", "JP", "CN", "RU", "BR", "DE"] as const).map((lang) => {
                        const active = currentLang === lang;
                        const flag = 
                          lang === "US" ? "🇺🇸" :
                          lang === "ES" ? "🇪🇸" :
                          lang === "FR" ? "🇫🇷" :
                          lang === "JP" ? "🇯🇵" :
                          lang === "CN" ? "🇨🇳" :
                          lang === "RU" ? "🇷🇺" :
                          lang === "BR" ? "🇧🇷" :
                          lang === "DE" ? "🇩🇪" : "";
                        const name = 
                          lang === "US" ? "English" :
                          lang === "ES" ? "Español" :
                          lang === "FR" ? "Français" :
                          lang === "JP" ? "日本語" :
                          lang === "CN" ? "简体中文" :
                          lang === "RU" ? "Русский" :
                          lang === "BR" ? "Português" :
                          lang === "DE" ? "Deutsch" : lang;

                        return (
                          <button
                            key={lang}
                            onClick={() => {
                              setCurrentLang(lang);
                              setShowLangDropdown(false);
                              setMascotState("winking");
                              setTimeout(() => setMascotState("idle"), 1000);
                            }}
                            className={`w-full text-left px-3 py-1.5 text-xs font-medium flex items-center gap-2 transition-all cursor-pointer ${
                              active
                                ? `${THEME_COLORS[themeColor].bgLightSolid} ${THEME_COLORS[themeColor].textSimple} font-bold`
                                : `${THEME_COLORS[themeColor].textSecondary} hover:bg-black/5`
                            }`}
                          >
                            <span className="text-sm leading-none">{flag}</span>
                            <span className="font-mono text-[10px]">{lang}</span>
                            <span className="text-[10px] ml-auto opacity-75">{name}</span>
                          </button>
                        );
                      })}
                    </div>
                  </>
                )}
              </div>

              {/* Adjustments gear button */}
              <button
                type="button"
                onClick={() => setShowSettings(true)}
                className={`p-1.5 rounded-lg transition-all cursor-pointer hover:bg-slate-100/50 ${THEME_COLORS[themeColor].textMuted} hover:${THEME_COLORS[themeColor].textPrimary}`}
                title={t("settingsTitle")}
              >
                <Settings size={15} />
              </button>

              <Mascot state={mascotState} size={24} />
            </div>
          </div>

          {/* SECTION: FILE UPLOADER */}
          <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} shadow-xs rounded-2xl p-4 flex flex-col gap-3 transition-colors duration-300`}>
            <h2 className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase tracking-widest font-bold flex items-center gap-1.5`}>
              <UploadCloud size={11} className={THEME_COLORS[themeColor].textMuted} />
              {t("uploadTitle")}
            </h2>

            <div className="flex gap-3 w-full">
              <button
                type="button"
                onClick={async () => {
                  if ((window as any).pywebview) {
                    const files = await (window as any).pywebview.api.select_files();
                    if (files && files.length > 0) {
                      const pendingFiles = files.map((f: any) => {
                        const p = typeof f === 'string' ? f : f.path;
                        const s = typeof f === 'string' ? 0 : f.size;
                        return { name: p.split(/[\\/]/).pop(), path: p, type: activeMediaType, size: s, isDirectory: false };
                      });
                      appendFilesToQueue(pendingFiles);
                    }
                  } else {
                    document.getElementById('file-upload')?.click();
                  }
                }}
                className={`flex-1 py-3 px-4 flex flex-col items-center justify-center gap-1.5 border ${THEME_COLORS[themeColor].cardBorder} ${THEME_COLORS[themeColor].inputBg} rounded-xl text-[10px] font-bold hover:opacity-85 transition-all cursor-pointer`}
              >
                <File size={16} className={THEME_COLORS[themeColor].textMuted} />
                <span className={THEME_COLORS[themeColor].textSimple}>{t("uploadFiles")}</span>
              </button>
              <button
                type="button"
                onClick={async () => {
                  if ((window as any).pywebview) {
                    const folder = await (window as any).pywebview.api.select_folder();
                    if (folder) {
                      const counts = await (window as any).pywebview.api.scan_directory(folder);
                      addLog(`Carpeta seleccionada con: ${counts.audio} audio, ${counts.video} video, ${counts.image} img`, "info");
                      const pendingFiles = [{ name: folder.split(/[\\/]/).pop(), path: folder, type: activeMediaType, size: counts.total_size || 0, isDirectory: true }];
                      appendFilesToQueue(pendingFiles);
                    }
                  }
                }}
                className={`flex-1 py-3 px-4 flex flex-col items-center justify-center gap-1.5 border ${THEME_COLORS[themeColor].cardBorder} ${THEME_COLORS[themeColor].inputBg} rounded-xl text-[10px] font-bold hover:opacity-85 transition-all cursor-pointer`}
              >
                <Folder size={16} className={THEME_COLORS[themeColor].textMuted} />
                <span className={THEME_COLORS[themeColor].textSimple}>{t("uploadFolderRecursive")}</span>
              </button>
              <input
                id="file-upload"
                type="file"
                onChange={handleManualFileInput}
                className="hidden"
                multiple
                accept="video/*,audio/*,image/*"
              />
            </div>
          </div>

          {/* SECTION: COLA DE PROCESAMIENTO POR LOTES (BATCH) */}
          {filesQueue.length > 0 && (
            <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} shadow-xs rounded-2xl p-4 flex flex-col gap-3 transition-colors duration-300`}>
              <div className="flex items-center justify-between border-b pb-1.5" style={{ borderColor: themeColor === "white" ? "#f1f5f9" : "rgba(255,255,255,0.08)" }}>
                <h2 className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase tracking-widest font-bold flex items-center gap-1.5`}>
                  <Layers size={11} className={THEME_COLORS[themeColor].accentIcon} />
                  {t("processingQueue")} ({filesQueue.filter(f => f.status === "completed").length}/{filesQueue.length})
                </h2>
                <div className="flex items-center gap-1">
                  {isProcessingQueue ? (
                    <button
                      type="button"
                      onClick={pauseBatchQueueProcessing}
                      className="px-1.5 py-0.5 bg-amber-550 hover:bg-amber-600 text-white rounded text-[8px] font-mono font-bold cursor-pointer transition-all"
                    >
                      {t("pause")}
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={startBatchQueueProcessing}
                      disabled={filesQueue.every(f => f.status === "completed")}
                      className={`px-1.5 py-0.5 bg-blue-600 hover:bg-blue-500 text-white rounded text-[8px] font-mono font-bold cursor-pointer transition-all disabled:opacity-50`}
                    >
                      {t("process")}
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={clearBatchQueue}
                    className="px-1.5 py-0.5 bg-rose-600 hover:bg-rose-500 text-white rounded text-[8px] font-mono font-bold cursor-pointer transition-all"
                  >
                    {t("clear")}
                  </button>
                </div>
              </div>

              <div className="space-y-1.5 max-h-36 overflow-y-auto pr-1">
                {filesQueue.map((file, idx) => {
                  const isActive = currentQueueIndex === idx;
                  const isCompleted = file.status === "completed";
                  const isProcessingItem = file.status === "processing";
                  return (
                    <div
                      key={file.id}
                      onClick={() => {
                        if (!isProcessingQueue && !isProcessing) {
                          setCurrentQueueIndex(idx);
                          setSelectedFile(file);
                          setActiveMediaType(file.type);
                        }
                      }}
                      className={`flex items-center justify-between p-2 rounded-xl text-[10px] font-mono transition-all border ${
                        isActive
                          ? `${THEME_COLORS[themeColor].bgLightSolid} ${THEME_COLORS[themeColor].border} font-bold`
                          : `${THEME_COLORS[themeColor].inputBg} ${THEME_COLORS[themeColor].cardBorder} cursor-pointer hover:bg-black/5`
                      }`}
                    >
                      <div className="flex items-center gap-2 overflow-hidden mr-1">
                        {renderMediaTypeIcon(file.type, 11)}
                        <span className={`truncate max-w-[140px] ${isActive ? THEME_COLORS[themeColor].textPrimary : THEME_COLORS[themeColor].textSecondary}`}>
                          {file.path || file.name}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5 shrink-0">
                        <span className={`text-[8px] ${THEME_COLORS[themeColor].textMuted}`}>
                          {formatBytes(file.originalSize, 0)}
                        </span>
                        {isCompleted && (
                          <span className="text-emerald-500 flex items-center gap-0.5 text-[8.5px] font-bold">
                            ✓ OK
                          </span>
                        )}
                        {isProcessingItem && (
                          <span className="text-blue-500 animate-pulse flex items-center gap-0.5 text-[8.5px] font-bold">
                            <RefreshCw size={8} className="animate-spin" /> RUN
                          </span>
                        )}
                        {file.status === "pending" && (
                          <span className={`text-[8.5px] ${THEME_COLORS[themeColor].textMuted}`}>
                            {t("processingQueue").split(" ")[0]}
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* SECTION: OPTIMIZATION PARAMETERS CONTROLLER */}
          <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} shadow-xs rounded-2xl p-4 flex flex-col gap-3 transition-colors duration-300`}>
            <div className="flex items-center justify-between">
              <h2 className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase tracking-widest font-bold flex items-center gap-1.5`}>
                <Sliders size={11} className={THEME_COLORS[themeColor].textMuted} />
                {t("compParameters")}
              </h2>
            </div>

            {/* Media Type Segmented Tabs Control */}
            <div className={`grid grid-cols-3 gap-0.5 p-0.5 ${THEME_COLORS[themeColor].segmentBg} rounded-lg text-[10px] font-medium transition-colors`}>
              {(["video", "audio", "image"] as MediaType[]).map((tab) => (
                <button
                  key={tab}
                  onClick={() => {
                    setActiveMediaType(tab);
                    if (tab === "video") setCodec("libx264");
                  }}
                  className={`py-1 rounded-md capitalize flex items-center justify-center gap-1 cursor-pointer transition-all ${
                    activeMediaType === tab
                      ? THEME_COLORS[themeColor].segmentActive + " font-bold"
                      : THEME_COLORS[themeColor].segmentInactive
                  }`}
                >
                  {renderMediaTypeIcon(tab, 10)}
                  <span className="text-[10px]">{tab}</span>
                </button>
              ))}
            </div>

            {/* Settings Form Items */}
            <div className="space-y-3">
              
              {/* Output format preset */}
              <div className="flex flex-col gap-1">
                <label className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase font-bold tracking-wider`}>{t("outputFormat")}</label>
                <select
                  value={format}
                  onChange={(e) => setFormat(e.target.value)}
                  className={`custom-select w-full ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].inputText} rounded-lg px-2.5 py-1 text-[11px] focus:outline-none focus:ring-1 ${THEME_COLORS[themeColor].ring}`}
                >
                  {activeMediaType === "video" && (
                    <>
                      <optgroup label="── Alta Compatibilidad ──">
                        <option value="mp4">MP4 (H.264/AAC) — recomendado</option>
                        <option value="mkv">MKV (Matroska)</option>
                        <option value="avi">AVI</option>
                        <option value="mov">MOV (QuickTime)</option>
                      </optgroup>
                      <optgroup label="── Web / Moderno ──">
                        <option value="webm">WebM (VP9/Opus)</option>
                        <option value="m4v">M4V (iTunes)</option>
                        <option value="ogv">OGV (Ogg Video)</option>
                      </optgroup>
                      <optgroup label="── Otros ──">
                        <option value="flv">FLV (Flash Video)</option>
                        <option value="wmv">WMV (Windows)</option>
                        <option value="mpeg">MPEG (MPEG-1/2)</option>
                        <option value="ts">TS (Transport Stream)</option>
                        <option value="3gp">3GP (Móvil)</option>
                        <option value="gif">GIF (Animación)</option>
                      </optgroup>
                    </>
                  )}
                  {activeMediaType === "audio" && (
                    <>
                      <optgroup label="── Sin pérdida ──">
                        <option value="flac">FLAC (Lossless)</option>
                        <option value="wav">WAV (PCM)</option>
                        <option value="alac">ALAC (Apple Lossless)</option>
                        <option value="aiff">AIFF</option>
                        <option value="wv">WV (WavPack)</option>
                        <option value="au">AU (Sun Audio)</option>
                      </optgroup>
                      <optgroup label="── Con pérdida ──">
                        <option value="mp3">MP3 (MPEG Layer 3)</option>
                        <option value="aac">AAC</option>
                        <option value="m4a">M4A (AAC/iTunes)</option>
                        <option value="opus">Opus</option>
                        <option value="ogg">OGG (Vorbis)</option>
                        <option value="wma">WMA (Windows)</option>
                        <option value="amr">AMR (Móvil)</option>
                      </optgroup>
                      <optgroup label="── Avanzado ──">
                        <option value="ac3">AC3 (Dolby Digital)</option>
                        <option value="dts">DTS</option>
                        <option value="caf">CAF (Apple Core Audio)</option>
                      </optgroup>
                    </>
                  )}
                  {activeMediaType === "image" && (
                    <>
                      <optgroup label="── Web moderno ──">
                        <option value="webp">WebP</option>
                        <option value="avif">AVIF (AV1 Image)</option>
                        <option value="apng">APNG (PNG Animado)</option>
                      </optgroup>
                      <optgroup label="── Estándar ──">
                        <option value="jpg">JPG / JPEG</option>
                        <option value="png">PNG (Lossless)</option>
                        <option value="gif">GIF</option>
                        <option value="bmp">BMP</option>
                        <option value="tiff">TIFF</option>
                        <option value="tga">TGA</option>
                      </optgroup>
                      <optgroup label="── Especial ──">
                        <option value="ico">ICO (Favicon)</option>
                        <option value="pdf">PDF</option>
                      </optgroup>
                    </>
                  )}
                </select>
              </div>

              {/* Resumen de formatos para modo carpeta */}
              {filesQueue.some(f => f.isDirectory) && (
                <div className="flex flex-col gap-1 p-2 rounded-lg border border-dashed" style={{ borderColor: "rgba(99,102,241,0.4)", background: "rgba(99,102,241,0.04)" }}>
                  <span className={`text-[8px] font-mono uppercase font-bold tracking-wider ${THEME_COLORS[themeColor].textMuted}`}>Formatos de salida (carpeta)</span>
                  <div className="flex gap-1.5 flex-wrap">
                    <span className="inline-flex items-center gap-1 text-[9px] px-1.5 py-0.5 rounded font-mono font-bold bg-blue-100 text-blue-700 border border-blue-200">
                      <FileVideo size={8} /> {videoFormat.toUpperCase()}
                    </span>
                    <span className="inline-flex items-center gap-1 text-[9px] px-1.5 py-0.5 rounded font-mono font-bold bg-emerald-100 text-emerald-700 border border-emerald-200">
                      <FileAudio size={8} /> {audioFormat.toUpperCase()}
                    </span>
                    <span className="inline-flex items-center gap-1 text-[9px] px-1.5 py-0.5 rounded font-mono font-bold bg-amber-100 text-amber-700 border border-amber-200">
                      <FileImage size={8} /> {imageFormat.toUpperCase()}
                    </span>
                  </div>
                  <span className={`text-[7.5px] font-mono ${THEME_COLORS[themeColor].textMuted}`}>Selecciona cada pestaña para configurar su formato</span>
                </div>
              )}

              {/* Quality CRF scale */}
              {(activeMediaType === "video" || activeMediaType === "image") && (
                <div className="flex flex-col gap-1">
                  <div className={`flex justify-between text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted}`}>
                    <span className="uppercase font-bold tracking-wider">
                      {activeMediaType === "video" ? `${t("videoCodec")} CRF` : `${t("fileChar")} Q`}
                    </span>
                    <span className={`${THEME_COLORS[themeColor].textSimple} font-bold`}>
                      {quality} {activeMediaType === "video" ? "(CRF)" : "%"}
                    </span>
                  </div>
                  <input
                    type="range"
                    min={activeMediaType === "video" ? "18" : "10"}
                    max={activeMediaType === "video" ? "51" : "100"}
                    value={quality}
                    onChange={(e) => setQuality(parseInt(e.target.value))}
                    className="w-full h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                  />
                  <div className={`flex justify-between text-[8px] font-mono ${THEME_COLORS[themeColor].textMuted}`}>
                    <span>{activeMediaType === "video" ? "18 (CRF)" : "10%"}</span>
                    <span>{activeMediaType === "video" ? "51 (CRF)" : "100%"}</span>
                  </div>
                </div>
              )}

              {/* Video Codec */}
              {activeMediaType === "video" && (
                <div className="flex flex-col gap-1">
                  <label className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase font-bold tracking-wider`}>{t("videoCodec")}</label>
                  <select
                    value={codec}
                    onChange={(e) => setCodec(e.target.value)}
                    className={`custom-select w-full ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].inputText} rounded-lg px-2.5 py-1 text-[11px] focus:outline-none focus:ring-1 ${THEME_COLORS[themeColor].ring}`}
                  >
                    <option value="libx264">H.264 / AVC (libx264)</option>
                      <option value="libx265">H.265 / HEVC (libx265)</option>
                      <option value="libvpx-vp9">VP9 (WebM)</option>
                      <option value="libaom-av1">AV1 (libaom)</option>
                      <option value="libsvtav1">AV1 (SVT-AV1, rápido)</option>
                      <option value="mjpeg">MJPEG</option>
                  </select>
                </div>
              )}

              {/* Audio Bitrate */}
              {(activeMediaType === "video" || activeMediaType === "audio") && (
                <div className="flex flex-col gap-1">
                  <div className={`flex justify-between text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted}`}>
                    <span className="uppercase font-bold tracking-wider">{t("audioBitrate")}</span>
                    <span className={`${THEME_COLORS[themeColor].textSimple} font-bold`}>{audioBitrate} kbps</span>
                  </div>
                  <select
                    value={audioBitrate}
                    onChange={(e) => setAudioBitrate(parseInt(e.target.value))}
                    className={`custom-select w-full ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].inputText} rounded-lg px-2.5 py-1 text-[11px] focus:outline-none focus:ring-1 ${THEME_COLORS[themeColor].ring}`}
                  >
                    <option value="32">32 kbps</option>
                    <option value="64">64 kbps</option>
                    <option value="128">128 kbps</option>
                    <option value="192">192 kbps</option>
                    <option value="320">320 kbps</option>
                  </select>
                </div>
              )}

              {/* Scaling Option */}
              {activeMediaType === "video" && (
                <div className="flex flex-col gap-1">
                  <label className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase font-bold tracking-wider`}>{t("resolutionScale")}</label>
                  <select
                    value={scale}
                    onChange={(e) => setScale(e.target.value)}
                    className={`custom-select w-full ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].inputText} rounded-lg px-2.5 py-1 text-[11px] focus:outline-none focus:ring-1 ${THEME_COLORS[themeColor].ring}`}
                  >
                    <option value="original">{t("originalScale")}</option>
                    <option value="1280x720">720p (HD)</option>
                    <option value="854x480">480p (SD)</option>
                  </select>
                </div>
              )}

              {/* Extra Parameters Input */}
              <div className="flex flex-col gap-1">
                <div className="flex items-center justify-between">
                  <label className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase font-bold tracking-wider`}>{t("customArgs")}</label>
                  <button
                    type="button"
                    onClick={() => setShowExamplesDropdown(!showExamplesDropdown)}
                    className={`flex items-center gap-0.5 text-[9px] ${THEME_COLORS[themeColor].textSimple} hover:underline font-bold transition-all cursor-pointer font-mono`}
                  >
                    <span>{t("formulaFormulas")}</span>
                    {showExamplesDropdown ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
                  </button>
                </div>
                <div className="relative flex items-center">
                  <input
                    type="text"
                    value={customArgs}
                    onChange={(e) => setCustomArgs(e.target.value)}
                    placeholder='Ej: -an'
                    className={`w-full ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].inputText} rounded-lg pl-2.5 pr-8 py-1 text-[11px] focus:outline-none focus:ring-1 ${THEME_COLORS[themeColor].ring} placeholder-gray-400 font-mono`}
                  />
                  <button
                    type="button"
                    onClick={() => setShowExamplesDropdown(!showExamplesDropdown)}
                    className={`absolute right-0 top-0 bottom-0 px-2 flex items-center ${THEME_COLORS[themeColor].textMuted} hover:opacity-85 cursor-pointer`}
                  >
                    {showExamplesDropdown ? <ChevronUp size={11} /> : <ChevronDown size={11} />}
                  </button>
                </div>
              </div>

              {/* Dropdown list of examples */}
              {showExamplesDropdown && (() => {
                type FormulaItem = { cmd: string; desc: string };
                type FormulaGroup = { group: string; desc?: string; items: FormulaItem[] };
                const videoGroups: FormulaGroup[] = [
                  { group: t("formulaGroupVideoImage"), desc: t("formulaGroupVideoImageDesc"), items: [
                    { cmd: "-vf hflip", desc: t("fHflip") },
                    { cmd: "-vf vflip", desc: t("fVflip") },
                    { cmd: "-vf transpose=1", desc: t("fTrans1") },
                    { cmd: "-vf transpose=2", desc: t("fTrans2") },
                    { cmd: "-vf format=gray", desc: t("fGray") },
                    { cmd: "-vf negate", desc: t("fNegate") },
                    { cmd: "-vf eq=brightness=0.05", desc: t("fBright5") },
                    { cmd: "-vf eq=contrast=1.3", desc: t("fCont30") },
                    { cmd: "-vf eq=saturation=1.5", desc: t("fSat50") },
                    { cmd: "-vf unsharp=5:5:1.5", desc: t("fUnsharp") },
                    { cmd: "-vf boxblur=2:2", desc: t("fBoxblur") },
                    { cmd: "-vf scale=1280:-2", desc: t("fScale1280") },
                    { cmd: "-vf pad=1920:1080:(ow-iw)/2:(oh-ih)/2", desc: t("fPadLetterbox") },
                  ]},
                  { group: t("formulaGroupVideoAudio"), desc: t("formulaGroupVideoAudioDesc"), items: [
                    { cmd: "-an", desc: t("fAn") },
                    { cmd: "-vn", desc: t("fVn") },
                    { cmd: "-c:a copy", desc: t("fCaCopy") },
                    { cmd: "-af volume=1.5", desc: t("fAfVol15") },
                    { cmd: "-af loudnorm", desc: t("fLoudnorm") },
                  ]},
                  { group: t("formulaGroupVideoTime"), desc: t("formulaGroupVideoTimeDesc"), items: [
                    { cmd: "-ss 00:00:30 -t 60", desc: t("fSsTrim") },
                    { cmd: "-r 30", desc: t("fR30") },
                    { cmd: "-r 60", desc: t("fR60") },
                    { cmd: "-vf setpts=0.5*PTS", desc: t("fSetpts05") },
                    { cmd: "-vf setpts=2.0*PTS", desc: t("fSetpts20") },
                  ]},
                  { group: t("formulaGroupVideoStream"), desc: t("formulaGroupVideoStreamDesc"), items: [
                    { cmd: "-c:v copy", desc: t("fCvCopy") },
                    { cmd: "-movflags +faststart", desc: t("fMovflags") },
                    { cmd: "-threads 4", desc: t("fThreads4") },
                    { cmd: "-b:v 2M", desc: t("fBv2m") },
                    { cmd: "-crf 18", desc: t("fCrf18") },
                  ]},
                ];
                const audioGroups: FormulaGroup[] = [
                  { group: t("formulaGroupAudioVol"), desc: t("formulaGroupAudioVolDesc"), items: [
                    { cmd: "-af volume=2.0", desc: t("fVol20") },
                    { cmd: "-af volume=1.5", desc: t("fAfVol15") },
                    { cmd: "-af volume=0.5", desc: t("fVol05") },
                    { cmd: "-af loudnorm", desc: t("fLoudnorm") },
                    { cmd: "-af dynaudnorm", desc: t("fDynaudnorm") },
                    { cmd: "-af agate", desc: t("fAgate") },
                  ]},
                  { group: t("formulaGroupAudioChannel"), desc: t("formulaGroupAudioChannelDesc"), items: [
                    { cmd: "-ac 1", desc: t("fAc1") },
                    { cmd: "-ac 2", desc: t("fAc2") },
                    { cmd: "-ar 44100", desc: t("fAr44") },
                    { cmd: "-ar 48000", desc: t("fAr48") },
                    { cmd: "-ar 22050", desc: t("fAr22") },
                  ]},
                  { group: t("formulaGroupAudioFx"), desc: t("formulaGroupAudioFxDesc"), items: [
                    { cmd: "-af atempo=1.5", desc: t("fAtempo15") },
                    { cmd: "-af atempo=0.75", desc: t("fAtempo075") },
                    { cmd: "-af aecho=0.8:0.9:500:0.3", desc: t("fAecho") },
                    { cmd: "-af highpass=f=200", desc: t("fHighpass") },
                    { cmd: "-af lowpass=f=3000", desc: t("fLowpass") },
                    { cmd: "-af afade=t=in:d=3", desc: t("fFadein") },
                    { cmd: "-af afade=t=out:d=3", desc: t("fFadeout") },
                  ]},
                  { group: t("formulaGroupAudioBitrate"), desc: t("formulaGroupAudioBitrateDesc"), items: [
                    { cmd: "-ss 00:01:00 -t 30", desc: t("fTrimAud") },
                    { cmd: "-c:a copy", desc: t("fCaCopy") },
                    { cmd: "-b:a 320k", desc: t("fBa320") },
                    { cmd: "-b:a 128k", desc: t("fBa128") },
                    { cmd: "-b:a 64k", desc: t("fBa64") },
                  ]},
                ];
                const imageGroups: FormulaGroup[] = [
                  { group: t("formulaGroupImageTransform"), desc: t("formulaGroupImageTransformDesc"), items: [
                    { cmd: "-vf hflip", desc: t("fHflip") },
                    { cmd: "-vf vflip", desc: t("fVflip") },
                    { cmd: "-vf transpose=1", desc: t("fTrans1") },
                    { cmd: "-vf transpose=2", desc: t("fTrans2") },
                    { cmd: "-vf scale=800:-1", desc: t("fScale800") },
                    { cmd: "-vf crop=iw/2:ih:0:0", desc: t("fCrop") },
                    { cmd: "-vf tile=3x3", desc: t("fTile") },
                  ]},
                  { group: t("formulaGroupImageColor"), desc: t("formulaGroupImageColorDesc"), items: [
                    { cmd: "-vf format=gray", desc: t("fGray") },
                    { cmd: "-vf negate", desc: t("fNegate") },
                    { cmd: "-vf eq=brightness=0.1", desc: t("fBright10") },
                    { cmd: "-vf eq=contrast=1.5", desc: t("fCont50") },
                    { cmd: "-vf eq=saturation=0", desc: t("fSat0") },
                    { cmd: "-vf eq=saturation=2", desc: t("fSatDouble") },
                    { cmd: "-vf curves=vintage", desc: t("fVintage") },
                    { cmd: "-vf eq=gamma=1.5", desc: t("fGamma") },
                  ]},
                  { group: t("formulaGroupImageFx"), desc: t("formulaGroupImageFxDesc"), items: [
                    { cmd: "-vf unsharp=5:5:2.0", desc: t("fUnsharpHigh") },
                    { cmd: "-vf unsharp=3:3:0.5", desc: t("fUnsharpLow") },
                    { cmd: "-vf boxblur=4:4", desc: t("fBoxblurGauss") },
                    { cmd: "-vf noise=alls=20:allf=t", desc: t("fNoise") },
                    { cmd: "-vf vignette", desc: t("fVignette") },
                    { cmd: "-vf edgedetect", desc: t("fEdge") },
                  ]},
                ];
                const groups = activeMediaType === "video" ? videoGroups : activeMediaType === "audio" ? audioGroups : imageGroups;
                return (
                  <div className={`flex flex-col ${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} rounded-xl max-h-64 overflow-y-auto shadow-xl`}>
                    {groups.map((g) => (
                      <div key={g.group}>
                        <div className={`sticky top-0 z-10 px-3 py-2 bg-black/5 dark:bg-black/40 backdrop-blur-md border-b ${THEME_COLORS[themeColor].cardBorder}`}>
                          <div className={`text-[10px] font-mono font-bold uppercase tracking-widest ${THEME_COLORS[themeColor].textPrimary} antialiased drop-shadow-sm`}>
                            {g.group}
                          </div>
                          {g.desc && (
                            <div className={`text-[9px] font-sans mt-0.5 ${THEME_COLORS[themeColor].textSecondary} font-medium antialiased leading-tight`}>
                              {g.desc}
                            </div>
                          )}
                        </div>
                        {g.items.map((ex) => (
                          <button
                            key={ex.cmd}
                            type="button"
                            onClick={() => setCustomArgs(customArgs === ex.cmd ? "" : ex.cmd)}
                            className={`w-full text-left px-3 py-2 flex flex-col gap-1 transition-all cursor-pointer border-b last:border-b-0 ${THEME_COLORS[themeColor].cardBorder} ${customArgs === ex.cmd ? THEME_COLORS[themeColor].bgLightSolid : (themeColor === "white" ? "hover:bg-slate-100/80" : "hover:bg-white/10")}`}
                          >
                            <code className={`shrink-0 font-mono text-[11px] font-bold antialiased ${customArgs === ex.cmd ? THEME_COLORS[themeColor].textSimple : THEME_COLORS[themeColor].textPrimary}`}>
                              {ex.cmd}
                            </code>
                            <span className={`font-sans text-[10px] font-medium leading-tight antialiased ${THEME_COLORS[themeColor].textSecondary}`}>
                              {ex.desc}
                            </span>
                          </button>
                        ))}
                      </div>
                    ))}
                  </div>
                );
              })()}
            </div>

            {/* Run Button / Progress Bar Transformation Inside Left panel/Android View */}
            {selectedFile && (
              <div className="w-full mt-2 transition-all">
                {!isProcessing && progress === 0 ? (
                  <button
                    onClick={handleRunOptimization}
                    className={`w-full flex items-center justify-center gap-1.5 px-4 py-2.5 ${THEME_COLORS[themeColor].primary} hover:shadow-md text-xs text-white font-bold rounded-xl transition-all cursor-pointer`}
                  >
                    <PlayCircle size={12} />
                    <span>{t("optimizeBtn").toUpperCase()}</span>
                  </button>
                ) : isProcessing ? (
                  <div className="relative w-full bg-slate-100 border border-slate-300 rounded-xl overflow-hidden h-9 flex items-center justify-center">
                    {/* Progress Fill Background */}
                    <div
                      className={`absolute left-0 top-0 bottom-0 ${THEME_COLORS[themeColor].progress} transition-all duration-150 opacity-15`}
                      style={{ width: `${progress}%` }}
                    />
                    <div className="z-10 flex items-center gap-2 text-xs font-bold font-mono" style={{ color: themeColor === "white" ? "#1e293b" : "inherit" }}>
                      <RefreshCw size={11} className="animate-spin text-blue-500" />
                      <span>{t("optimizingBtn")} {progress}%</span>
                    </div>
                  </div>
                ) : (
                  <div className={`${THEME_COLORS[themeColor].cardBg} border-2 border-dashed ${THEME_COLORS[themeColor].border} p-3 rounded-2xl flex flex-col gap-2.5 transition-all`}>
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono text-emerald-600 flex items-center gap-1 font-bold">
                        <CheckCircle2 size={11} className="text-emerald-500" />
                        {t("successMsg")}
                      </span>
                      <span className={`text-[10px] font-mono font-bold ${THEME_COLORS[themeColor].textSimple}`}>{progress}%</span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-[10px] font-mono">
                      <div className={`flex flex-col ${THEME_COLORS[themeColor].inputBg} p-1.5 rounded border ${THEME_COLORS[themeColor].inputBorder}`}>
                        <span className={`text-[8px] ${THEME_COLORS[themeColor].textMuted} uppercase`}>{t("original")}</span>
                        <span className={`${THEME_COLORS[themeColor].textSecondary} font-bold`}>{simulationMetrics.original}</span>
                      </div>
                      <div className={`flex flex-col ${THEME_COLORS[themeColor].inputBg} p-1.5 rounded border ${THEME_COLORS[themeColor].inputBorder}`}>
                        <span className={`text-[8px] ${THEME_COLORS[themeColor].textMuted} uppercase`}>{t("estimated")}</span>
                        <span className="text-emerald-500 font-extrabold">{simulationMetrics.compressed}</span>
                      </div>
                    </div>

                    <div className="text-[10px] font-mono text-center bg-emerald-50/70 text-emerald-600 py-1 rounded border border-emerald-100 font-bold">
                      {t("savings")}: -{simulationMetrics.savings}%
                    </div>

                    <div className="flex gap-2.5">
                      <button
                        onClick={() => {
                          setProgress(0);
                          setTerminalLogs([]);
                          setMascotState("idle");
                          setFilesQueue([]);
                          setCurrentQueueIndex(-1);
                          setSelectedFile(null);
                        }}
                        className="flex-1 flex items-center justify-center gap-1.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-[10px] font-bold transition-all cursor-pointer font-mono"
                      >
                        <span>¡Listo! Archivos Guardados en Origen</span>
                      </button>
                    </div>
                  </div>
                )}
                {/* Hidden element to maintain logsEndRef */}
                <div ref={logsEndRef} style={{ display: "none" }} />
              </div>
            )}
          </div>

          {/* SECTION: MINI COMPRESSION HISTORY */}
          {optimizationHistory.length > 0 && (
            <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} shadow-xs rounded-2xl p-4 flex flex-col gap-2 transition-colors duration-300`}>
              <h2 className={`text-[9px] font-mono ${THEME_COLORS[themeColor].textMuted} uppercase tracking-widest font-bold border-b ${THEME_COLORS[themeColor].cardBorder} pb-1.5`}>
                {t("historyTitle")} ({optimizationHistory.length})
              </h2>
              <div className="space-y-2 max-h-40 overflow-y-auto pr-1">
                {optimizationHistory.map((item, idx) => (
                  <div key={idx} className={`${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} rounded-xl p-2.5 flex flex-col gap-1 text-[10px] font-mono ${THEME_COLORS[themeColor].textSecondary}`}>
                    <div className={`flex items-center justify-between font-bold ${THEME_COLORS[themeColor].textPrimary}`}>
                      <span className="truncate max-w-[150px]">{item.fileName}</span>
                      <span className={`${THEME_COLORS[themeColor].formatBadge} uppercase text-[9px]`}>{item.format}</span>
                    </div>
                    <div className={`flex justify-between text-[9px] ${THEME_COLORS[themeColor].textMuted}`}>
                      <span>{formatBytes(item.originalSize)} → <strong className={THEME_COLORS[themeColor].textSecondary}>{formatBytes(item.compressedSize)}</strong></span>
                      <span className="text-emerald-600 font-bold">-{item.savingsPercent}%</span>
                    </div>

                  </div>
                ))}
              </div>
            </div>
          )}

        </div>

        {/* TELEMETRY PRIVACY OPT-IN POPUP */}
        {telemetryConsentShow && (
          <div className="absolute inset-0 bg-slate-950/85 backdrop-blur-xs flex items-end justify-center z-50">
            <div className="bg-white rounded-t-3xl w-full p-5 shadow-2xl border-t border-gray-150 flex flex-col gap-4 animate-in slide-in-from-bottom duration-300">
              <div className="flex items-center justify-between border-b border-gray-100 pb-2">
                <div className="flex items-center gap-1.5 text-gray-950 font-display font-black text-xs uppercase tracking-tight">
                  <AlertTriangle size={14} className="text-blue-600 animate-pulse" />
                  <span>Privacidad de Datos</span>
                </div>
              </div>
              <p className="text-[10px] text-gray-600 leading-relaxed font-mono">
                ¡Hola! Alenia Porter es una herramienta gratuita y de código abierto.
                Queremos mejorar continuamente. ¿Nos das permiso para recopilar estadísticas de optimización totalmente anónimas (ahorro de espacio, formatos y tiempos de conversión)?
              </p>
              <div className="flex flex-col gap-1 text-[8.5px] font-mono text-gray-500 bg-gray-50 p-2 rounded-xl">
                <div className="flex justify-between items-center">
                  <span>Tu alias anónimo asignado:</span>
                  <strong className="text-gray-800 bg-gray-200/60 px-2 py-0.5 rounded-md font-bold">{userNickname}</strong>
                </div>
                <div className="flex justify-between items-center">
                  <span>UUID:</span>
                  <strong className="text-gray-800 bg-gray-200/60 px-2 py-0.5 rounded-md font-bold">{userUuid}</strong>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-2 pt-1 font-mono">
                <button
                  type="button"
                  onClick={() => {
                    setTelemetryEnabled(false);
                    localStorage.setItem("alenia_telemetry_consent", "declined");
                    localStorage.setItem("alenia_telemetry_enabled", "false");
                    setTelemetryConsentShow(false);
                    addLog("[Sistema] Has rechazado la telemetría. Alenia Porter funcionará de forma 100% silenciosa y sin conexión.", "info");
                  }}
                  className="py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold text-[9.5px] rounded-xl transition-all cursor-pointer text-center"
                >
                  Mantener Privado
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setTelemetryEnabled(true);
                    localStorage.setItem("alenia_telemetry_consent", "given");
                    localStorage.setItem("alenia_telemetry_enabled", "true");
                    setTelemetryConsentShow(false);
                    addLog("[Sistema] ¡Muchas gracias! Has activado la telemetría de optimización anónima para la comunidad.", "success");
                    submitTelemetryEvent("init", 1, 0, 0);
                  }}
                  className="py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-bold text-[9.5px] rounded-xl transition-all cursor-pointer text-center shadow-xs"
                >
                  Compartir y Apoyar
                </button>
              </div>
            </div>
          </div>
        )}

        {/* VERSION POPUP MODAL */}
        {showVersionModal && (
          <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-xs flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-3xl w-full max-w-[320px] p-5 shadow-2xl border border-gray-100 flex flex-col gap-4 animate-in fade-in zoom-in-95 duration-200">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                <h3 className="font-display font-extrabold text-xs text-gray-950 tracking-tight uppercase">
                  Información de Versión
                </h3>
                <button
                  type="button"
                  onClick={() => {
                    if (!isUpdatingVersion) setShowVersionModal(false);
                  }}
                  className="text-gray-400 hover:text-gray-600 font-bold p-1 text-xs cursor-pointer rounded-lg hover:bg-gray-100"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center bg-gray-50 p-2.5 rounded-xl border border-gray-100">
                  <span className="text-[10px] text-gray-500 font-mono">Versión Actual</span>
                  <span className="text-xs font-bold text-gray-800 bg-gray-200/60 px-2.5 py-0.5 rounded-full font-mono">v{appVersion}</span>
                </div>

                <div className="flex flex-col gap-1.5 bg-blue-50/40 p-3 rounded-xl border border-blue-100/50">
                  <span className="text-[9px] text-blue-800 font-mono uppercase tracking-wider font-bold">Enlace a Github</span>
                  <a
                    href="https://github.com/Kaia-Alenia/Alenia-Porter"
                    target="_blank"
                    rel="noreferrer"
                    className="text-[10.5px] font-mono font-medium text-blue-600 hover:text-blue-700 hover:underline flex items-center gap-1"
                  >
                    <span>Kaia-Alenia/Alenia-Porter</span>
                    <ExternalLink size={10} />
                  </a>
                </div>

                {updateAvailable && (
                  <div className="p-3 bg-amber-50 border border-amber-100 rounded-xl flex flex-col gap-2">
                    <div className="flex items-center gap-1.5 text-amber-800 font-bold text-[10px]">
                      <AlertTriangle size={12} className="text-amber-500 animate-bounce" />
                      <span>¡NUEVA VERSIÓN DISPONIBLE!</span>
                    </div>
                    <p className="text-[9.5px] text-amber-700 leading-normal">
                      Hay una actualización disponible en GitHub (v{latestVersion}). Se recomienda actualizar para obtener optimizaciones de audio, video e imágenes.
                    </p>

                    {isUpdatingVersion ? (
                      <div className="space-y-1.5 mt-1">
                        <div className="flex justify-between text-[8.5px] font-mono text-amber-800 font-bold">
                          <span>Descargando actualización...</span>
                          <span>{updateProgress}%</span>
                        </div>
                        <div className="w-full bg-amber-200/60 rounded-full h-1.5 overflow-hidden">
                          <div className="bg-amber-500 h-full transition-all duration-150" style={{ width: `${updateProgress}%` }} />
                        </div>
                        <p className="text-[8px] text-amber-600 text-center">La app se reiniciará automáticamente al terminar</p>
                      </div>
                    ) : (
                      <div className="flex flex-col gap-1.5 mt-1">
                        <button
                          type="button"
                          onClick={async () => {
                            const isPyWebView = !!(window as any).pywebview;
                            const dlUrl = updateDownloadUrl; // URL directa del binario
                            if (isPyWebView && dlUrl) {
                              // Actualización real via backend Python
                              setIsUpdatingVersion(true);
                              setUpdateProgress(0);
                              (window as any).updateProgress = (p: number) => {
                                setUpdateProgress(p);
                              };
                              try {
                                await (window as any).pywebview.api.download_update(dlUrl);
                              } catch (e) {
                                setIsUpdatingVersion(false);
                                addLog(`[Error] No se pudo iniciar la actualización: ${e}`, "error");
                              }
                            } else {
                              const link = updateUrl || "https://github.com/Kaia-Alenia/Alenia-Porter/releases/latest";
                              try {
                                const parsedUrl = new URL(link);
                                if (parsedUrl.protocol === "https:" && parsedUrl.hostname === "github.com" && parsedUrl.pathname.startsWith("/Kaia-Alenia/Alenia-Porter")) {
                                  window.open(parsedUrl.href, "_blank");
                                }
                              } catch (e) {
                              }
                            }
                          }}
                          className="w-full py-2 bg-amber-500 hover:bg-amber-600 text-white font-bold text-[10px] rounded-lg transition-all cursor-pointer shadow-xs flex items-center justify-center gap-1.5"
                        >
                          <RefreshCw size={11} className="animate-spin-slow" /> Actualizar ahora
                        </button>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* SETTINGS OVERLAY SCREEN */}
        {showSettings && (
          <div className={`absolute inset-0 ${THEME_COLORS[themeColor].bodyBg} z-45 flex flex-col animate-in slide-in-from-bottom duration-300 transition-colors`}>
            {/* Header */}
            <div className={`${THEME_COLORS[themeColor].cardBg} px-4 py-3 border-b ${THEME_COLORS[themeColor].cardBorder} flex items-center gap-3 shrink-0 transition-colors`}>
              <button
                type="button"
                onClick={() => setShowSettings(false)}
                className={`p-1 hover:opacity-80 rounded-lg transition-all cursor-pointer ${THEME_COLORS[themeColor].textPrimary}`}
              >
                <ArrowLeft size={16} />
              </button>
              <h2 className={`font-display font-black text-xs ${THEME_COLORS[themeColor].textPrimary} uppercase tracking-wider`}>
                {t("settingsTitle")}
              </h2>
            </div>

            {/* Content (Scrollable) */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              
              {/* SECTION 1: APARIENCIA */}
              <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} rounded-2xl p-4 shadow-2xs space-y-3 transition-colors`}>
                <div className={`flex items-center gap-2 border-b ${THEME_COLORS[themeColor].cardBorder} pb-2`}>
                  <Palette size={14} className={THEME_COLORS[themeColor].textSimple} />
                  <h3 className={`text-[10px] font-mono font-bold ${THEME_COLORS[themeColor].textPrimary} uppercase tracking-widest`}>
                    {t("visualCustomization")}
                  </h3>
                </div>
                <p className={`text-[9.5px] ${THEME_COLORS[themeColor].textMuted} font-mono leading-normal`}>
                  {t("themeLabel")}
                </p>
                
                <div className="grid grid-cols-3 gap-2 pt-1">
                  {(Object.keys(THEME_COLORS) as Array<keyof typeof THEME_COLORS>).map((col) => {
                    const active = themeColor === col;
                    return (
                      <button
                        key={col}
                        type="button"
                        onClick={() => setThemeColor(col)}
                        className={`py-2 px-1 rounded-xl border text-[9px] font-bold capitalize transition-all cursor-pointer flex flex-col items-center gap-1.5 ${
                          active
                            ? `${THEME_COLORS[col].bgLightSolid} ${THEME_COLORS[col].border} ${THEME_COLORS[col].textSimple} shadow-xs ring-1 ring-offset-1 ring-slate-200`
                            : `${THEME_COLORS[themeColor].inputBg} ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].textSecondary} hover:opacity-85`
                        }`}
                      >
                        <span className={`w-3.5 h-3.5 rounded-full ${
                          col === "slate" ? "bg-slate-800" :
                          col === "blue" ? "bg-blue-600" :
                          col === "emerald" ? "bg-emerald-600" :
                          col === "violet" ? "bg-violet-600" :
                          col === "white" ? "bg-white border border-slate-300" :
                          col === "dark" ? "bg-gray-900 border border-gray-600" :
                          col === "cream" ? "bg-amber-100 border border-amber-300" :
                          "bg-rose-600"
                        }`}></span>
                        <span>{
                          col === "white" ? t("themeWhite") :
                          col === "dark" ? t("themeDark") :
                          col === "cream" ? t("themeCream") :
                          col
                        }</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* SECTION 2: ACERCA DE */}
              <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} rounded-2xl p-4 shadow-2xs space-y-3 transition-colors`}>
                <div className={`flex items-center gap-2 border-b ${THEME_COLORS[themeColor].cardBorder} pb-2`}>
                  <BookOpen size={14} className={THEME_COLORS[themeColor].textSimple} />
                  <h3 className={`text-[10px] font-mono font-bold ${THEME_COLORS[themeColor].textPrimary} uppercase tracking-widest`}>
                    {t("supportedFormats")}
                  </h3>
                </div>
                <p className={`text-[9.5px] ${THEME_COLORS[themeColor].textMuted} font-mono leading-normal`}>
                  {t("supportedFormatsDesc")}
                </p>

                <div className="space-y-3">
                  {/* Imagen */}
                  <div className="space-y-1">
                    <span className={`text-[8px] font-mono font-bold ${THEME_COLORS[themeColor].textMuted} uppercase tracking-wider block`}>IMAGEN</span>
                    <div className="flex flex-wrap gap-1">
                      {["webp", "jpg", "png", "gif", "bmp", "ico", "tiff"].map((fmt) => (
                        <span key={fmt} className="text-[8px] font-mono font-semibold bg-blue-50 border border-blue-100/50 text-blue-700 px-1.5 py-0.5 rounded">
                          .{fmt}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Video */}
                  <div className="space-y-1">
                    <span className={`text-[8px] font-mono font-bold ${THEME_COLORS[themeColor].textMuted} uppercase tracking-wider block`}>VIDEO</span>
                    <div className="flex flex-wrap gap-1">
                      {["mp4", "webm", "gif", "avi", "mkv", "mov", "3gp", "flv", "mpeg"].map((fmt) => (
                        <span key={fmt} className="text-[8px] font-mono font-semibold bg-emerald-50 border border-emerald-100/50 text-emerald-700 px-1.5 py-0.5 rounded">
                          .{fmt}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Audio */}
                  <div className="space-y-1">
                    <span className={`text-[8px] font-mono font-bold ${THEME_COLORS[themeColor].textMuted} uppercase tracking-wider block`}>AUDIO</span>
                    <div className="flex flex-wrap gap-1">
                      {["ogg", "opus", "mp3", "wav", "flac", "aac", "amr", "wma"].map((fmt) => (
                        <span key={fmt} className="text-[8px] font-mono font-semibold bg-violet-50 border border-violet-100/50 text-violet-700 px-1.5 py-0.5 rounded">
                          .{fmt}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* SECTION 3: APOYAR */}
              <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} rounded-2xl p-4 shadow-2xs space-y-3 transition-colors`}>
                <div className={`flex items-center gap-2 border-b ${THEME_COLORS[themeColor].cardBorder} pb-2`}>
                  <Heart size={14} className="text-rose-500 fill-rose-500/10" />
                  <h3 className={`text-[10px] font-mono font-bold ${THEME_COLORS[themeColor].textPrimary} uppercase tracking-widest`}>
                    {t("supportTitle")}
                  </h3>
                </div>
                <p className={`text-[9.5px] ${THEME_COLORS[themeColor].textMuted} font-mono leading-normal`}>
                  {t("supportDesc")}
                </p>

                <div className="flex flex-col gap-2 font-mono text-[9px]">
                  {/* Github */}
                  <a
                    href="https://github.com/Kaia-Alenia"
                    target="_blank"
                    rel="noreferrer"
                    className={`flex items-center justify-between p-2 rounded-xl ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].textSecondary} hover:opacity-85 transition-all cursor-pointer`}
                  >
                    <span className={THEME_COLORS[themeColor].textMuted}>github:</span>
                    <span className={`font-bold flex items-center gap-1 ${THEME_COLORS[themeColor].textPrimary}`}>
                      Kaia-Alenia <ExternalLink size={10} />
                    </span>
                  </a>

                  {/* Patreon */}
                  <a
                    href="https://patreon.com/alenia_studios"
                    target="_blank"
                    rel="noreferrer"
                    className={`flex items-center justify-between p-2 rounded-xl ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].textSecondary} hover:opacity-85 transition-all cursor-pointer`}
                  >
                    <span className={THEME_COLORS[themeColor].textMuted}>patreon:</span>
                    <span className={`font-bold flex items-center gap-1 ${THEME_COLORS[themeColor].textPrimary}`}>
                      alenia_studios <ExternalLink size={10} />
                    </span>
                  </a>

                  {/* Ko-fi */}
                  <a
                    href="https://ko-fi.com/alenia_studios"
                    target="_blank"
                    rel="noreferrer"
                    className={`flex items-center justify-between p-2 rounded-xl ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].textSecondary} hover:opacity-85 transition-all cursor-pointer`}
                  >
                    <span className={THEME_COLORS[themeColor].textMuted}>ko_fi:</span>
                    <span className={`font-bold flex items-center gap-1 ${THEME_COLORS[themeColor].textPrimary}`}>
                      alenia_studios <ExternalLink size={10} />
                    </span>
                  </a>

                  {/* Paypal Link */}
                  <a
                    href="https://www.paypal.com/ncp/payment/TCCYMCFSVMV8E"
                    target="_blank"
                    rel="noreferrer"
                    className={`flex items-center justify-between p-2 rounded-xl ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].textSecondary} hover:opacity-85 transition-all cursor-pointer`}
                  >
                    <span className={THEME_COLORS[themeColor].textMuted}>paypal:</span>
                    <span className="text-blue-600 font-bold flex items-center gap-1 truncate max-w-[180px]">
                      {t("donatePaypal")} <ExternalLink size={10} />
                    </span>
                  </a>

                  {/* Itch.io Link */}
                  <a
                    href="https://alenia-studios.itch.io/"
                    target="_blank"
                    rel="noreferrer"
                    className={`flex items-center justify-between p-2 rounded-xl ${THEME_COLORS[themeColor].inputBg} border ${THEME_COLORS[themeColor].inputBorder} ${THEME_COLORS[themeColor].textSecondary} hover:opacity-85 transition-all cursor-pointer`}
                  >
                    <span className={THEME_COLORS[themeColor].textMuted}>itch.io:</span>
                    <span className="text-rose-600 font-bold flex items-center gap-1 truncate max-w-[180px]">
                      alenia-studios.itch.io <ExternalLink size={10} />
                    </span>
                  </a>
                </div>
              </div>

              {/* SECTION 4: RENDIMIENTO Y DIAGNÓSTICO */}
              <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} rounded-2xl p-4 shadow-2xs space-y-3 transition-colors`}>
                <div className={`flex items-center gap-2 border-b ${THEME_COLORS[themeColor].cardBorder} pb-2`}>
                  <Sliders size={14} className={THEME_COLORS[themeColor].textSimple} />
                  <h3 className={`text-[10px] font-mono font-bold ${THEME_COLORS[themeColor].textPrimary} uppercase tracking-widest`}>
                    {t("supportTitle")}
                  </h3>
                </div>

                <div className="space-y-2.5">
                  <div className="flex items-center justify-between">
                    <div className="flex flex-col gap-0.5">
                      <span className={`text-[9.5px] font-bold ${THEME_COLORS[themeColor].textPrimary}`}>{t("hardwareAcceleration")}</span>
                      <span className={`text-[8px] ${THEME_COLORS[themeColor].textMuted} font-mono`}>{t("hwDetectedLabel")}: {gpuEncoderDetected}</span>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={hardwareAccelerationEnabled}
                        onChange={(e) => {
                          setHardwareAccelerationEnabled(e.target.checked);
                          localStorage.setItem("alenia_hw_acc", e.target.checked ? "true" : "false");
                          addLog(e.target.checked ? `[${t("systemSettings")}] ${t("hardwareAcceleration")} enabled.` : `[${t("systemSettings")}] ${t("hardwareAcceleration")} disabled.`, "info");
                        }}
                        className="sr-only peer"
                      />
                      <div className="w-7 h-4 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex flex-col gap-0.5">
                      <span className={`text-[9.5px] font-bold ${THEME_COLORS[themeColor].textPrimary}`}>{t("safeMode")}</span>
                      <span className={`text-[8px] ${THEME_COLORS[themeColor].textMuted} font-mono`}>{t("safeModeDesc")}</span>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={safeMode}
                        onChange={(e) => {
                          setSafeMode(e.target.checked);
                          localStorage.setItem("alenia_safe_mode", e.target.checked ? "true" : "false");
                          addLog(e.target.checked ? `[${t("systemSettings")}] ${t("safeMode")} enabled.` : `[${t("systemSettings")}] ${t("safeMode")} disabled.`, "info");
                        }}
                        className="sr-only peer"
                      />
                      <div className="w-7 h-4 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="pt-1.5 border-t" style={{ borderColor: themeColor === "white" ? "#f1f5f9" : "rgba(255,255,255,0.08)" }}>
                    <button
                      type="button"
                      onClick={generateCrashDump}
                      className="w-full flex items-center justify-center gap-1.5 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-[9px] font-bold transition-all cursor-pointer font-mono"
                    >
                      <AlertTriangle size={11} /> {t("downloadCrashDump")}
                    </button>
                    <p className={`text-[7.5px] ${THEME_COLORS[themeColor].textMuted} font-mono text-center mt-1`}>
                      {t("crashDumpDesc")}
                    </p>
                  </div>
                </div>
              </div>

              {/* SECTION 5: PRIVACIDAD Y TELEMETRÍA DE LA COMUNIDAD */}
              <div className={`${THEME_COLORS[themeColor].cardBg} border ${THEME_COLORS[themeColor].cardBorder} rounded-2xl p-4 shadow-2xs space-y-3 transition-colors`}>
                <div className={`flex items-center gap-2 border-b ${THEME_COLORS[themeColor].cardBorder} pb-2`}>
                  <CheckCircle2 size={14} className={THEME_COLORS[themeColor].textSimple} />
                  <h3 className={`text-[10px] font-mono font-bold ${THEME_COLORS[themeColor].textPrimary} uppercase tracking-widest`}>
                    {t("privacyTitle")}
                  </h3>
                </div>

                <div className="space-y-2.5">
                  <div className="flex items-center justify-between">
                    <div className="flex flex-col gap-0.5">
                      <span className={`text-[9.5px] font-bold ${THEME_COLORS[themeColor].textPrimary}`}>{t("sendTelemetry")}</span>
                      <div className="flex items-center gap-2">
                        {isEditingNickname ? (
                          <div className="flex items-center gap-1">
                            <input 
                              type="text" 
                              value={tempNickname} 
                              onChange={(e) => setTempNickname(e.target.value)}
                              className="text-[8px] px-1 py-0.5 border rounded w-24 bg-transparent outline-none"
                              style={{ borderColor: themeColor === "white" ? "#cbd5e1" : "rgba(255,255,255,0.2)", color: themeColor === "white" ? "#1e293b" : "#f8fafc" }}
                              maxLength={20}
                              autoFocus
                            />
                            <button 
                              onClick={() => {
                                if (tempNickname.trim()) {
                                  setUserNickname(tempNickname.trim());
                                  localStorage.setItem("alenia_user_nickname", tempNickname.trim());
                                  localStorage.setItem("alenia_nickname_customized", "true");
                                  setNicknameCustomized(true);
                                  if ((window as any).pywebview && (window as any).pywebview.api && (window as any).pywebview.api.set_nickname) {
                                    (window as any).pywebview.api.set_nickname(tempNickname.trim());
                                  }
                                }
                                setIsEditingNickname(false);
                              }}
                              className="text-[8px] bg-blue-500 hover:bg-blue-600 text-white px-1.5 py-0.5 rounded cursor-pointer transition-colors"
                            >
                              {t("nicknameSave")}
                            </button>
                            <button 
                              onClick={() => setIsEditingNickname(false)}
                              className="text-[8px] bg-gray-500 hover:bg-gray-600 text-white px-1.5 py-0.5 rounded cursor-pointer transition-colors"
                            >
                              {t("nicknameCancel")}
                            </button>
                          </div>
                        ) : (
                          <div className="flex items-center gap-1">
                            <span className={`text-[8px] ${THEME_COLORS[themeColor].textMuted} font-mono`}>{t("nicknameAlias")}: {userNickname}</span>
                            <button 
                              onClick={() => {
                                setTempNickname(userNickname);
                                setIsEditingNickname(true);
                              }}
                              className="text-[8px] text-blue-500 hover:text-blue-600 underline cursor-pointer"
                            >
                              {t("nicknameEdit")}
                            </button>
                          </div>
                        )}
                      </div>
                      <span className={`text-[8px] ${THEME_COLORS[themeColor].textMuted} font-mono`}>UUID: {userUuid}</span>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={telemetryEnabled}
                        onChange={(e) => {
                          setTelemetryEnabled(e.target.checked);
                          localStorage.setItem("alenia_telemetry_enabled", e.target.checked ? "true" : "false");
                          localStorage.setItem("alenia_telemetry_consent", "given");
                          addLog(e.target.checked ? `[${t("systemSettings")}] ${t("sendTelemetry")} enabled.` : `[${t("systemSettings")}] ${t("sendTelemetry")} disabled.`, "info");
                        }}
                        className="sr-only peer"
                      />
                      <div className="w-7 h-4 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="pt-2 border-t space-y-2" style={{ borderColor: themeColor === "white" ? "#f1f5f9" : "rgba(255,255,255,0.08)" }}>
                    <span className={`text-[8px] font-mono font-bold ${THEME_COLORS[themeColor].textMuted} uppercase tracking-wider block`}>
                      {t("communityDashboard")}
                    </span>
                    <div className="grid grid-cols-2 gap-1.5 text-[8.5px] font-mono">
                      <div className={`p-1.5 rounded border flex flex-col ${THEME_COLORS[themeColor].inputBg}`} style={{ borderColor: themeColor === "white" ? "#f1f5f9" : "rgba(255,255,255,0.08)" }}>
                        <span className={THEME_COLORS[themeColor].textMuted}>{t("files")}</span>
                        <strong className={THEME_COLORS[themeColor].textPrimary}>{globalStats.totalFiles || 0}</strong>
                      </div>
                      <div className={`p-1.5 rounded border flex flex-col ${THEME_COLORS[themeColor].inputBg}`} style={{ borderColor: themeColor === "white" ? "#f1f5f9" : "rgba(255,255,255,0.08)" }}>
                        <span className={THEME_COLORS[themeColor].textMuted}>{t("bytesSaved")}</span>
                        <strong className="text-emerald-500 truncate" title={formatBytes(globalStats.totalBytesSaved || 0)}>
                          {formatBytes(globalStats.totalBytesSaved || 0, 1)}
                        </strong>
                      </div>
                      <div className={`p-1.5 rounded border flex flex-col ${THEME_COLORS[themeColor].inputBg}`} style={{ borderColor: themeColor === "white" ? "#f1f5f9" : "rgba(255,255,255,0.08)" }}>
                        <span className={THEME_COLORS[themeColor].textMuted}>{t("apiRequests")}</span>
                        <strong className={THEME_COLORS[themeColor].textPrimary}>{globalStats.totalEvents || 0}</strong>
                      </div>
                      <div className={`p-1.5 rounded border flex flex-col ${THEME_COLORS[themeColor].inputBg}`} style={{ borderColor: themeColor === "white" ? "#f1f5f9" : "rgba(255,255,255,0.08)" }}>
                        <span className={THEME_COLORS[themeColor].textMuted}>{t("users")}</span>
                        <strong className={THEME_COLORS[themeColor].textPrimary}>{globalStats.uniqueUsers || 0}</strong>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

          </div>
        )}
      </div>
    </div>
  );
}
