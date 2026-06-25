import os
import json
import base64
import fitz
import chromadb

from docling.document_converter import DocumentConverter
from openai import OpenAI
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from dotenv import load_dotenv
load_dotenv(override=True)

# ============================================================
# CONFIG
# ============================================================

PDF_PATH = r"doc\sample_paper.pdf"

CHROMA_PATH = "./chroma_db"
COLLECTION_NAME = "paper_rag"

EXTRACT_DIR = "./extracted"

EMBEDDING_MODEL = "text-embedding-3-large"
LLM_MODEL = "gpt-5-nano"

os.makedirs(EXTRACT_DIR, exist_ok=True)

client = OpenAI()


# ============================================================
# IMAGE UTILS
# ============================================================

def encode_image(image_path):

    with open(image_path, "rb") as f:
        return base64.b64encode(
            f.read()
        ).decode()


# ============================================================
# PDF CROP
# ============================================================

pdf_doc = fitz.open(PDF_PATH)

def save_item_crop(item, item_type, idx):
    prov = item.prov[0]
    page = pdf_doc[prov.page_no - 1]
    bbox = prov.bbox
    page_height = page.rect.height
    rect = fitz.Rect(
        bbox.l,
        page_height - bbox.t,
        bbox.r,
        page_height - bbox.b
    )

    pix = page.get_pixmap(
        matrix=fitz.Matrix(3, 3),
        clip=rect
    )

    save_path = os.path.join(
        EXTRACT_DIR,
        f"{item_type}_{idx}.png"
    )

    pix.save(save_path)
    return save_path


# ============================================================
# IMAGE DESCRIPTION
# ============================================================

def describe_image(image_path, prompt):
    image_b64 = encode_image(image_path)
    response = client.responses.create(
        model=LLM_MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{image_b64}"
                    }
                ]
            }
        ]
    )

    return response.output_text


# ============================================================
# DOCLING PARSE
# ============================================================

converter = DocumentConverter()
result = converter.convert(PDF_PATH)
doc = result.document


# ============================================================
# EXTRACT RECORDS
# ============================================================

records = []

figure_idx = 0
table_idx = 0
formula_idx = 0

for item, level in doc.iterate_items():
    item_type = type(item).__name__
    if not item.prov:
        continue

    page_no = item.prov[0].page_no

    # --------------------------------------------------------
    # SECTION
    # --------------------------------------------------------

    if item_type == "SectionHeaderItem":

        records.append({
            "type": "section",
            "page": page_no,
            "content": item.text
        })

    # --------------------------------------------------------
    # TEXT
    # --------------------------------------------------------

    elif item_type == "TextItem":
        text = item.text.strip()

        if text:
            records.append({
                "type": "text",
                "page": page_no,
                "content": text
            })

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    elif item_type == "TableItem":
        image_path = save_item_crop(
            item,
            "table",
            table_idx
        )

        markdown = item.export_to_markdown(doc)
        caption = item.caption_text(doc)
        table_description = describe_image(
            image_path,
            """
            Explain this table in detail.
            Describe important values and findings.
            """
        )

        records.append({
            "type": "table",
            "page": page_no,
            "caption": caption,
            "content": markdown,
            "description": table_description,
            "image_path": image_path
        })

        table_idx += 1

    # --------------------------------------------------------
    # FIGURE
    # --------------------------------------------------------

    elif item_type == "PictureItem":
        image_path = save_item_crop(
            item,
            "figure",
            figure_idx
        )

        caption = item.caption_text(doc)
        figure_description = describe_image(
            image_path,
            """
            Analyze this scientific figure.

            Extract:
            - architecture names
            - model names
            - encoder
            - decoder
            - attention
            - multi-head attention
            - feed forward network
            - transformer components
            - data flow
            - arrows and connections

            Write a detailed retrieval-friendly description.
            """
        )

        records.append({
            "type": "figure",
            "page": page_no,
            "caption": caption,
            "description": figure_description,
            "image_path": image_path
        })

        figure_idx += 1

    # --------------------------------------------------------
    # FORMULA
    # --------------------------------------------------------

    elif item_type == "FormulaItem":
        image_path = save_item_crop(
            item,
            "formula",
            formula_idx
        )

        formula_description = describe_image(
            image_path,
            """
            Convert this formula into text.

            Extract:
            - mathematical expression
            - variable names
            - symbol meanings
            - purpose of the equation

            Write a retrieval-friendly explanation.
            """
        )

        records.append({
            "type": "formula",
            "page": page_no,
            "description": formula_description,
            "image_path": image_path
        })

        formula_idx += 1


# ============================================================
# SAVE RECORDS
# ============================================================

with open(
    "records.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        records,
        f,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# CHROMADB
# ============================================================

embedding_function = OpenAIEmbeddingFunction(
    api_key=os.environ["OPENAI_API_KEY"],
    model_name=EMBEDDING_MODEL
)

db = chromadb.PersistentClient(
    path=CHROMA_PATH
)

try:
    db.delete_collection(COLLECTION_NAME)
except:
    pass

collection = db.create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


# ============================================================
# VECTOR INDEX
# ============================================================

documents = []
metadatas = []
ids = []

for idx, rec in enumerate(records):

    if rec["type"] == "section":
        document = rec["content"]
    elif rec["type"] == "text":
        document = rec["content"]
    elif rec["type"] == "table":
        document = f"""
        {rec.get('caption','')}
        {rec.get('content','')}
        {rec.get('description','')}
        """

    elif rec["type"] == "figure":
        document = f"""
        {rec.get('caption','')}
        {rec.get('description','')}
        """

    elif rec["type"] == "formula":
        document = rec.get(
            "description",
            ""
        )

    documents.append(document)
    metadatas.append({
        "page": rec["page"],
        "record_idx": idx,
        "type": rec["type"]
    })

    ids.append(f"doc_{idx}")

collection.add(
    ids=ids,
    documents=documents,
    metadatas=metadatas
)


# ============================================================
# PAGE INDEX
# ============================================================

page_index = {}

for rec in records:
    page = rec["page"]
    if page not in page_index:
        page_index[page] = []

    page_index[page].append(rec)


# ============================================================
# RAG
# ============================================================

def ask_rag(question):

    # --------------------------------------------------
    # 1. Vector Search
    # --------------------------------------------------
    result = collection.query(
        query_texts=[question],
        n_results=20
    )

    # --------------------------------------------------
    # 2. 검색 페이지 + 인접 페이지 확장
    # --------------------------------------------------
    expanded_pages = set()

    for meta in result["metadatas"][0]:

        page = meta["page"]

        expanded_pages.add(page - 1)
        expanded_pages.add(page)
        expanded_pages.add(page + 1)

    expanded_pages = {
        p for p in expanded_pages
        if p > 0
    }

    # --------------------------------------------------
    # 3. 페이지 전체 객체 수집
    # --------------------------------------------------
    related_records = []

    for page in sorted(expanded_pages):

        if page not in page_index:
            continue

        related_records.extend(
            page_index[page]
        )

    # --------------------------------------------------
    # 4. Context 생성
    # --------------------------------------------------
    context_parts = []

    figure_images = []
    formula_images = []
    table_images = []

    for rec in related_records:

        rec_type = rec["type"]

        if rec_type == "section":

            context_parts.append(
                f"""
[SECTION]
{rec['content']}
"""
            )

        elif rec_type == "text":

            context_parts.append(
                f"""
[TEXT]
{rec['content']}
"""
            )

        elif rec_type == "table":

            context_parts.append(
                f"""
[TABLE]

Page:
{rec['page']}

Caption:
{rec.get('caption','')}

Markdown:
{rec.get('content','')}

Description:
{rec.get('description','')}
"""
            )

            if rec.get("image_path"):
                table_images.append(
                    rec["image_path"]
                )

        elif rec_type == "figure":

            context_parts.append(
                f"""
[FIGURE]

Page:
{rec['page']}

Caption:
{rec.get('caption','')}

Description:
{rec.get('description','')}
"""
            )

            if rec.get("image_path"):
                figure_images.append(
                    rec["image_path"]
                )

        elif rec_type == "formula":

            context_parts.append(
                f"""
[FORMULA]

Page:
{rec['page']}

Description:
{rec.get('description','')}
"""
            )

            if rec.get("image_path"):
                formula_images.append(
                    rec["image_path"]
                )

    # --------------------------------------------------
    # 5. Context 길이 제한
    # --------------------------------------------------
    context = "\n\n".join(context_parts)

    MAX_CONTEXT_CHARS = 30000

    context = context[:MAX_CONTEXT_CHARS]

    # --------------------------------------------------
    # 6. 이미지 선별
    # --------------------------------------------------
    figure_images = figure_images[:5]
    formula_images = formula_images[:5]
    table_images = table_images[:3]

    # --------------------------------------------------
    # 7. GPT 입력
    # --------------------------------------------------
    content = [
        {
            "type": "input_text",
            "text": f"""
You are answering questions about a scientific paper.

The context contains:
- section headers
- paragraphs
- figures
- tables
- formulas

IMPORTANT:

1. Use figure descriptions.
2. Use table contents.
3. Use formula descriptions.
4. If figures are relevant, explicitly mention them.
5. If tables are relevant, explicitly mention them.
6. If formulas are relevant, explain them.
7. Prefer information from figures/tables over plain text when available.

Question:
{question}

Context:
{context}
"""
        }
    ]

    # --------------------------------------------------
    # 8. Figure 이미지 추가
    # --------------------------------------------------
    for image_path in figure_images:

        content.append(
            {
                "type": "input_image",
                "image_url":
                f"data:image/png;base64,{encode_image(image_path)}"
            }
        )

    # --------------------------------------------------
    # 9. Formula 이미지 추가
    # --------------------------------------------------
    for image_path in formula_images:

        content.append(
            {
                "type": "input_image",
                "image_url":
                f"data:image/png;base64,{encode_image(image_path)}"
            }
        )

    # --------------------------------------------------
    # 10. Table 이미지 추가
    # --------------------------------------------------
    for image_path in table_images:

        content.append(
            {
                "type": "input_image",
                "image_url":
                f"data:image/png;base64,{encode_image(image_path)}"
            }
        )

    # --------------------------------------------------
    # 11. Answer
    # --------------------------------------------------
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {
                "role": "user",
                "content": content
            }
        ]
    )

    return response.output_text


# ============================================================
# EXAMPLE
# ============================================================

answer = ask_rag(
    "Transformer에 대한 아키텍처 구조를 설명해줘"
)

print(answer)