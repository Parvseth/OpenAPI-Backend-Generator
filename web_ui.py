import os
import io
import shutil
import zipfile
import tempfile
import yaml
import json
import streamlit as st

from parser.openapi_parser import parse_openapi_spec
from codegen.engine import generate_clean_backend

st.set_page_config(
    page_title="OpenAPI Backend Generator",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Enterprise OpenAPI Backend Generator")
st.caption("Convert any OpenAPI v3.1 specification into a production-ready, 3-tier FastAPI + PostgreSQL backend in seconds.")

st.sidebar.header("⚙️ Configuration")
use_ai = st.sidebar.toggle("Enable AI Service Logic (Groq)", value=True)
selected_db = st.sidebar.selectbox("Target Database", ["PostgreSQL (Docker)", "SQLite (Local)"])

uploaded_file = st.file_uploader("Upload OpenAPI Spec (YAML or JSON)", type=["yaml", "yml", "json"])

if uploaded_file is not None:
    try:
        content_bytes = uploaded_file.read()
        filename = uploaded_file.name
        
        if filename.endswith(".json"):
            spec_dict = json.loads(content_bytes.decode("utf-8"))
        else:
            spec_dict = yaml.safe_load(content_bytes.decode("utf-8"))

        ir_spec = parse_openapi_spec(spec_dict)

        st.success(f"Parsed Spec: **{ir_spec.title}** (v{ir_spec.version})")

        # Layout Columns for Preview
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"📦 Data Models ({len(ir_spec.models)})")
            for model in ir_spec.models:
                with st.expander(f"Model: {model.name} (table: `{model.table_name}`)"):
                    for field in model.fields:
                        st.write(f"- `{field.name}`: **{field.pydantic_type}** ({field.sqlalchemy_type}) {'[PK]' if field.is_primary_key else ''}")

        with col2:
            st.subheader(f"🌐 API Endpoints ({len(ir_spec.routes)})")
            for route in ir_spec.routes:
                st.write(f"`{route.method}` **{route.path}** → `{route.operation_id}`")

        st.divider()

        if st.button("🚀 Generate Backend Project (ZIP)", type="primary"):
            with st.spinner("Generating Clean Architecture code & scaffolding DevOps files..."):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    out_path = os.path.join(tmp_dir, "generated_backend")
                    generate_clean_backend(ir_spec, out_path, use_ai=use_ai)

                    # Create ZIP in memory
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                        for root, _, files in os.walk(out_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                archive_name = os.path.relpath(file_path, out_path)
                                zip_file.write(file_path, archive_name)

                    zip_buffer.seek(0)

                    st.balloons()
                    st.success("Backend generation complete!")

                    st.download_button(
                        label="📦 Download Backend (ZIP)",
                        data=zip_buffer,
                        file_name=f"{ir_spec.title.lower().replace(' ', '_')}_backend.zip",
                        mime="application/zip"
                    )

    except Exception as e:
        st.error(f"Error parsing OpenAPI spec: {e}")
else:
    st.info("💡 Please upload an OpenAPI v3 spec (`.yaml` or `.json`) to get started.")
