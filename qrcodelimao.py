from flask import Flask, jsonify, send_file, render_template
import qrcode
import io

app = Flask(__name__)

# URL base para os QR Codes
base_url = "https://www.instagram.com/limaogalego.restaurante/?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw=="
counter = 1  # Inicia o contador

@app.route('/generate_qr', methods=['GET'])
def generate_qr():
    global counter

    if counter > 5:  # Alterado para 100 conforme sua solicitação
        return render_template('error.html')  # Renderiza a página de erro se o limite for atingido

    # Cria a URL única com o contador atual
    unique_url = f"{base_url}/{counter}"

    # Gera o QR Code para a URL única
    img = qrcode.make(unique_url)

    # Incrementa o contador após cada geração de QR Code
    counter += 1

    # Salva o QR Code em memória e envia como resposta
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
