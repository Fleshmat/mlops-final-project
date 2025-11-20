import os
import requests
import gradio as gr
import io
from PIL import Image

LLM_URL = os.getenv("LLM_URL")
SKLEARN_URL = os.getenv("SKLEARN_URL")
CNN_URL = os.getenv("CNN_URL")


def ask_llm(question: str):
    try:
        resp = requests.post(LLM_URL, json={"question": question}, timeout=70)
        return resp.json().get("answer")
    except Exception as exc:
        return f"LLM inalcanzable: {exc}"


def predict_tabular(values: str):
    try:
        vals = [float(x.strip()) for x in values.split(",")]
        resp = requests.post(SKLEARN_URL, json={"features": vals}, timeout=70)
        return resp.json()
    except Exception as exc:
        return {"error": str(exc)}


def predict_tabular(account_age_days, total_transactions_user,
                    avg_amount_user, amount, promo_used, avs_match,
                    cvv_result, three_ds_flag, shipping_distance_km,
                    country, channel, merchant_category):
    
    country_map = {"DE":0,"ES":1,"FR":2,"GB":3,"IT":4,"NL":5,"PL":6,"RO":7,"TR":8,"US":9}
    channel_map = {"app":0,"web":1}
    merchant_map = {"electronics":0,"fashion":1,"gaming":2,"grocery":3,"travel":4}
    
    try:
        vals = [
            int(account_age_days),
            int(total_transactions_user),
            float(avg_amount_user),
            float(amount),
            int(promo_used),
            int(avs_match),
            int(cvv_result),
            int(three_ds_flag),
            float(shipping_distance_km),
            country_map[country],
            channel_map[channel],
            merchant_map[merchant_category]
        ]

        resp = requests.post(SKLEARN_URL, json={"features": vals}, timeout=70)
        return resp.json()
    except Exception as exc:
        return {"error": str(exc)}


def classify_image(image):
    try:
        pil_img = Image.fromarray(image.astype("uint8"))
        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG")
        buf.seek(0)
        files = {"file": ("img.jpg", buf, "image/jpeg")}
        resp = requests.post(CNN_URL, files=files, timeout=90)
        return resp.json()
    except Exception as exc:
        return {"error": str(exc)}


with gr.Blocks() as demo:
    gr.Markdown("# MLOps Final Project — Frontend con Gradio")
    with gr.Tab("Chat LLM"):
        inp = gr.Textbox(label="Pregunta")
        out = gr.Textbox(label="Respuesta", lines=15)
        btn = gr.Button("Preguntar")
        btn.click(fn=ask_llm, inputs=inp, outputs=out)
    with gr.Tab("Detección de Fraude"):
        account_age_days = gr.Number(label="Antigüedad de la cuenta (días)")
        total_transactions_user = gr.Number(label="Total de transacciones del usuario")
        avg_amount_user = gr.Number(label="Monto promedio del usuario")
        amount = gr.Number(label="Monto de la transacción")
        promo_used = gr.Radio(choices=["0","1"], label="Promoción usada")
        avs_match = gr.Radio(choices=["0","1"], label="Coincidencia AVS")
        cvv_result = gr.Radio(choices=["0","1"], label="Resultado CVV")
        three_ds_flag = gr.Radio(choices=["0","1"], label="Seguridad 3DS activada")
        shipping_distance_km = gr.Number(label="Distancia de envío (km)")
        country = gr.Dropdown(choices=["DE","ES","FR","GB","IT","NL","PL","RO","TR","US"], label="País")
        channel = gr.Dropdown(choices=["app","web"], label="Canal")
        merchant_category = gr.Dropdown(choices=["electronics","fashion","gaming","grocery","travel"], label="Categoría del comerciante")

        pred_btn = gr.Button("Predecir")
        pred_out = gr.JSON()

        pred_btn.click(
            fn=predict_tabular,
            inputs=[account_age_days, total_transactions_user,
                    avg_amount_user, amount, promo_used, avs_match,
                    cvv_result, three_ds_flag, shipping_distance_km,
                    country, channel, merchant_category],
            outputs=pred_out
        )
    with gr.Tab("Clasificador de Imágenes"):
        img_in = gr.Image(type="numpy", height=224, width=224, label="Sube una imagen de un dígito (0-3)")
        img_btn = gr.Button("Clasificar")
        img_out = gr.JSON()
        img_btn.click(fn=classify_image, inputs=img_in, outputs=img_out)


def main():
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
