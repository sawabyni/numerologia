# Importando bibliotecas para o python
from flask import Flask, render_template, request, send_file, make_response, jsonify, url_for, redirect, session, json
import requests
from reportlab.pdfgen import canvas
from io import BytesIO
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import mysql.connector
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random

app = Flask(__name__)  # Cria um site vazio

# chave de seguranca requerida para usar session
app.secret_key = '2kae'


@app.route('/')
def home():
    return render_template('index.html')


def numerology(name):
    # Tabela de conversão letra/número
    letters = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
        'j': 1, 'k': 2, 'l': 3, 'm': 4, 'n': 5, 'o': 6, 'p': 7, 'q': 8, 'r': 9,
        's': 1, 't': 2, 'u': 3, 'v': 4, 'w': 5, 'x': 6, 'y': 7, 'z': 8
    }

    # Converter para minúsculas e remover espaços
    name = name.lower().replace(" ", "")

    # Calcular o valor numerológico
    value = sum(letters.get(c, 0) for c in name)

    # Verificar se o número é um número mestre
    if value in [11, 22, 33, 44, 55, 66, 77, 88, 99]:
        return value, f"{value} mestre"

    # Verificar se os dígitos das casas são iguais
    houses = [int(d) for d in str(value)]
    if all(digit == houses[0] for digit in houses):
        return value, f"{value} é um número com dígitos iguais"

    # Calcular o valor reduzido se o número não for mestre nem tiver dígitos iguais
    while value > 9:
        houses = [int(d) for d in str(value)]
        value = sum(houses)
    return value, value

def sig(value):
    value = int(value)
    if value == 1:
       return f"Representa a liderança, a independência, a criatividade e a coragem. Empresas com esse número tendem a ser inovadoras e pioneiras em seu setor."
    elif value == 2:
       return f"Representa a diplomacia, a cooperação e a sensibilidade. Empresas com esse número tendem a ser bem-sucedidas em parcerias e colaborações."
    elif value == 3:
       return f"Representa a comunicação, a criatividade e a alegria. Empresas com esse número tendem a ser bem-sucedidas em áreas criativas, como publicidade e marketing."
    elif value == 4:
       return f"Representa a estabilidade, a organização e a disciplina. Empresas com esse número tendem a ser bem-sucedidas em áreas que exigem precisão e metodologia. "
    elif value == 5:
       return f"Representa a mudança, a adaptabilidade e a liberdade. Empresas com esse número tendem a ser bem-sucedidas em áreas inovadoras e que exigem flexibilidade. "
    elif value == 6:
       return f"Representa a harmonia, o equilíbrio e a responsabilidade. Empresas com esse número tendem a ser bem-sucedidas em áreas que exigem cuidado e atenção aos detalhes."
    elif value == 7:
       return f"Representa a sabedoria, a intuição e a introspecção. Empresas com esse número tendem a ser bem-sucedidas em áreas que exigem análise e pesquisa. "
    elif value == 8:
       return f"Representa o sucesso, o poder e a ambição. Empresas com esse número tendem a ser bem-sucedidas em áreas de finanças e negócios. "
    elif value == 9:
       return f"Representa a compaixão, a generosidade e a humanidade. Empresas com esse número tendem a ser bem-sucedidas em áreas que exigem ajuda e apoio a outras pessoas. "
    elif value == 11:
       return f"Visto como um dos mais poderosos e influentes números. Esse número representa o potencial para a intuição, a espiritualidade e a inspiração, bem como a capacidade de liderança e de fazer grandes coisas acontecerem." \
              f"Empresas que possuem o número 11 em sua numerologia costumam ser inovadoras, criativas e inspiradoras. Elas tendem a ter uma visão de longo prazo, pensando em como suas ações podem impactar o mundo e contribuir para a evolução da humanidade. Além disso, essas empresas geralmente têm uma forte liderança, com líderes carismáticos e inspiradores." \
              f"Porém, é importante lembrar que o número 11 também pode trazer desafios, especialmente quando há um desequilíbrio entre a energia espiritual e a energia material. Empresas com uma forte influência do número 11 devem se esforçar para manter um equilíbrio saudável entre essas duas energias, de modo a garantir o sucesso e a prosperidade a longo prazo."
    elif value == 22:
       return f"Visto como um número poderoso e influente, que representa o potencial para criar grandes coisas no mundo material." \
              f"Costumam ser visionárias e ambiciosas, com uma forte orientação para o sucesso a longo prazo. Elas tendem a ter uma abordagem pragmática para os negócios, combinando uma visão clara e estratégias práticas para alcançar seus objetivos." \
              f"Essas empresas também são conhecidas por sua capacidade de inovar e pensar fora da caixa, buscando soluções criativas para desafios complexos. Elas tendem a ser muito bem organizadas e estruturadas, com uma forte liderança e um foco em alcançar metas ambiciosas." \
              f"No entanto, o número 22 também pode trazer desafios. Empresas com uma forte influência do número 22 podem ser excessivamente ambiciosas e focadas em resultados, em detrimento do bem-estar de seus funcionários e da sustentabilidade do meio ambiente. É importante que essas empresas se esforcem para manter um equilíbrio saudável entre seus objetivos financeiros e suas responsabilidades sociais e ambientais, a fim de garantir sua prosperidade a longo prazo."
    elif value == 33:
       return f"Representa um alto nível de realização espiritual e material. Ele é um número poderoso e traz um grande potencial de liderança, criatividade e habilidade para inspirar e motivar os outros." \
              f"As empresas com o número 33 em sua numerologia são frequentemente vistas como empresas que têm uma missão ou propósito maior do que apenas obter lucro. Elas geralmente têm uma visão humanitária, com uma abordagem equilibrada para o sucesso financeiro e a melhoria do mundo ao seu redor." \
              f"No entanto, é importante lembrar que a numerologia empresarial é apenas uma ferramenta para entender as energias e características associadas a um número. A verdadeira natureza de uma empresa é determinada por seus valores, práticas e estratégias de negócios. "
    elif value == 44:
       return f"Representa um grande potencial para o sucesso material e a realização espiritual. Empresas com o número 44 em sua numerologia são frequentemente vistas como empresas que têm uma visão clara e uma estratégia bem planejada para atingir seus objetivos." \
              f"O número 44 é frequentemente associado à liderança forte, à habilidade de inspirar e motivar os outros e à capacidade de tomar decisões importantes com confiança e sabedoria. Essas empresas são frequentemente vistas como líderes em seu setor e têm uma forte presença no mercado." \
              f"No entanto, assim como qualquer número na numerologia, o número 44 não é uma garantia de sucesso. O verdadeiro sucesso de uma empresa é determinado por vários fatores, incluindo sua estratégia de negócios, a qualidade de seus produtos ou serviços, sua equipe e sua capacidade de se adaptar às mudanças do mercado. "
    elif value == 55:
       return f"Representa um alto nível de energia e mudança. Esse número traz consigo uma forte vibração de progresso, expansão e crescimento, tanto material quanto espiritual." \
              f"são frequentemente vistas como inovadoras e visionárias, com uma capacidade única de identificar e aproveitar oportunidades de negócios. Essas empresas são frequentemente vistas como pioneiras em seus setores e estão sempre em busca de novas maneiras de crescer e expandir seus negócios." \
              f" também pode trazer desafios e incertezas, já que as mudanças e transformações que ele representa podem ser desconfortáveis ou assustadoras para algumas pessoas. As empresas com o número 55 em sua numerologia devem estar preparadas para lidar com a mudança e se adaptar rapidamente às novas circunstâncias do mercado." \
              f"Como em qualquer outra numerologia, é importante lembrar que o verdadeiro sucesso de uma empresa é determinado por uma série de fatores, incluindo sua estratégia de negócios, seus produtos ou serviços, sua equipe e sua capacidade de se adaptar às mudanças do mercado. O número 55 pode fornecer uma indicação das energias e características associadas a uma empresa, mas não é uma garantia de sucesso. "
    elif value == 66:
       return f"Representa um alto nível de equilíbrio, harmonia e responsabilidade social. Empresas com o número 66 em sua numerologia são frequentemente vistas como empresas que se preocupam profundamente com seu impacto na sociedade e no meio ambiente, e que trabalham para equilibrar o sucesso financeiro com o bem-estar das pessoas e do planeta."\
              f"O número 66 é frequentemente associado à liderança humanitária, à habilidade de inspirar e motivar as pessoas para trabalhar em conjunto por uma causa comum, e à capacidade de tomar decisões importantes com sabedoria e compaixão. Essas empresas são frequentemente vistas como líderes em seu setor, não apenas pelo seu sucesso financeiro, mas também pela sua contribuição para a sociedade." \
              f"No entanto, assim como qualquer número na numerologia, o número 66 não é uma garantia de sucesso. O verdadeiro sucesso de uma empresa é determinado por vários fatores, incluindo sua estratégia de negócios, a qualidade de seus produtos ou serviços, sua equipe e sua capacidade de se adaptar às mudanças do mercado. O número 66 pode fornecer uma indicação das energias e características associadas a uma empresa, mas é importante lembrar que o verdadeiro sucesso vem de um compromisso com a responsabilidade social e uma visão humanitária."
    elif value == 77:
       return f"Representa um alto nível de espiritualidade e busca pelo conhecimento. Empresas com o número 77 em sua numerologia são frequentemente vistas como empresas que estão em busca constante de conhecimento e que trabalham para alcançar um alto nível de excelência em seus produtos ou serviços." \
              f"O número 77 é frequentemente associado à liderança intelectual, à habilidade de inovar e criar soluções inovadoras para problemas complexos, e à capacidade de tomar decisões importantes com base na sabedoria e no conhecimento. Essas empresas são frequentemente vistas como líderes em seu setor, não apenas pelo seu sucesso financeiro, mas também pela sua contribuição para o avanço da tecnologia e do conhecimento em seu campo de atuação." \
              f"No entanto, assim como qualquer número na numerologia, o número 77 não é uma garantia de sucesso. O verdadeiro sucesso de uma empresa é determinado por vários fatores, incluindo sua estratégia de negócios, a qualidade de seus produtos ou serviços, sua equipe e sua capacidade de se adaptar às mudanças do mercado. O número 77 pode fornecer uma indicação das energias e características associadas a uma empresa, mas é importante lembrar que o verdadeiro sucesso vem da busca constante por conhecimento e inovação. "
    elif value == 88:
       return f"Considerado um número muito auspicioso e representa um alto nível de sucesso e prosperidade financeira. Empresas com o número 88 em sua numerologia são frequentemente vistas como empresas que estão destinadas a alcançar o sucesso financeiro e que têm a capacidade de construir uma base financeira sólida e duradoura." \
              f"O número 88 é frequentemente associado à liderança financeira, à habilidade de gerenciar grandes somas de dinheiro com sabedoria e à capacidade de tomar decisões importantes com base em análises financeiras precisas. Essas empresas são frequentemente vistas como líderes em seu setor, não apenas pelo seu sucesso financeiro, mas também pela sua capacidade de investir em seu crescimento futuro e expandir seus negócios." \
              f"No entanto, assim como qualquer número na numerologia, o número 88 não é uma garantia de sucesso. O verdadeiro sucesso de uma empresa é determinado por vários fatores, incluindo sua estratégia de negócios, a qualidade de seus produtos ou serviços, sua equipe e sua capacidade de se adaptar às mudanças do mercado. O número 88 pode fornecer uma indicação das energias e características associadas a uma empresa, mas é importante lembrar que o verdadeiro sucesso vem da capacidade de gerenciar sabiamente as finanças e investir no crescimento futuro da empresa. "
    elif value == 99:
       return f"Representa um alto nível de realização espiritual e humanitária. Empresas com o número 99 em sua numerologia são frequentemente vistas como empresas que estão empenhadas em fazer a diferença no mundo e que trabalham para alcançar um alto nível de sucesso financeiro enquanto contribuem para a sociedade." \
              f"O número 99 é frequentemente associado à liderança humanitária, à habilidade de inspirar e motivar as pessoas para trabalhar em conjunto por uma causa comum, e à capacidade de tomar decisões importantes com sabedoria e compaixão. Essas empresas são frequentemente vistas como líderes em seu setor, não apenas pelo seu sucesso financeiro, mas também pela sua contribuição para a sociedade e para o bem-estar das pessoas." \
              f"O número 99 é também considerado um número de conclusão, o que significa que empresas com este número em sua numerologia podem ser vistas como tendo alcançado um alto nível de sucesso e realização. No entanto, isso não significa que a empresa deva se contentar com seu sucesso atual. É importante continuar a buscar novas maneiras de fazer a diferença e contribuir para a sociedade." \
              f"Em resumo, o número 99 na numerologia empresarial representa uma empresa que se preocupa profundamente com a humanidade e o bem-estar social, enquanto busca alcançar o sucesso financeiro. "

@app.route('/', methods=['POST'])
def separar():
    name = request.form['palavra']
    value, description = numerology(name)
    significado = sig(value)

    # Armazena os valores de name e value na sessão do Flask
    session['name'] = name
    session['value'] = value
    session['significado'] = significado

    # Exibir os resultados na página web
    return render_template('pagamento.html')

# Geracao de PDF
def generate_pdf(name, value, significado):
    # Criar PDF com os resultados
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    imagem = "static/img/logteste.jpg"
    logo = "static/img/logo.gif"
    p.drawImage(imagem, x=0, y=0, width=900, height= 900)
    p.drawImage(logo, x=30, y=730, width=80, height=80)
    p.drawString(100, 650, "Empresa: " + name)
    p.drawString(100, 600, "Numerologia: " + str(value))
    p.drawString(100, 550, "Significado:")
    # Definir posição inicial para a primeira linha do significado
    x, y = 100, 520

    # Quebrar o texto do significado em várias linhas com base na largura do canvas
    significado_lines = []
    line = ''
    for word in significado.split():
        if p.stringWidth(line + word) < 400:
            line += word + ' '
        else:
            significado_lines.append(line)
            line = word + ' '
    significado_lines.append(line)

    # Iterar sobre as linhas do significado
    for line in significado_lines:
        # Se a linha exceder a altura da página, adicionar uma nova página
        if y < 50:
            p.showPage()
            y = 750

        # Adicionar a linha à página atual
        p.drawString(x, y, line)
        y -= 20
    p.showPage()
    p.save()

    # Salvar PDF em arquivo
    buffer.seek(0)

    return buffer
#Link de Download do PDF
@app.route('/download-pdf/<name>/<value>/<significado>')
def download_pdf(name, value, significado):
    # Gerar o PDF com os resultados
    pdf_file = generate_pdf(name, value, significado)

    # Configurar a resposta HTTP para fazer o download do PDF
    response = make_response(pdf_file.getvalue())
    response.headers.set('Content-Disposition', 'attachment', filename='resultados.pdf')
    response.headers.set('Content-Type', 'application/pdf')

    return response

#configuracao do pague seguro (producao ou teste)
def conf():
    sandbox = True
    if sandbox:
        e_aut = "sawabyni@hotmail.com"
        token = "5C40DB411C9B4757A2867EEBAB3182F3"
        url = "https://sandbox.api.pagseguro.com/oauth2/application"
        urlpix = "https://sandbox.api.pagseguro.com/orders"

    else:
        e_aut = "sawabyni@hotmail.com"
        token = "14358cef-3201-4200-80f8-d7bc942aecb7f16ff0c049bd9274da43350bc2bd21e57b66-2eb1-4a16-a78e-7c1ac133b584"
        url = "https://api.pagseguro.com"
        urlpix = "https://api.pagseguro.com/orders"

    return url, token, urlpix, e_aut

url, token, urlpix, e_aut = conf()

# Funcao de pegar a data da geracao do pedido
def data_pedido():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")
    next_date = (datetime.strptime(current_date, '%Y-%m-%d') + relativedelta(months=1)).strftime('%Y-%m-%d')
    d_s_traco = next_date.replace('-', '')
    limite_d_pix = (next_date + "T" + current_time + "-03:00")  # variavel contendo limite de 1 mes para ser pago
    return current_time, current_date, next_date,limite_d_pix, d_s_traco




#gerando numero de pedido (data do pedido e numero random)
def gerar_pedido():
    _, _, _, _, d_s_traco = data_pedido()
    numero_pedido = str(random.randint(10000000, 99999999))
    numero_pedido = (d_s_traco + numero_pedido)
    return numero_pedido



# campos a serem enviados no cartao de credito
@app.route('/cartao', methods=['POST'])
def pagseguro():

    name = request.form['name']
    emailpg = request.form['email']
    cpf = request.form['cpf']
    ncard = request.form['ncard']
    exp_month = request.form['exp_month']
    exp_year = request.form['exp_year']
    s_code = request.form['s_code']

    numero_pedido = gerar_pedido()
    current_time, current_date, _, _, _ = data_pedido()
    tipo_pg = "2"
    status = "1"
    next_date = "2000-01-01"
    conecta_db()
    sel_pg(conn)
    insere_pg(conn, numero_pedido, tipo_pg, status, current_date, current_time,next_date, name, emailpg)

    headers = {
        'Authorization': f"{token} ",
        'Content-Type': 'application/json'
    }
    payload = {
        "reference_id": f"{numero_pedido}",
        "customer": {
            "name": f"{name} ",
            "email": f"{emailpg}",
            "tax_id": f"{cpf}",

        },
        "items": [
            {
                "reference_id": "referencia do item",
                "name": "nome do item",
                "quantity": 1,
                "unit_amount": 700
            }
        ],
        "shipping": {
            "address": {
                "street": "Avenida Brigadeiro Faria Lima",
                "number": "1384",
                "complement": "apto 12",
                "locality": "Pinheiros",
                "city": "São Paulo",
                "region_code": "SP",
                "country": "BRA",
                "postal_code": "01452002"
            }
        },
        "notification_urls": [
            "https://numerologia.up.railway.app/notificacao.html"
        ],
        "charges": [
            {

                "amount": {
                    "value": 500,
                    "currency": "BRL"
                },
                "payment_method": {
                    "type": "CREDIT_CARD",
                    "installments": 1,
                    "capture": True,
                    "card": {
                      "number": f"{ncard}",
                      "exp_month": f"{exp_month}",
                      "exp_year": f"{exp_year}",
                      "security_code": f"{s_code}",
                      "holder": {
                        "name": f"{name} "
                      },
                        "store": False
                    }
                }
            }
        ]
    }
    desconecta_db(conn)
    response = requests.post('https://sandbox.api.pagseguro.com/orders', headers=headers, json=payload)

    if response.ok:
        return redirect(url_for('resultado'))

        # se o pagamento nao foi precessado com sucesso, retorna JSON response
    return jsonify(response.json())

# campos a serem enviados no pix
@app.route('/pix', methods=['POST'])
def pix():
    numero_pedido = gerar_pedido()
    current_time, current_date, next_date,limite_d_pix, _ = data_pedido()
    url = f"{urlpix}"
    emailpg = request.form['epix']
    tipo_pg = "1"
    status = "1"
    name =""
    conecta_db()
    sel_pg(conn)
    insere_pg(conn, numero_pedido, tipo_pg,status, current_date,current_time,next_date,name,emailpg)

    headers = {
        "Content-Type": "application/json",
        'Authorization': f"{token}"

    }

    payload = {
        "reference_id": f"{numero_pedido}",
        "customer": {
            "name": "Jose da Silva",
            "email": f"{emailpg}",
            "tax_id": "12345678909",

        },
        "items": [
            {
                "name": "nome do item",
                "quantity": 1,
                "unit_amount": 500
            }
        ],
        "qr_codes": [
            {
                "amount": {
                    "value": 5000000
                },
                "expiration_date": f"{limite_d_pix}"
            }
        ],
        "shipping": {
            "address": {
                "street": "Avenida Brigadeiro Faria Lima",
                "number": "1384",
                "complement": "apto 12",
                "locality": "Pinheiros",
                "city": "São Paulo",
                "region_code": "SP",
                "country": "BRA",
                "postal_code": "01452002"
            }
        },
        "notification_urls": [
            "https://numerologia.up.railway.app/notificacao.html"
        ]
    }
    desconecta_db(conn)

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        data = response.json()
        href = data['links'][0]['href']
        return render_template('pagamento.html', href=href)
    else:
        return "Erro ao processar a solicitação."


#Recebe as notificacao de pagamento
token = f"{token} "
email = f"{e_aut} "
@app.route('/notificacao', methods=['POST'])
def notificacao():
    # Recebe a notificação enviada pelo PagSeguro por meio de uma solicitação POST
    xml_notification = request.data.decode('utf-8')

    # Analisa o XML de notificação e extrai o código de notificação
    root = ET.fromstring(xml_notification)
    codigo_notificacao = root.find('notificationCode').text

    # Parâmetros do POST de consulta da transação
    params = {'token': token, 'email': email, 'notificationCode': codigo_notificacao}

    # Codifica os parâmetros do POST em formato de consulta
    query_string = urllib.parse.urlencode(params).encode('utf-8')

    # Faz a solicitação de POST e lê a resposta XML
    url = 'https://ws.sandbox.pagseguro.uol.com.br/v3/transactions/notifications/'
    response = urllib.request.urlopen(url, query_string)
    xml_response = response.read().decode('utf-8')

    # Analisa o XML de resposta e extrai as informações necessárias
    root = ET.fromstring(xml_response)
    status = root.find('status').text

    if status == '3':  # Transação concluída
        pagamento_concluido = True
        # Atualiza o status do pagamento no banco de dados
        conecta_db()
        sel_pg(conn)
        cur = conn.cursor()
        cur.execute('UPDATE pagamentos SET status = %s WHERE codigo_notificacao = %s',
                       ('3', codigo_notificacao))
        conn.commit()
        desconecta_db(conn)

    else:
        # Atualiza o status do pagamento no banco de dados
        conecta_db()
        sel_pg(conn)
        cur = conn.cursor()
        cur.execute('UPDATE pagamentos SET status = %s WHERE codigo_notificacao = %s',
                    (status, codigo_notificacao))
        conn.commit()
        desconecta_db(conn)
        pagamento_concluido = False

    # Renderiza o template HTML e passa as informações para ele
    return render_template('notificacao.html', pagamento_concluido=pagamento_concluido)


@app.route('/resultado')
def resultado():
    name = session.get('name', None)
    value = session.get('value', None)
    significado = session.get('significado', None)
    return render_template('resultado.html', name=name, value=value, significado=significado)

# Conecta ao DB
conn = None
def conecta_db():
    global conn
    print(conn)
    if (not conn) or (not conn.is_connected()):
        host = "containers-us-west-60.railway.app"
        port = 6809
        user = "root"
        password = "sK8r1pjr5tJEfU9Y6K9w"
        database = "railway"
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
    return conn

#Seleciona a tabela pagamentos no DB
def sel_pg(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pagamentos")
    rows = cur.fetchall()
    return rows

# Inserindo dados de pagamento na tabela do DB
def insere_pg(conn, numero_pedido,tipo_pg,status ,current_date,current_time,next_date,name,emailpg):
    cur = conn.cursor()
    cur.execute("INSERT INTO pagamentos (referencia,tipo_pg,status,data_compra,hora_compra,data_modificacao,data_exp, nome, email) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (numero_pedido,tipo_pg,status,current_date,current_time,current_date,next_date,name,emailpg))

    conn.commit()

# Desconecta do DB
def desconecta_db(conn):
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)  # coloca o site no ar