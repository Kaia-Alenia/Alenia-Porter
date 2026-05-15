from PIL import Image, ImageDraw, ImageFilter
import os

def clean_background_premium(path, output, size):
    if not os.path.exists(path):
        print(f"Error: No existe {path}")
        return
    
    img = Image.open(path).convert("RGBA")
    
    # Recortar bordes vacíos primero
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
        
    img = img.resize(size, Image.Resampling.LANCZOS)
    width, height = img.size
    
    # Solo aplicamos el floodfill y erosión si no es el logo del estudio
    if "studio_logo" not in output:
        ImageDraw.floodfill(img, (0, 0), (0, 0, 0, 0), thresh=50)
        ImageDraw.floodfill(img, (width-1, 0), (0, 0, 0, 0), thresh=50)
        ImageDraw.floodfill(img, (0, height-1), (0, 0, 0, 0), thresh=50)
        ImageDraw.floodfill(img, (width-1, height-1), (0, 0, 0, 0), thresh=50)
        
        # Solo erosionamos si la imagen es grande (personaje de esquina)
        if size[0] > 50:
            alpha = img.getchannel("A")
            alpha = alpha.filter(ImageFilter.MinFilter(3)) 
            alpha = alpha.filter(ImageFilter.SMOOTH)
            img.putalpha(alpha)
    
    img.save(output, "PNG")
    print(f"Asset generado: {output}")

if __name__ == "__main__":
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # 1. Personaje Kaia de la esquina (Estándar)
    logo_path = "copilot_image_1778784278247.jpeg"
    clean_background_premium(logo_path, "assets/kaia_default.png", (100, 100))
    
    # 2. Personaje Kaia de Éxito (Pulgar arriba)
    success_path = "copilot_image_1778784270416.jpeg"
    clean_background_premium(success_path, "assets/kaia_success.png", (120, 120))
    
    # 3. Personaje Kaia de Información (Pintando/Explicando)
    info_path = "copilot_image_1778784269085.jpeg"
    clean_background_premium(info_path, "assets/kaia_info.png", (130, 130))
    
    # 4. Personaje Kaia de Apoyo (Corazón/Cariño)
    support_path = "copilot_image_1778784266687.jpeg"
    clean_background_premium(support_path, "assets/kaia_support.png", (130, 130))
    
    # 5. Icono de la Barra de Progreso (Estándar)
    mini_kaia_path = "copilot_image_1778784780429.jpeg"
    clean_background_premium(mini_kaia_path, "assets/kaia_mini.png", (35, 35))
    
    # 6. Logo del Estudio Estándar
    studio_path = "copilot_image_1778783714837.jpeg"
    clean_background_premium(studio_path, "assets/studio_logo.png", (180, 120))

    # --- ASSETS BLANCOS (CORREGIDOS) ---
    # 7. Logo Blanco para el pie de la app
    clean_background_premium("logo blanco.jpeg", "assets/studio_logo_white.png", (180, 120))
    # 8. Carita Blanca para la barra de progreso
    clean_background_premium("carita blanca.jpeg", "assets/kaia_mini_white.png", (35, 35))
    
    print("Todos los assets han sido procesados.")
