import streamlit as st
import urllib.request, json
st.set_page_config(page_title="Mzigo AI — Biashara ya Kimataifa", page_icon="📦", layout="centered")
st.markdown("""<style>.stApp{background:#0a0c14;color:#e8edf5}
.mz-card{background:#0d1829;border:1px solid #1e3a6e;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#1565c0;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)
API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYS = "Wewe ni mshauri wa biashara ya kimataifa Kenya. Jibu kwa Kiswahili na Kiingereza. Eleza: ushuru wa forodha, nyaraka za kuagiza/kuuza nje, KEBS standards, COMESA, EAC trade."
def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body={"contents":[{"role":"user","parts":[{"text":q}]}],"systemInstruction":{"parts":[{"text":SYS}]},"generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"
st.markdown("# 📦 Mzigo AI"); st.markdown("**Biashara ya Kimataifa Kenya — Uagizaji na Usafirishaji**")
tab1,tab2,tab3=st.tabs(["📥 Kuagiza (Import)","📤 Kuuza Nje (Export)","🌍 Masoko ya EAC/COMESA"])
with tab1:
    item=st.text_input("Bidhaa unayotaka kuagiza:",placeholder="Mfano: Electronics kutoka China")
    origin=st.selectbox("Kutoka wapi:",["China","India","UAE","UK","USA","South Africa","Turkey"])
    value=st.number_input("Thamani (USD):",value=5000,step=500)
    if st.button("📥 Hesabu Forodha",key="m1") and item:
        with st.spinner("..."): r=ask(f"Kuagiza {item} kutoka {origin} Kenya, thamani USD {value:,}. Toa: Ushuru wa forodha (%), VAT, nyaraka (Bill of Lading, Invoice, KEBS inspection), wakala wa forodha, muda, jumla ya gharama za makadirio.")
        st.markdown(f'<div class="mz-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab2:
    export_item=st.text_input("Bidhaa unayotaka kuuza nje:",placeholder="Mfano: Chai, Mboga, Handicrafts")
    dest=st.selectbox("Kwenda wapi:",["UAE","UK","USA","Germany","China","Uganda","Tanzania","Ethiopia"])
    if st.button("📤 Mwongozo wa Usafirishaji",key="m2") and export_item:
        with st.spinner("..."): r=ask(f"Kuuza nje {export_item} kutoka Kenya kwenda {dest}. Toa: KEBS certification, EPC (Export Promotion Council), nyaraka, masoko, bei za kawaida, na jinsi ya kupata mnunuzi wa kwanza.")
        st.markdown(f'<div class="mz-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab3:
    if st.button("🌍 Faida za EAC na COMESA",key="m3"):
        with st.spinner("..."): r=ask("Faida za EAC (East African Community) na COMESA kwa biashara ndogo Kenya. Bidhaa gani zinaweza kusafirishwa bila ushuru? Jinsi ya kutumia Certificate of Origin.")
        st.markdown(f'<div class="mz-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
st.markdown("---"); st.caption("📦 Mzigo AI v1.0 | KRA Customs: kra.go.ke | EPC: epckenya.go.ke | KEBS: kebs.org | CC BY-NC-ND 4.0")
