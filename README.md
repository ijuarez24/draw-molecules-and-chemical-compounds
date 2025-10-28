# ⌬ Draw Molecules and Chemical Compounds App

This repository contains the source code for a simple yet powerful web application that allows users to **search, visualize, and download molecular structures** in PNG format with a **transparent background**.

The goal of this project is to provide an intuitive interface for chemists, students, and researchers to quickly obtain chemical structures by compound name — using public data from the **ChEMBL API** and rendering through **RDKit**.


## 🧪 Workflow Overview

1️⃣ **ChEMBL API** → Retrieves the compound’s SMILES from its name.  
2️⃣ **SMILES to Mol** → Converts the SMILES string into an RDKit molecular object.  
3️⃣ **Mol to Image** → Generates a high-quality PNG image using RDKit’s 2D drawer.  
4️⃣ **Streamlit Interface** → Provides a clean and responsive UI to interact with the model.  



## ⚙️ Technologies Used  

- **Python** (RDKit)  
- **Streamlit** (web interface)  
- **ChEMBL API** (molecular data source)  



## 📁 Project Structure

```

draw-molecules-and-chemical-compounds/
├──images
| ├── app_preview.png
├── app.py
├── environment.yml
├── requirements.txt
└── README.md

```

## 🖼️ App Preview

<p>
  <img src="https://raw.githubusercontent.com/ijuarez24/draw-molecules-and-chemical-compounds/main/images/app_preview.png" width="400" alt="App screenshot">
</p>



## 🌐 Live Demo

👉 [Open the app on Streamlit Cloud](https://draw-molecules.streamlit.app)


## 👩‍💻 Contact

- [LinkedIn Profile](https://www.linkedin.com/in/inmaculadajuarez)
- [Email](mailto:inma.juarez24@gmail.com)  






