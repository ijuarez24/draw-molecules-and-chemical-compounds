# -*- coding: utf-8 -*-


# app.py
import io
import requests
from urllib.parse import quote_plus
import streamlit as st
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D


# 1) ChEMBL API 

def get_smiles_from_chembl(name: str):
    """Return SMILES from ChEMBL (or None if no match)."""
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule/search.json?q={quote_plus(name)}"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except requests.RequestException:
        return None

    try:
        data = r.json()
        hits = data.get("molecules") or []
        for h in hits:
            ms = h.get("molecule_structures") or {}
            smiles = ms.get("canonical_smiles")
            if smiles:
                return smiles
        return None
    except Exception:
        return None
    
    
    
    
# 2) SMILES to mol

def smiles_to_mol(smiles: str):
    """Convert a SMILES string to an RDKit Mol (or None on failure)."""
    if not smiles:
        return None
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    Chem.SanitizeMol(mol)
    AllChem.Compute2DCoords(mol)
    return mol





# 3) Gnerate image

def mol_to_png_bytes(mol, legend: str = "", size=(1200, 800)) -> bytes:
    """Draw Mol (transparent background, black atoms) and return PNG bytes."""
    if mol is None:
        return None
    w, h = size
    drawer = rdMolDraw2D.MolDraw2DCairo(w, h)
    opts = drawer.drawOptions()
    opts.clearBackground = False   # transparent background
    opts.useBWAtomPalette()        # black atoms
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol, legend)
    drawer.FinishDrawing()
    return drawer.GetDrawingText()  # PNG bytes


# 4) Streamlit UI 

st.set_page_config(page_title="Quickly draw molecules", page_icon="⌬", layout="centered")

st.markdown("""
<style>
/* ===== Light background ===== */
html, body, [data-testid="stAppViewContainer"] {
  background-color: #ffffff !important;
  color: #000000 !important;
}
/* ===== Inputs ===== */
.stTextInput input,
.stNumberInput input,
textarea {
  background: #ffffff !important;
  color: #000000 !important;
  border: 1px solid #d9d9d9 !important;
  font-size: 16px !important;
  height: 44px;
}

/* ===== Labels ===== */
.stTextInput label,
.stNumberInput label,
label[for] {
  font-size: 19px !important;   /* + */
  font-weight: 600 !important;
  color: #000000 !important;
}

/* Increase st.image caption size */
figure figcaption,
[data-testid="stCaptionContainer"] * {
  font-size: 16px !important;
  line-height: 1.4 !important;
  color: #000000 !important;
}

/* Readable placeholders */
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
textarea::placeholder {
  color: #6b7280 !important;
  opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)


st.title("⌬ Draw molecules and chemical compounds")
st.caption("Type a compound name, generate the image, and download it as PNG (transparent background).")


with st.form("search_form"):
    name = st.text_input("Compound name", placeholder="ibuprofen, paracetamol, ethanol...")
    col1, col2, col3 = st.columns(3)
    with col1:
        width = st.number_input("Width (px)", min_value=200, max_value=4000, value=1200, step=50)
    with col2:
        height = st.number_input("Height (px)", min_value=200, max_value=4000, value=800, step=50)
    with col3:
        legend = st.text_input("Caption (optional)", value="")
    submitted = st.form_submit_button("Generate image", type="primary")

if submitted:
    if not name.strip():
        st.error("Please type the molecule name you want to draw (in English).")
        st.stop()

    with st.spinner("Searching in ChEMBL and drawing…"):
        smiles = get_smiles_from_chembl(name.strip())
        if not smiles:
            st.error("The compound was not found in ChEMBL or there was a network problem.")
            st.stop()

        mol = smiles_to_mol(smiles)
        if mol is None:
            st.error("Invalid SMILES.")
            st.stop()

        png_bytes = mol_to_png_bytes(mol, legend=legend, size=(int(width), int(height)))
        if not png_bytes:
            st.error("The image could not be generated.")
            st.stop()

    st.success(f"Done! Found SMILES: `{smiles}`")
    st.image(io.BytesIO(png_bytes), caption=legend, use_container_width=True)

    default_filename = f"{name.strip()}.png"
    st.download_button(
        label="⬇️ Download image",
        data=png_bytes,
        file_name=default_filename,
        mime="image/png",
        type="primary"
    )


st.markdown("---", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center; font-size:16px; color:#000; padding-top:10px;">
      Built with 
      <a href="https://streamlit.io/" target="_blank"><strong>Streamlit</strong></a> · 
      <a href="https://www.rdkit.org/" target="_blank"><strong>RDKit</strong></a> · 
      <a href="https://www.ebi.ac.uk/chembl/" target="_blank"><strong>ChEMBL</strong></a>
    </div>
    <div style="text-align:center; font-size:16px; color:#000; padding-top:10px;">
      <strong>Inma Juárez Gonzálvez</strong><br/>
      <a href="https://www.linkedin.com/in/inmaculadajuarez/" target="_blank" style="margin-right:10px;">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="28" style="vertical-align:middle;"/>
      </a>
      <a href="https://github.com/ijuarez24" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="28" style="vertical-align:middle;"/>
      </a>
    </div>
    """,
    unsafe_allow_html=True
)
