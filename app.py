"""
Site imersivo — Rayssa Siviero | Maquiadora Tatuapé/Carrão
Rode com:  streamlit run app.py
Estrutura da pasta: app.py, template.html, assets/rayssa.jpg, requirements.txt
"""
import base64
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

BASE = Path(__file__).parent

try:
    from photo_data import PHOTO_B64, PHOTO_SOBRE_B64, LOOKS_B64
except ImportError:
    PHOTO_B64 = PHOTO_SOBRE_B64 = ""
    LOOKS_B64 = []

# ═════════════════════ CONFIGURAÇÃO — edite tudo por aqui ═════════════════════
CONFIG = {
    "nome": "Rayssa Siviero",
    "cidade": "Tatuapé/Carrão",
    "instagram": "rayssasivieromakeup",
    "studio": "_studiorsbeauty",
    "bio": "https://bio.site/studiorayssasiviero",
    # WhatsApp com DDI+DDD, só números. Ex.: "5511999999999". Vazio = abre o direct do Instagram.
    "whatsapp": "",
    "especialidades": ["noivas", "madrinhas", "formaturas", "eventos", "pele de verdade"],
    "sobre": (
        "Rayssa é maquiadora no Tatuapé/Carrão, em São Paulo, e criadora de conteúdo digital. "
        "Em 8 anos de carreira passou de 5.000 atendimentos e reuniu 16,8 mil pessoas no Instagram "
        "falando de beauty, lifestyle e empreendedorismo. Também é CEO do @_studiorsbeauty."
    ),
    "foco": {
        "Maquiagem": "Técnica, produtos e passo a passo para pele, olhos e boca, do dia a dia ao grande evento.",
        "Lifestyle": "Bastidores da rotina, autocuidado e as escolhas que sustentam uma imagem que combina com você.",
        "Empreendedorismo": "A trajetória de transformar talento em negócio: atendimento, marca e crescimento.",
    },
    "stats": [
        {"v": 8, "l": "anos de carreira"},
        {"v": 5000, "pre": "+", "l": "atendimentos"},
        {"v": 16.8, "dec": 1, "suf": " mil", "l": "seguidores"},
        {"v": 870, "l": "posts"},
    ],
    # ── Serviços (EXEMPLOS: troque pelos reais) ──
    "servicos": [
        {"nome": "Maquiagem social", "desc": "Pele luminosa e acabamento elegante para jantares e eventos.",
         "inclui": ["Preparo de pele", "Maquiagem completa", "Cílios (opcional)", "Fixação para a noite toda"]},
        {"nome": "Noivas", "desc": "Teste e dia do casamento, pensados para durar cerimônia e festa.",
         "inclui": ["Teste de make", "Maquiagem no grande dia", "Kit de retoque", "Fixação máxima"]},
        {"nome": "Madrinhas e convidadas", "desc": "Looks que combinam com o vestido e com a história do evento.",
         "inclui": ["Consultoria de cor", "Maquiagem completa", "Atendimento em grupo"]},
        {"nome": "Formatura", "desc": "Produção resistente a fotos, luz forte e muitas horas de festa.",
         "inclui": ["Preparo de pele", "Make à prova de flash", "Fixação reforçada"]},
        {"nome": "Automaquiagem (aula)", "desc": "Aprenda a fazer a sua própria make, do preparo ao delineado.",
         "inclui": ["Análise de pele", "Passo a passo prático", "Lista de produtos"]},
        {"nome": "Ensaio e conteúdo", "desc": "Make pensada para câmera, com foco em pele real.",
         "inclui": ["Make para fotos e vídeo", "Ajustes de brilho", "Retoque durante o ensaio"]},
    ],
    # ── Escolha seu look (paleta de cada estilo) ──
    "lab": [
        {"n": "Natural", "cor": "#E8C9B5",
         "desc": "Pele uniforme e viço natural, com tudo no lugar e quase nada à vista.",
         "itens": [{"k": "Pele", "n": "Skin tint", "c": "#E8B998"}, {"k": "Sombra", "n": "Nude", "c": "#D9B7A4"},
                   {"k": "Blush", "n": "Pêssego", "c": "#F0A88C"}, {"k": "Batom", "n": "Nude", "c": "#C9877A"}]},
        {"n": "Noiva", "cor": "#D9A5A0",
         "desc": "Romântico e luminoso, pensado para durar cerimônia e festa.",
         "itens": [{"k": "Pele", "n": "Glow radiante", "c": "#F1D5C3"}, {"k": "Sombra", "n": "Champagne", "c": "#D8B98A"},
                   {"k": "Blush", "n": "Rosé", "c": "#E59A9A"}, {"k": "Batom", "n": "Rosa", "c": "#D4707F"}]},
        {"n": "Festa", "cor": "#8E2F3B",
         "desc": "Pele matte sofisticada, olhar esfumado e boca marcante para a noite.",
         "itens": [{"k": "Pele", "n": "Matte", "c": "#D29A74"}, {"k": "Sombra", "n": "Marrom esfumado", "c": "#7A4A3C"},
                   {"k": "Blush", "n": "Coral", "c": "#E5806F"}, {"k": "Batom", "n": "Vinho", "c": "#8E2F3B"}]},
        {"n": "Glam dourado", "cor": "#C8A27A",
         "desc": "Olhos dourados com delineado gráfico e iluminador marcado.",
         "itens": [{"k": "Pele", "n": "Glow", "c": "#F3D3BF"}, {"k": "Sombra", "n": "Dourada", "c": "#C8A27A"},
                   {"k": "Blush", "n": "Terracota", "c": "#C2705A"}, {"k": "Batom", "n": "Bege", "c": "#B98A78"}]},
    ],
    # ── Lookbook (cada look pode ganhar uma foto real depois) ──
    "looks": [
        {"nome": "Noiva rosé", "cat": "Noiva", "tags": ["suave", "evento", "casamento"],
         "cores": ["#E8C9B5", "#D9A5A0", "#C98E7F"], "grad": "linear-gradient(135deg,#E8C9B5,#D9A5A0 60%,#C98E7F)",
         "desc": "Pele luminosa, sombra champagne e lábio rosado. Romântico e atemporal.",
         "itens": ["Pele radiante", "Sombra champagne", "Blush rosé", "Gloss nude"]},
        {"nome": "Glam dourado", "cat": "Festa", "tags": ["marcante", "evento", "glow"],
         "cores": ["#C8A27A", "#8A5A3A", "#3B231F"], "grad": "linear-gradient(135deg,#E2C28F,#A9784B 55%,#3B231F)",
         "desc": "Olhos dourados com delineado gráfico. Para quem quer ser vista.",
         "itens": ["Esfumado dourado", "Delineado gráfico", "Iluminador marcado", "Batom nude rosado"]},
        {"nome": "Vinho de festa", "cat": "Festa", "tags": ["marcante", "matte", "evento"],
         "cores": ["#8E2F3B", "#5A1F2A", "#2A1613"], "grad": "linear-gradient(135deg,#B5485A,#7A2634 55%,#2A1613)",
         "desc": "Boca vinho e pele matte sofisticada para a noite.",
         "itens": ["Pele matte", "Batom vinho", "Olhos esfumados em marrom", "Cílios definidos"]},
        {"nome": "Pele de verdade", "cat": "Dia a dia", "tags": ["suave", "natural", "glow"],
         "cores": ["#F1D5C3", "#E8B998", "#D9A5A0"], "grad": "linear-gradient(135deg,#F6E3D6,#E8C1A5 60%,#D9A5A0)",
         "desc": "Quase nada, mas com tudo no lugar: pele uniforme e viço natural.",
         "itens": ["Skin tint", "Corretivo pontual", "Blush cremoso", "Gloss"]},
        {"nome": "Madrinha elegante", "cat": "Noiva", "tags": ["media", "evento", "casamento"],
         "cores": ["#C78A98", "#E9CDBF", "#7A4A3C"], "grad": "linear-gradient(135deg,#E9CDBF,#C78A98 60%,#7A4A3C)",
         "desc": "Esfumado suave em malva e marrom, com fixação para o dia inteiro.",
         "itens": ["Olhos malva", "Delineado fino", "Blush malva", "Batom rosa"]},
        {"nome": "Câmera e conteúdo", "cat": "Dia a dia", "tags": ["media", "glow", "natural"],
         "cores": ["#D8B98A", "#E59A9A", "#6E4125"], "grad": "linear-gradient(135deg,#F0DDC3,#D9A57F 55%,#6E4125)",
         "desc": "Make pensada para luz e lente: pele real, olhar definido, sem excesso de brilho.",
         "itens": ["Base leve com cobertura média", "Olhar definido", "Pó translúcido", "Batom hidratante"]},
    ],
    "quiz": [
        {"p": "Para qual ocasião é a make?", "o": [
            {"t": "Casamento ou madrinha", "v": ["casamento"]},
            {"t": "Festa ou formatura", "v": ["evento"]},
            {"t": "Dia a dia e trabalho", "v": ["natural"]},
            {"t": "Fotos e redes sociais", "v": ["glow"]}]},
        {"p": "Qual acabamento de pele você prefere?", "o": [
            {"t": "Luminoso, com glow", "v": ["glow"]},
            {"t": "Matte sofisticado", "v": ["matte"]},
            {"t": "Natural, quase sem make", "v": ["natural"]},
            {"t": "Uniforme e discreto", "v": ["suave"]}]},
        {"p": "Quanto você quer chamar atenção?", "o": [
            {"t": "Quase nada, só realçar", "v": ["suave", "natural"]},
            {"t": "Na medida certa", "v": ["media"]},
            {"t": "Quero que olhem", "v": ["marcante"]},
            {"t": "Surpreenda-me", "v": ["marcante", "evento"]}]},
    ],
    "processo": [
        {"t": "Conversa inicial", "d": "Você conta a ocasião, o vestido e a referência que gosta. É aqui que a make começa a ser desenhada."},
        {"t": "Preparo da pele", "d": "Hidratação e preparo, para que a make assente bem e dure mais."},
        {"t": "Maquiagem", "d": "Execução do look escolhido, ajustando cor e intensidade ao seu tom de pele e ao seu estilo."},
        {"t": "Fixação e retoque", "d": "Finalização pensada para a duração do evento, com orientações para retoques."},
    ],
    # ── Depoimentos (EXEMPLOS: substitua por depoimentos reais) ──
    "depoimentos": [
        {"t": "Cliente satisfeita: escreva aqui um depoimento real.", "a": "Cliente · Noiva"},
        {"t": "Outro depoimento real entra aqui.", "a": "Cliente · Formatura"},
        {"t": "Mais um depoimento de cliente.", "a": "Cliente · Madrinha"},
    ],
    "faq": [
        {"q": "Preciso fazer teste de make antes do casamento?", "a": "É o mais indicado. No teste você define o look e o grande dia fica sem surpresas."},
        {"q": "Quanto tempo antes devo agendar?", "a": "Para datas concorridas, como sábados e épocas de formatura, agende com antecedência. A Rayssa confirma a agenda na conversa."},
        {"q": "A maquiagem dura a festa toda?", "a": "Com preparo de pele e fixação adequados à ocasião, sim. Você pode testar combinações no laboratório do site."},
        {"q": "Atende em domicílio?", "a": "O agendamento tem a opção de atendimento em domicílio. Valores e disponibilidade são combinados na conversa."},
        {"q": "Onde vejo trabalhos anteriores?", "a": "No Instagram @rayssasivieromakeup, com mais de 870 publicações."},
    ],
}
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Rayssa Siviero • Maquiadora Tatuapé/Carrão", page_icon="💄",
                   layout="wide", initial_sidebar_state="collapsed")

# Deixa o site ocupar a tela inteira e esconde a interface do Streamlit
st.markdown(
    """
<style>
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
.stApp { background: #2A1613; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] > .main { padding: 0 !important; }
[data-testid="stVerticalBlock"] { gap: 0 !important; }
[data-testid="stElementContainer"], [data-testid="stCustomComponentV1"] { width: 100% !important; }
iframe { width: 100% !important; height: 100vh !important; min-height: 100vh !important; border: 0; display: block; }
</style>
""",
    unsafe_allow_html=True,
)


def montar_html() -> str:
    foto = BASE / "assets" / "rayssa.jpg"
    b64 = PHOTO_B64 or (base64.b64encode(foto.read_bytes()).decode() if foto.exists() else "")
    foto2 = BASE / "assets" / "rayssa_sobre.jpg"
    sobre = PHOTO_SOBRE_B64 or (base64.b64encode(foto2.read_bytes()).decode() if foto2.exists() else b64)
    cfg = json.loads(json.dumps(CONFIG))
    for i, look in enumerate(cfg["looks"]):
        arq = BASE / "assets" / "looks" / f"look{i + 1}.jpg"
        if i < len(LOOKS_B64) and LOOKS_B64[i]:
            look["img"] = "data:image/jpeg;base64," + LOOKS_B64[i]
        elif arq.exists():
            look["img"] = "data:image/jpeg;base64," + base64.b64encode(arq.read_bytes()).decode()
    html = (BASE / "template.html").read_text(encoding="utf-8")
    return (
        html.replace("__PHOTO_SOBRE_B64__", sobre)
        .replace("__PHOTO_B64__", b64)
        .replace("__CONFIG_JSON__", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    )


components.html(montar_html(), height=900, scrolling=True)
