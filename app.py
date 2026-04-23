import streamlit as st
import yfinance as yf
import pandas as pd
import feedparser
from datetime import datetime

# Konfigurasi UI Profesional
st.set_page_config(page_title="AI Market Intelligence Pro", layout="wide", page_icon="🏦")

# --- DATABASE & ENGINE ---
def get_safe_data(ticker):
    try:
        t = yf.Ticker(ticker)
        df = t.history(period="1y")
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        return t, df
    except: return None, None

def get_detailed_news():
    # Menarik berita dari beberapa sumber sekaligus
    feeds = ["https://www.cnbcindonesia.com/market/rss", "https://www.kontan.co.id/rss/investasi"]
    combined_news = []
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:3]:
                if hasattr(entry, 'title'):
                    combined_news.append(entry.title)
        except: continue
    return combined_news

# --- DAFTAR 50 SAHAM ---
SEKTOR_WATCHLIST = {
    "Perbankan": ["BBCA.JK", "BBRI.JK", "BMRI.JK", "BBNI.JK", "BRIS.JK", "ARTO.JK", "BBTN.JK", "BDMN.JK", "PNBN.JK", "BJBR.JK"],
    "Energi": ["ADRO.JK", "ITMG.JK", "PTBA.JK", "MEDC.JK", "AKRA.JK", "HRUM.JK", "INDY.JK", "PGAS.JK", "ENRG.JK", "ELSA.JK"],
    "Infrastruktur/BUMN": ["TLKM.JK", "ISAT.JK", "EXCL.JK", "JSMR.JK", "BREN.JK", "TOWR.JK", "TBIG.JK", "PGEO.JK", "META.JK", "WIKA.JK"],
    "Consumer/Health": ["UNVR.JK", "ICBP.JK", "INDF.JK", "MYOR.JK", "AMRT.JK", "KLBF.JK", "MIKA.JK", "HEAL.JK", "ACES.JK", "ERAA.JK"],
    "Mining/Industrial": ["ASII.JK", "UNTR.JK", "ANTM.JK", "INCO.JK", "TINS.JK", "MDKA.JK", "MBMA.JK", "NCKL.JK", "SMGR.JK", "INTP.JK"]
}

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Analyst Hub")
    menu = st.radio("Menu Strategis:", ["🔍 Intelligence Report", "📊 Sectoral Matrix", "🧬 Stock DNA Pro"])
    st.markdown("---")
    st.write("**Land Context:** 18x28m Plot Development.")
    st.caption(f"Sync: {datetime.now().strftime('%H:%M:%S')}")

# --- MENU 1: INTELLIGENCE REPORT (NARRATIVE VERSION) ---
if menu == "🔍 Intelligence Report":
    st.header("🌍 Strategic Market Intelligence")
    st.subheader("📝 Deep Daily Market Synthesis")
    
    news_titles = get_detailed_news()
    main_news = news_titles[0] if news_titles else "Sentimen Suku Bunga Global"

    # NARASI DETAIL & PANJANG
    st.markdown(f"""
    <div style="background-color: #1e293b; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6;">
        <h4 style="margin-top:0;">🌐 Analisis Komprehensif Berita Global & Nasional</h4>
        <p>Pasar keuangan saat ini tengah berada dalam fase <b>'Wait and See'</b> yang krusial. Fokus utama investor global tertuju pada pergerakan yield obligasi AS yang kembali fluktuatif, memicu kekhawatiran akan terjadinya <i>capital outflow</i> dari pasar saham negara berkembang (Emerging Markets).</p>
        <p><b>Dinamika Berita Terkini:</b> Berita utama mengenai <i>"{main_news}"</i> memberikan sinyal kuat bahwa volatilitas di sektor berbasis komoditas dan teknologi mungkin akan meningkat dalam beberapa sesi ke depan. Adanya sentimen ini mengharuskan investor untuk lebih selektif dalam memilih emiten dengan profil utang yang rendah.</p>
        <p><b>Perspektif Nasional:</b> Di dalam negeri, indeks IHSG sedang mencoba mempertahankan level psikologisnya. Arus dana asing terpantau masih masuk secara selektif (selective buying) pada saham-saham perbankan berkapitalisasi besar, yang dianggap sebagai <i>safe haven</i> di tengah ketidakpastian makro. Namun, sektor retail dan properti perlu dicermati lebih lanjut karena daya beli masyarakat yang mulai tertekan oleh inflasi pangan.</p>
        <p><b>Kesimpulan Strategis:</b> Manfaatkan momentum koreksi sehat untuk melakukan akumulasi bertahap pada sektor perbankan dan energi, sembari tetap menjaga level <i>cash</i> yang cukup untuk menghadapi potensi volatilitas mendadak akibat rilis data ekonomi AS pekan ini.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🔥 Sector Impact Matrix")
        st.success("**BULLISH (+)**\n- **Banking:** Profitabilitas terjaga (NIM Tinggi) & pertumbuhan kredit stabil.\n- **Energy:** Outlook harga batubara tetap solid didorong permintaan musiman.")
        st.error("**BEARISH (-)**\n- **Tech/Property:** Sensitif terhadap kenaikan suku bunga & pelemahan daya beli menengah.")
    with c2:
        st.subheader("📋 MSCI Rebalancing Tracker")
        st.markdown("""
        **IN (Potensial/Aktif):**
        - **AMMN:** Dominasi Market Cap di sektor tambang tembaga.
        - **BREN:** Playmaker utama di sektor energi terbarukan global.
        
        **OUT (Potensial/Aktif):**
        - **UNVR:** Penurunan volume konsumsi dan tekanan pada margin laba.
        - **INCO:** Sentimen harga nikel global yang masih cenderung <i>sideways</i>.
        """)

# --- MENU 2 & 3 TETAP STABIL ---
elif menu == "📊 Sectoral Matrix":
    st.header("📊 Sectoral Health Matrix Scan")
    for sektor, tickers in SEKTOR_WATCHLIST.items():
        with st.expander(f"📂 Analisa Detail {sektor}", expanded=True):
            rows = []
            for t in tickers:
                try:
                    data = yf.download(t, period="6mo", progress=False)
                    if data.empty: continue
                    if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.get_level_values(0)
                    price = data['Close'].iloc[-1]
                    ma20 = data['Close'].rolling(20).mean().iloc[-1]
                    ma50 = data['Close'].rolling(50).mean().iloc[-1]
                    status = "Strong Bullish 🔥" if price > ma20 and price > ma50 else ("Bearish 🔻" if price < ma50 else "Neutral ⚖️")
                    rows.append({"Ticker": t, "Price": f"{price:,.0f}", "MA20": f"{ma20:,.0f}", "MA50": f"{ma50:,.0f}", "Trend": status})
                except: continue
            st.table(pd.DataFrame(rows))

elif menu == "🧬 Stock DNA Pro":
    st.header("🧬 Stock DNA: Fundamental & Technical Deep-Dive")
    target = st.text_input("Ketik Kode Saham (e.g. BBCA.JK):", "BBCA.JK").upper()
    ticker_obj, df = get_safe_data(target)
    if ticker_obj and not df.empty:
        info = ticker_obj.info
        m1, m2, m3, m4 = st.columns(4)
        curr = info.get('currentPrice', 0)
        target_p = info.get('targetMeanPrice', 0)
        upside = ((target_p - curr)/curr)*100 if target_p and curr else 0
        m1.metric("Current Price", f"Rp {curr:,.0f}")
        m2.metric("Analyst Target", f"Rp {target_p:,.0f}", f"{upside:.2f}% Upside")
        m3.metric("P/E Ratio", f"{info.get('trailingPE', 0):.2f}x")
        m4.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%")
        st.markdown("---")
        col_left, col_right = st.columns([1, 1])
        with col_left:
            st.subheader("📊 Fundamental Scorecard")
            pe = info.get('trailingPE', 20)
            if pe < 15: st.success("✅ **VALUATION:** Undervalued")
            elif pe < 25: st.warning("⚖️ **VALUATION:** Fair Value")
            else: st.error("❌ **VALUATION:** Overvalued")
            st.write(f"**ROE:** {info.get('returnOnEquity', 0)*100:.2f}% | **Market Cap:** Rp {info.get('marketCap', 0):,.0f}")
        with col_right:
            st.subheader("📈 Technical Momentum")
            df['MA20'] = df['Close'].rolling(20).mean()
            df['MA50'] = df['Close'].rolling(50).mean()
            last_close, last_ma50 = df['Close'].iloc[-1], df['MA50'].iloc[-1]
            if last_close > last_ma50: st.success("🔥 **TREND:** Strong Uptrend")
            else: st.error("🔻 **TREND:** Bearish / Correction")
            st.line_chart(df[['Close', 'MA20', 'MA50']])