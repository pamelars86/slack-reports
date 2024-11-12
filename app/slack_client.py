import time
import backoff
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.llm_client import generate_summary_with_llm

from . import logger
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Crea el cliente de Slack con el token de autenticación
client = WebClient(token=os.getenv("SLACK_TOKEN"))
slack_home = os.getenv("SLACK_HOME")

if not client:
    logger.error("SLACK_API_TOKEN debe estar configurado en el entorno")

    raise EnvironmentError("SLACK_API_TOKEN deve estar configurado no ambiente")
else:
    logger.info("Cliente de Slack creado con éxito")

 # Función para obtener mensajes de un canal de Slack en un rango de fechas, con reintentos exponenciales
@backoff.on_exception(
    backoff.expo,                   # Estrategia de reintento exponencial
    SlackApiError,                  # Excepción a capturar
    max_time=300,                   # Tiempo máximo de reintento en segundos (5 minutos)
    jitter=backoff.full_jitter,     # Agrega jitter para evitar picos
    giveup=lambda e: e.response["error"] != "ratelimited",  # Sólo se reintenta si el error es 'ratelimited'
    on_backoff=lambda details: logger.info(f"Reintentando... {details}")
)
def fetch_messages(channel, start_date, end_date):
    messages = []
    try:
        # Convierte las fechas de inicio y fin en timestamps
        start_ts = time.mktime(datetime.strptime(start_date, "%Y-%m-%d").timetuple())
        end_ts = time.mktime(datetime.strptime(end_date, "%Y-%m-%d").timetuple())
        next_cursor = None

        # Itera sobre las páginas de mensajes usando el cursor de paginación
        while True:
            try:
                # Intentamos obtener los mensajes
                response = client.conversations_history(
                    channel=channel,
                    oldest=start_ts,
                    latest=end_ts,
                    limit=100,
                    cursor=next_cursor
                )
                for msg in response['messages']:
                    # Estructura el mensaje con la información necesaria
                    post_id =  msg.get("ts")
                    formatted_msg = {
                        "author": msg.get("user"),
                        "message": msg.get("text"),
                        "post_id": post_id,
                        "url": f"{slack_home}/archives/{channel}/p{post_id[:10]}.{post_id[-6:]}",
                        "date": datetime.fromtimestamp(float(msg.get("ts"))).isoformat(),
                        "reactions": {r["name"]: r["count"] for r in msg.get("reactions", [])},
                        "replies": []
                    }

                    # Si el mensaje tiene respuestas, las obtenemos y añadimos al mensaje
                    if "reply_count" in msg:
                        replies_response = fetch_replies(channel, msg["ts"])
                        formatted_msg["replies"] = replies_response

                        # TO DO Generar resumen para todo el hilo (mensaje + respuestas)
                        thread_content = msg["text"] + " ".join(reply["message"] for reply in replies_response)
                        formatted_msg["summary"] = generate_summary_with_llm(thread_content)
                    else:
                        # TO DO Generar resumen solo para el mensaje sin respuestas
                        formatted_msg["summary"] = generate_summary_with_llm(msg["text"])


                    messages.append(formatted_msg)

                # Actualiza el cursor para la siguiente página de mensajes
                next_cursor = response.get("response_metadata", {}).get("next_cursor")
                if not next_cursor:
                    break

            except SlackApiError as e:
                logger.error(f"Error en paginación de mensajes: {e}")
                logger.error(f"Error response en paginación de mensajes: {e.response}")
                return {"error": str(e)}

    except SlackApiError as e:
        logger.error(f"Error al obtener mensajes: {e}")
        logger.error(f"Error response en obtener mensajes: {e.response}")
        return {"error": str(e)}

    return messages

# Función para obtener respuestas (con reintentos exponenciales)
@backoff.on_exception(
    backoff.expo,                   # Estrategia de reintento exponencial
    SlackApiError,                  # Excepción a capturar
    max_time=300,                   # Tiempo máximo de reintento en segundos (5 minutos)
    jitter=backoff.full_jitter,     # Agrega jitter para evitar picos
    giveup=lambda e: e.response["error"] != "ratelimited",  # Solo se reintenta si es ratelimited
    on_backoff=lambda details: logger.info(f"Reintentando... {details}")
)
def fetch_replies(channel, ts):
    try:
        replies_response = client.conversations_replies(
            channel=channel,
            ts=ts
        )
        return [
            {
                "author": reply.get("user"),
                "message": reply.get("text"),
                "post_id": reply.get("ts"),
                "url": f"{slack_home}/archives/{channel}/p{reply.get('ts')[:10]}.{reply.get('ts')[-6:]}",
                "date": datetime.fromtimestamp(float(reply.get("ts"))).isoformat()
            } for reply in replies_response["messages"] if reply.get("ts") != ts
        ]
    except SlackApiError as e:
        logger.error(f"Error al obtener respuestas: {e}")
        logger.error(f"Error response en obtener respuestas: {e.response}")

        if 'error' in e.response and e.response["error"] == "ratelimited":
            logger.info("Error ratelimitado detectado. Aplicando backoff.")
        raise e  # Propaga el error para que sea manejado por backoff
    
def fetch_top_repliers():
    return []