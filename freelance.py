import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import time
from datetime import datetime
from dotenv import load_dotenv
import os
import base64

# Carrega variáveis do .env
load_dotenv()

# Configuração inicial da página
st.set_page_config(
    page_title="Automação Python",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS melhorado para estilo visual
st.markdown("""
    <style>
    .stApp {
        background: url('https://img.freepik.com/vetores-gratis/numeros-de-queda-digitais-do-codigo-binario-do-estilo-da-matriz-fundo-azul_1017-37387.jpg?semt=ais_hybrid&w=740');
        background-size: cover;
        font-family: 'Arial', sans-serif;
    }

    .main-container {
        background-color: rgba(255, 255, 255, 0.0);
        padding: 3rem 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        max-width: 700px;
        margin: 2rem auto;
        border: 2px solid rgba(255,255,255,0.2);
    }

    .title {
        text-align: center;
        color: #2c3e50;
        font-size: 39px;
        margin-bottom: 1rem;
        font-weight: 700;
    }

    .subtitle {
        text-align: center;
        color: white;
        font-size: 20px;
        margin-bottom: 2rem;
    }

    .success-message {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }

    .success-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }

    .footer {
        text-align: center;
        color: white;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ecf0f1;
    }

    /* Customização dos inputs */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 0.7px solid #359feb;
        padding: 18px;
        font-size: 1rem;
        height:15px;
    }

    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 0.7px solid #359feb;
        padding: 0.75rem;
        font-size: 1rem;
        min-height: 120px;
    }

    .stButton > button {
        background: green;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .reset-button {
        background: linear-gradient(45deg, #ff7b7b, #ff9a8b);
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


# Função para validar email
def validar_email(email):
    """Valida se o email tem formato correto"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Função para validar telefone
def validar_telefone(telefone):
    """Valida se o telefone tem formato básico correto"""
    # Remove espaços e caracteres especiais
    telefone_limpo = re.sub(r'[^\d]', '', telefone)
    # Verifica se tem entre 10 e 11 dígitos (formato brasileiro)
    return len(telefone_limpo) >= 10 and len(telefone_limpo) <= 15


# Função para enviar email
def enviar_email(nome, email, telefone, descricao):
    """Envia email com as informações do formulário"""
    try:
        # Configurações do email (use variáveis de ambiente em produção)
        remetente = os.getenv("EMAIL_SENDER")
        senha = os.getenv("EMAIL_PASSWORD")  # Considere usar st.secrets em produção
        destinatario =  os.getenv("EMAIL_RECEIVER")

        # Criar mensagem
        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = destinatario
        msg["Subject"] = f"Nova Solicitação de Automação - {nome}"

        # Corpo do email com melhor formatação
        corpo_email = f"""
        🤖 NOVA SOLICITAÇÃO DE AUTOMAÇÃO PYTHON
        ═══════════════════════════════════════════

        📍 DADOS DO CLIENTE:
        Nome: {nome}
        Email: {email}
        Telefone: {telefone}

        📋 DESCRIÇÃO DO PROJETO:
        {descricao}

        📅 Data da solicitação: {datetime.now().strftime("%d/%m/%Y às %H:%M")}

        ═══════════════════════════════════════════
        Enviado automaticamente pelo sistema de solicitações.
        """

        msg.attach(MIMEText(corpo_email, "plain", "utf-8"))

        # Enviar email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente, senha)
            server.send_message(msg)

        return True, "Email enviado com sucesso!"

    except smtplib.SMTPAuthenticationError:
        return False, "Erro de autenticação. Verifique as credenciais do email."
    except smtplib.SMTPException as e:
        return False, f"Erro SMTP: {str(e)}"
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


# Inicializar estados da sessão
if "form_enviado" not in st.session_state:
    st.session_state.form_enviado = False
if "mostrar_loading" not in st.session_state:
    st.session_state.mostrar_loading = False

# Interface principal
# st.markdown('<div class="main-container">', unsafe_allow_html=True)

if not st.session_state.form_enviado:
    # Cabeçalho
    st.markdown('<h1 class="title">🤖 Solicite sua Automação em Python</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Descreva o projeto que você tem em mente e entraremos em contato!</p>',
                unsafe_allow_html=True)

    # Formulário
    with st.form("formulario_automacao", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input(
                "👨‍🦱 Nome completo *",
                placeholder="Digite seu nome",
                help="Insira seu nome completo"
            )

        with col2:
            telefone = st.text_input(
                "📱 Telefone *",
                placeholder="(11) 99999-9999",
                help="Telefone com DDD"
            )

        email = st.text_input(
            "📧 Email *",
            placeholder="seu@email.com",
            help="Email válido para contato"
        )

        descricao = st.text_area(
            "📝 Descrição da Automação *",
            placeholder="Descreva detalhadamente o que você gostaria de automatizar...",
            help="Quanto mais detalhes, melhor poderemos ajudá-lo",
            height=150
        )

        # Checkbox de confirmação
        st.markdown("---")
        confirmar = st.checkbox(
            "✅ Confirmo que todas as informações estão corretas e autorizo o contato",
            help="Marque para confirmar os dados"
        )

        # Botão de envio
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            enviar = st.form_submit_button("🚀 Enviar Solicitação")

        # Validação e envio
        if enviar:
            st.session_state.mostrar_loading = True

            # Lista de erros
            erros = []

            # Validações
            if not nome.strip():
                erros.append("Nome é obrigatório")
            elif len(nome.strip()) < 2:
                erros.append("Nome deve ter pelo menos 2 caracteres")

            if not email.strip():
                erros.append("Email é obrigatório")
            elif not validar_email(email):
                erros.append("Email inválido")

            if not telefone.strip():
                erros.append("Telefone é obrigatório")
            elif not validar_telefone(telefone):
                erros.append("Telefone inválido")

            if not descricao.strip():
                erros.append("Descrição é obrigatória")
            elif len(descricao.strip()) < 20:
                erros.append("Descrição deve ter pelo menos 20 caracteres")

            if not confirmar:
                erros.append("Você deve confirmar as informações")

            # Se houver erros, exibir
            if erros:
                st.session_state.mostrar_loading = False
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Mostrar loading
                with st.spinner("Enviando solicitação..."):
                    time.sleep(1)  # Simular processamento

                    # Tentar enviar email
                    sucesso, mensagem = enviar_email(nome, email, telefone, descricao)

                    if sucesso:
                        st.session_state.form_enviado = True
                        st.success("✅ " + mensagem)
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ " + mensagem)
                        st.info("💡 Tente novamente em alguns minutos ou entre em contato diretamente.")

                st.session_state.mostrar_loading = False

else:
    # Tela de sucesso
    st.markdown("""
        <div class="success-message">
            <div class="success-icon">🎉</div>
            <h2>Solicitação Enviada com Sucesso!</h2>
            <p>Recebemos sua solicitação de automação e entraremos em contato em breve.</p>
            <p><strong>Próximos passos:</strong></p>
            <ul style="text-align: left; display: inline-block;">
                <li>Analisaremos sua solicitação</li>
                <li>Entraremos em contato em até 24 horas</li>
                <li>Faremos uma proposta personalizada</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Botão para nova solicitação
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📝 Nova Solicitação", key="nova_solicitacao"):
            # Reset do estado
            st.session_state.form_enviado = False
            st.session_state.mostrar_loading = False
            st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        💻 Desenvolvido para automações Python personalizadas<br>
        🔒 Suas informações são tratadas com total segurança
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)