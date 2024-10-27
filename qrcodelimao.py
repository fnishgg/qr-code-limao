from flask import Flask, jsonify, send_file, render_template
import qrcode
import io
from PIL import Image

app = Flask(__name__)

# URL base para os QR Codes
base_url = "https://www.instagram.com/limaogalego.restaurante/?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
counter = 1  # Inicia o contador

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    global counter

    if counter > 100:  # Limite de 100 QR Codes
        return render_template('error.html')  # Renderiza a página de erro se o limite for atingido

    # Cria a URL única com o contador atual
    unique_url = f"{base_url}/{counter}"

    # Gera o QR Code para a URL única
    qr_img = qrcode.make(unique_url)

    # Adiciona a imagem de fundo
    background_path = 'static/limaologo.jpg'  # Caminho da imagem de fundo
    try:
        background = Image.open(background_path).convert("RGBA")  # Abre a imagem de fundo e a converte para RGBA
        print("Imagem de fundo carregada com sucesso.")
    except Exception as e:
        return jsonify({"error": f"Erro ao carregar a imagem de fundo: {str(e)}"}), 500

    # Ajusta o tamanho da imagem de fundo para o tamanho do QR Code
    background = background.resize(qr_img.size, Image.LANCZOS)  # Usando LANCZOS para suavizar a imagem

    # Ajusta a opacidade da imagem de fundo
    alpha = background.split()[3]  # Canal alpha
    alpha = alpha.point(lambda p: p * 0.5)  # Ajusta a opacidade (50% de opacidade)
    background.putalpha(alpha)  # Aplica a opacidade

    # Converte o QR Code para RGBA
    qr_img = qr_img.convert("RGBA")

    # Cria uma nova imagem vazia com o mesmo tamanho do QR Code
    combined = Image.new("RGBA", qr_img.size)

    # Coloca a imagem de fundo na imagem combinada
    combined = Image.alpha_composite(combined, background)

    # Adiciona o QR Code
    combined = Image.alpha_composite(combined, qr_img)

    # Incrementa o contador após cada geração de QR Code
    counter += 1

    # Salva a imagem do QR Code com o fundo em memória e envia como resposta
    img_io = io.BytesIO()
    combined.save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
