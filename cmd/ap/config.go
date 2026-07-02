package main

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

const version = "1.5.0"

type choice struct {
	Value string
	Label string
}

var (
	scanAudioExts = []string{".aac", ".aif", ".aiff", ".alac", ".amr", ".au", ".caf", ".daud", ".dts", ".flac", ".m4a", ".mid", ".midi", ".mp2", ".mp3", ".mpga", ".ogg", ".opus", ".ra", ".snd", ".voc", ".wav", ".wma", ".wsaud", ".wv"}
	scanVideoExts = []string{".3g2", ".3gp", ".adts", ".asf", ".asf_stream", ".avi", ".avif", ".dts", ".divx", ".fits", ".flv", ".m2ts", ".m4v", ".mkv", ".mp4", ".mpg", ".mpeg", ".mpeg1video", ".mpeg2video", ".mpegts", ".mov", ".mxf", ".mxf_d10", ".mxf_opatom", ".nut", ".ogv", ".rm", ".rtp_mpegts", ".rtsp", ".ts", ".vob", ".webm", ".webm_chunk", ".webm_dash_manifest", ".wmv", ".yuv4mpegpipe"}
	scanImageExts = []string{".apng", ".avif", ".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".mjpeg", ".mpjpeg", ".pdf", ".png", ".smjpeg", ".tga", ".tiff", ".webp"}

	audioFormats = []choice{
		{"aac", "AAC"}, {"aiff", "AIFF"}, {"alac", "ALAC / M4A"}, {"amr", "AMR"},
		{"au", "AU"}, {"ac3", "AC3"}, {"caf", "CAF"}, {"dts", "DTS"},
		{"flac", "FLAC"}, {"m4a", "M4A / AAC"}, {"mp3", "MP3"}, {"ogg", "OGG Vorbis"},
		{"opus", "Opus"}, {"wav", "WAV"}, {"wma", "WMA"}, {"wv", "WavPack"},
	}

	videoFormats = []choice{
		{"3gp", "3GP"}, {"3g2", "3G2"}, {"adts", "ADTS"}, {"asf", "ASF"}, {"asf_stream", "ASF Stream"},
		{"avi", "AVI"}, {"avif", "AVIF"}, {"fits", "FITS"}, {"flv", "FLV"}, {"gif", "GIF"},
		{"m4v", "M4V"}, {"mkv", "MKV"}, {"mp4", "MP4"}, {"mpg", "MPG"}, {"mpeg", "MPEG"},
		{"mpeg1video", "MPEG-1 Video"}, {"mpeg2video", "MPEG-2 Video"}, {"mpegts", "MPEG-TS"},
		{"mov", "MOV"}, {"mxf", "MXF"}, {"mxf_d10", "MXF D-10"}, {"mxf_opatom", "MXF OPAtom"},
		{"nut", "NUT"}, {"ogv", "OGV"}, {"rm", "RealMedia"}, {"rtp_mpegts", "RTP / MPEG-TS"},
		{"rtsp", "RTSP"}, {"ts", "TS"}, {"vob", "VOB"}, {"webm", "WebM"},
		{"webm_chunk", "WebM Chunk"}, {"webm_dash_manifest", "WebM DASH Manifest"},
		{"wmv", "WMV"}, {"yuv4mpegpipe", "YUV4MPEG"},
	}

	imageFormats = []choice{
		{"apng", "APNG"}, {"avif", "AVIF"}, {"bmp", "BMP"}, {"gif", "GIF"},
		{"ico", "ICO"}, {"jpeg", "JPEG"}, {"jpg", "JPG"}, {"mjpeg", "MJPEG"},
		{"mpjpeg", "MPJPEG"}, {"pdf", "PDF"}, {"png", "PNG"}, {"smjpeg", "SMJPEG"},
		{"tga", "TGA"}, {"tiff", "TIFF"}, {"webp", "WebP"},
	}

	languageChoices = []choice{
		{"en", "English"}, {"es", "Español"}, {"fr", "Français"}, {"ja", "日本語"},
		{"zh", "中文"}, {"ru", "Русский"}, {"pt-br", "Português (BR)"}, {"de", "Deutsch"}, {"pt", "Português"},
	}
)

func isExt(name string, exts []string) bool {
	ext := strings.ToLower(filepath.Ext(name))
	for _, e := range exts {
		if ext == e {
			return true
		}
	}
	return false
}

func countMediaFiles(dir string) (int, int, int) {
	v, a, i := 0, 0, 0
	_ = filepath.Walk(dir, func(path string, fi os.FileInfo, err error) error {
		if err != nil || fi == nil {
			return nil
		}
		if fi.IsDir() {
			if fi.Name() == "Alenia_Optimized" {
				return filepath.SkipDir
			}
			return nil
		}
		switch {
		case isExt(fi.Name(), scanVideoExts):
			v++
		case isExt(fi.Name(), scanAudioExts):
			a++
		case isExt(fi.Name(), scanImageExts):
			i++
		}
		return nil
	})
	return v, a, i
}

func languageLabel(code string) string {
	for _, lang := range languageChoices {
		if lang.Value == code {
			return lang.Label
		}
	}
	return code
}

func formatChoiceStrings(items []choice) []string {
	out := make([]string, 0, len(items))
	for _, item := range items {
		out = append(out, fmt.Sprintf("%s - %s", item.Value, item.Label))
	}
	return out
}

func selectedChoiceValue(item string) string {
	if idx := strings.Index(item, " - "); idx > 0 {
		return strings.TrimSpace(item[:idx])
	}
	return strings.TrimSpace(item)
}

func defaultChoice(items []choice, value string) string {
	for _, item := range items {
		if item.Value == value {
			return item.Value
		}
	}
	if len(items) > 0 {
		return items[0].Value
	}
	return ""
}
