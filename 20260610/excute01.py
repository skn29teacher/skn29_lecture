from dotenv import load_dotenv
load_dotenv(override=True)

pdf_path = r'doc\sample_paper.pdf'
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert(pdf_path)
doc = result.document

import fitz
import os
pdf = fitz.open(pdf_path)
output_dir = "extracted"
os.makedirs(output_dir, exist_ok=True)
def save_item_crop(item, item_type, idx):
    prov = item.prov[0]
    page = pdf[prov.page_no - 1]
    bbox = prov.bbox
    page_height = page.rect.height
    rect = fitz.Rect(
        bbox.l,
        page_height - bbox.t,
        bbox.r,
        page_height - bbox.b
    )

    pix = page.get_pixmap(
        matrix=fitz.Matrix(3,3),
        clip=rect
    )

    save_path = os.path.join(
        output_dir,
        f"{item_type}_{idx}.png"
    )

    pix.save(save_path)
    return save_path

records = []

figure_idx = 0
table_idx = 0
formula_idx = 0

for item, level in doc.iterate_items():
    item_type = type(item).__name__
    page_no = item.prov[0].page_no
    # Text
    if item_type == "TextItem":
        records.append({
            "type": "text",
            "page": page_no,
            "content": item.text
        })
    # Section
    elif item_type == "SectionHeaderItem":
        records.append({
            "type": "section",
            "page": page_no,
            "content": item.text
        })
    # Table
    elif item_type == "TableItem":
        image_path = save_item_crop(
            item,
            "table",
            table_idx
        )
        records.append({
            "type": "table",
            "page": page_no,
            "caption": item.caption_text(doc),
            "content": item.export_to_markdown(doc),
            "image_path": image_path
        })

        table_idx += 1

    # Figure
    elif item_type == "PictureItem":
        image_path = save_item_crop(
            item,
            "figure",
            figure_idx
        )
        records.append({
            "type": "figure",
            "page": page_no,
            "caption": item.caption_text(doc),
            "image_path": image_path
        })

        figure_idx += 1
    # Formula
    elif item_type == "FormulaItem":
        image_path = save_item_crop(
            item,
            "formula",
            formula_idx
        )

        records.append({
            "type": "formula",
            "page": page_no,
            "image_path": image_path
        })

        formula_idx += 1

from openai import OpenAI

client = OpenAI()

import base64

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(
            f.read()
        ).decode()
    
for record in records:
    if record["type"] not in ["figure","formula"]:
        continue

    image_b64 = encode_image(
        record["image_path"]
    )

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role":"user",
                "content":[
                    {
                        "type":"input_text",
                        "text":"Describe this figure for RAG retrieval."
                    },
                    {
                        "type":"input_image",
                        "image_url":f"data:image/png;base64,{image_b64}"
                    }
                ]
            }
        ]
    )

    record["description"] = (
        response.output_text
    )            